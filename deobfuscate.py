#!/usr/bin/env python3
"""Turn AppleScript that hides its strings as character codes back into readable source.

Usage: python3 deobfuscate.py obfuscated.txt > readable.txt
"""
import re
import sys

STRING_LITERAL = re.compile(r'"(?:[^"\\]|\\.)*"')
CHARACTER_CALL = re.compile(r"\(\s*(?:character id|ASCII character)\s+(\d+)\s*\)")
STRING_ID_CALL = re.compile(r"\(\s*string id\s*\{([\d,\s]+)\}\s*\)")
JOIN_OPERATOR = re.compile(r"\s*&\s*")
OPENING_PAREN = re.compile(r"(?<![\w)])\(\s*$")
CLOSING_PAREN = re.compile(r"^\s*\)")


def as_literal(text):
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def decode_character_calls(source):
    source = CHARACTER_CALL.sub(lambda m: as_literal(chr(int(m.group(1)))), source)
    return STRING_ID_CALL.sub(
        lambda m: as_literal("".join(chr(int(code)) for code in m.group(1).split(","))),
        source,
    )


def split_into_code_and_strings(source):
    tokens, position = [], 0
    for literal in STRING_LITERAL.finditer(source):
        tokens.append(("code", source[position:literal.start()]))
        tokens.append(("string", literal.group()))
        position = literal.end()
    tokens.append(("code", source[position:]))
    return tokens


def is_join_between_strings(tokens):
    return (
        len(tokens) >= 2
        and tokens[-1][0] == "code"
        and JOIN_OPERATOR.fullmatch(tokens[-1][1])
        and tokens[-2][0] == "string"
    )


def join_adjacent_strings(tokens):
    joined = []
    for kind, text in tokens:
        if kind == "string" and is_join_between_strings(joined):
            joined.pop()
            _, left = joined.pop()
            joined.append(("string", left[:-1] + text[1:]))
        else:
            joined.append((kind, text))
    return joined


def unwrap_parenthesised_strings(tokens):
    tokens = list(tokens)
    for i in range(1, len(tokens) - 1):
        before, after = tokens[i - 1][1], tokens[i + 1][1]
        if tokens[i][0] == "string" and OPENING_PAREN.search(before) and CLOSING_PAREN.match(after):
            tokens[i - 1] = ("code", OPENING_PAREN.sub("", before))
            tokens[i + 1] = ("code", CLOSING_PAREN.sub("", after, count=1))
    return tokens


def collapse_concatenations(source):
    while True:
        tokens = split_into_code_and_strings(source)
        tokens = unwrap_parenthesised_strings(join_adjacent_strings(tokens))
        collapsed = "".join(text for _, text in tokens)
        if collapsed == source:
            return collapsed
        source = collapsed


def deobfuscate(source):
    return collapse_concatenations(decode_character_calls(source))


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python3 deobfuscate.py <obfuscated.txt>")
    with open(sys.argv[1], encoding="utf-8", errors="replace") as handle:
        print(deobfuscate(handle.read()), end="")


if __name__ == "__main__":
    main()
