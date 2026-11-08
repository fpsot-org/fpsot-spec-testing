#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Lints the Gherkin feature files of a folder. It runs no step.

Usage: check-features.py DIR

DIR holds one folder per language, en/ and fr/, with the same file names.
The check fails when:
  - a feature file does not parse with the official Gherkin parser (TST-034);
  - its first line is not the "# language:" header of its folder (TST-031);
  - a scenario or a background has a description, which is what a misspelled
    first step keyword gives, since the parser then reads that step as text;
  - a scenario has no When step or no Then step (TST-024);
  - a file exists in one language folder only (TST-032);
  - the two versions of a file differ in structure (TST-032): the order of
    rules, scenarios and examples, their tags, the number and kind of their
    steps, the cells of their data tables and the body rows of their
    examples. Names, descriptions, step text and the header row of an
    examples table are text in the language of the file, so they may differ.
"""
import pathlib
import sys

from gherkin.parser import Parser
from gherkin.token_matcher import TokenMatcher

LANGS = ("en", "fr")


def walk(children):
    """Yields each background and scenario, also those inside a rule."""
    for child in children:
        if "rule" in child:
            yield from walk(child["rule"]["children"])
        elif "background" in child:
            yield child["background"]
        elif "scenario" in child:
            yield child["scenario"]


def parse(path, lang, errors):
    text = path.read_text(encoding="utf-8")
    first = text.splitlines()[0] if text else ""
    if first.replace(" ", "") != f"#language:{lang}":
        errors.append(f"{path}:1: the first line must be '# language: {lang}'")
    try:
        doc = Parser().parse(text, TokenMatcher())
    except Exception as e:  # The parser raises one composite error with every finding.
        for line in str(e).splitlines():
            if line.strip() and line.strip() != "Parser errors:":
                errors.append(f"{path}: parse error {line.strip()}")
        return None
    if not doc.get("feature"):
        errors.append(f"{path}: no Feature")
        return None
    for node in walk(doc["feature"]["children"]):
        where = f"{path}:{node['location']['line']}: '{node['keyword']}'"
        if node.get("description", "").strip():
            errors.append(f"{where} has a description; check the keyword of its first step,"
                          " since the parser reads lines with no keyword as a description")
        kinds = {s["keywordType"] for s in node.get("steps", [])}
        if "examples" in node and not {"Action", "Outcome"} <= kinds:
            errors.append(f"{where} needs a When step and a Then step (TST-024)")
    return doc


def tags(node):
    return [t["name"] for t in node.get("tags", [])]


def table(rows):
    return [[c["value"] for c in r["cells"]] for r in rows or []]


def steps(node):
    out = []
    for s in node.get("steps", []):
        arg = None
        if "dataTable" in s:
            arg = ("table", table(s["dataTable"]["rows"]))
        elif "docString" in s:
            arg = ("docString", s["docString"].get("mediaType"))
        out.append((s["keywordType"], arg))
    return out


def shape(children):
    """The parts of a feature or rule that both language versions must share."""
    out = []
    for child in children:
        if "background" in child:
            out.append(("background", steps(child["background"])))
        elif "rule" in child:
            r = child["rule"]
            out.append(("rule", tags(r), shape(r["children"])))
        elif "scenario" in child:
            s = child["scenario"]
            examples = [
                (tags(e), len(e["tableHeader"]["cells"]) if e.get("tableHeader") else 0,
                 table(e.get("tableBody")))
                for e in s.get("examples", [])
            ]
            out.append(("scenario", tags(s), steps(s), examples))
    return out


def first_difference(a, b, where="feature"):
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if len(a) != len(b):
            return f"{where}: {len(a)} items in English, {len(b)} in French"
        for i, (x, y) in enumerate(zip(a, b)):
            d = first_difference(x, y, f"{where}[{i}]")
            if d:
                return d
        return None
    return None if a == b else f"{where}: {a!r} in English, {b!r} in French"


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    root = pathlib.Path(sys.argv[1])
    errors = []
    files = {lang: {p.name: p for p in sorted((root / lang).glob("*.feature"))} for lang in LANGS}
    if not any(files.values()):
        errors.append(f"{root}: no feature file found")
    docs = {lang: {n: parse(p, lang, errors) for n, p in files[lang].items()} for lang in LANGS}
    for name in sorted(set(files["en"]) | set(files["fr"])):
        missing = [lang for lang in LANGS if name not in files[lang]]
        if missing:
            errors.append(f"{root}/{missing[0]}/{name}: missing; each feature file needs"
                          " an English and a French version")
            continue
        en, fr = docs["en"][name], docs["fr"][name]
        if en is None or fr is None:
            continue
        a = ("feature", tags(en["feature"]), shape(en["feature"]["children"]))
        b = ("feature", tags(fr["feature"]), shape(fr["feature"]["children"]))
        d = first_difference(a, b)
        if d:
            errors.append(f"{root}: en/{name} and fr/{name} are not in parity: {d}")
    for e in errors:
        print(f"FAIL: {e}")
    if not errors:
        print(f"PASS: {root}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
