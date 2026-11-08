#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Lints the Gherkin feature files of a folder. It runs no step.

Usage: check-features.py DIR

DIR holds one folder per language, en/ and fr/, with the same file names.
The check fails when:
  - a feature file does not parse with the official Gherkin parser (TST-034);
  - its first line is not exactly "# language: en" or "# language: fr",
    as its folder requires (TST-031);
  - it uses a keyword outside the table of TST-031, such as "Soit",
    "Lorsque", "Exemple" or "*" (TST-031);
  - a scenario, a Scenario Outline or a background has a description
    (TST-036), which is also what a misspelled first step keyword gives,
    since the parser then reads that step as text;
  - a scenario has no When step or no Then step (TST-024);
  - a file exists in one language folder only (TST-030);
  - the two versions of a file differ in structure (TST-032): the order of
    rules, scenarios and examples, their tags, the number of steps and the
    column of TST-031 that each step keyword comes from, the values between
    double quotes in each step, the cells of data tables and the body rows of
    examples. Names, the descriptions of features and rules, the other text of
    steps and the header row of an examples table are text in the language of
    the file, so they may differ.
"""
import pathlib
import re
import sys

from gherkin.parser import Parser
from gherkin.token_matcher import TokenMatcher

LANGS = ("en", "fr")

# The keyword table of TST-031: one keyword per element and language.
KEYWORDS = {
    "en": {
        "feature": "Feature", "background": "Background", "rule": "Rule",
        "scenario": "Scenario", "outline": "Scenario Outline", "examples": "Examples",
        "given": "Given", "when": "When", "then": "Then", "and": "And", "but": "But",
    },
    "fr": {
        "feature": "Fonctionnalité", "background": "Contexte", "rule": "Règle",
        "scenario": "Scénario", "outline": "Plan du scénario", "examples": "Exemples",
        "given": "Étant donné", "when": "Quand", "then": "Alors", "and": "Et", "but": "Mais",
    },
}
STEP_COLUMNS = ("given", "when", "then", "and", "but")
QUOTED = re.compile(r'"([^"]*)"')
PLACEHOLDER = re.compile(r"<([^<>]+)>")


def walk(children):
    """Yields each background and scenario, also those inside a rule."""
    for child in children:
        if "rule" in child:
            yield from walk(child["rule"]["children"])
        elif "background" in child:
            yield child["background"]
        elif "scenario" in child:
            yield child["scenario"]


def check_keywords(path, lang, feature, errors):
    table = KEYWORDS[lang]
    steps_of = {table[c]: c for c in STEP_COLUMNS}

    def expect(node, column):
        if node["keyword"].strip() != table[column]:
            errors.append(f"{path}:{node['location']['line']}: keyword '{node['keyword'].strip()}';"
                          f" TST-031 allows '{table[column]}' here")

    expect(feature, "feature")

    def visit(children):
        for child in children:
            if "rule" in child:
                expect(child["rule"], "rule")
                visit(child["rule"]["children"])
                continue
            node = child.get("background") or child.get("scenario")
            if "background" in child:
                expect(node, "background")
            else:
                expect(node, "outline" if node.get("examples") else "scenario")
                for e in node.get("examples", []):
                    expect(e, "examples")
            for s in node.get("steps", []):
                if s["keyword"].strip() not in steps_of:
                    errors.append(f"{path}:{s['location']['line']}: step keyword '{s['keyword'].strip()}';"
                                  f" TST-031 allows only {', '.join(repr(k) for k in steps_of)}")

    visit(feature["children"])


def parse(path, lang, errors):
    text = path.read_text(encoding="utf-8")
    first = text.splitlines()[0] if text else ""
    if first != f"# language: {lang}":
        errors.append(f"{path}:1: the first line must be exactly '# language: {lang}'")
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
    check_keywords(path, lang, doc["feature"], errors)
    for node in walk(doc["feature"]["children"]):
        where = f"{path}:{node['location']['line']}: '{node['keyword']}'"
        if node.get("description", "").strip():
            errors.append(f"{where} has a description (TST-036); check the keyword of its first step,"
                          " since the parser reads lines with no keyword as a description")
        kinds = {s["keywordType"] for s in node.get("steps", [])}
        if "examples" in node and not {"Action", "Outcome"} <= kinds:
            errors.append(f"{where} needs a When step and a Then step (TST-024)")
    return doc


def tags(node):
    return [t["name"] for t in node.get("tags", [])]


def table(rows):
    return [[c["value"] for c in r["cells"]] for r in rows or []]


def column(lang, keyword):
    for c in STEP_COLUMNS:
        if KEYWORDS[lang][c] == keyword.strip():
            return c
    return keyword.strip()


def steps(node, lang, header):
    """Each step as its keyword column, its quoted values and its argument.

    A placeholder such as <full name> becomes the position of its column in the
    examples header, since the header names differ between the languages."""
    out = []
    for s in node.get("steps", []):
        values = [PLACEHOLDER.sub(lambda m: f"<{header.index(m.group(1))}>" if m.group(1) in header
                                  else m.group(0), v) for v in QUOTED.findall(s["text"])]
        arg = None
        if "dataTable" in s:
            arg = ("table", table(s["dataTable"]["rows"]))
        elif "docString" in s:
            arg = ("docString", s["docString"].get("mediaType"))
        out.append((column(lang, s["keyword"]), values, arg))
    return out


def shape(children, lang):
    """The parts of a feature or rule that both language versions must share."""
    out = []
    for child in children:
        if "background" in child:
            out.append(("background", steps(child["background"], lang, [])))
        elif "rule" in child:
            r = child["rule"]
            out.append(("rule", tags(r), shape(r["children"], lang)))
        elif "scenario" in child:
            s = child["scenario"]
            header = []
            examples = []
            for e in s.get("examples", []):
                cells = [c["value"] for c in e["tableHeader"]["cells"]] if e.get("tableHeader") else []
                header = header or cells
                examples.append((tags(e), len(cells), table(e.get("tableBody"))))
            out.append(("scenario", tags(s), steps(s, lang, header), examples))
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
        a = ("feature", tags(en["feature"]), shape(en["feature"]["children"], "en"))
        b = ("feature", tags(fr["feature"]), shape(fr["feature"]["children"], "fr"))
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
