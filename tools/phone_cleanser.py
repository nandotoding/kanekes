"""Phone-number row cleansing utilities for Kanekes."""

import re
from typing import List, Tuple

# Number-like tokens with at least seven digits. Separators commonly used in
# phone numbers are accepted, while surrounding punctuation is left outside.
NUMBER_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9])\+?\d(?:[\d\s().-]*\d)?(?![A-Za-z0-9])")
LEADING_ROW_NUMBER_RE = re.compile(r"^\s*(?:\d{1,4}\s*[.)、:-]\s*)+")
DASHES = "-–—"


def _digit_count(value: str) -> int:
    return sum(ch.isdigit() for ch in value)


def _extract_number_tokens(line: str) -> List[Tuple[int, int, str]]:
    found = []
    for match in NUMBER_TOKEN_RE.finditer(line):
        token = match.group(0).strip()
        if _digit_count(token) >= 7:
            found.append((match.start(), match.end(), token))
    return found


def _normalize_number(token: str) -> str:
    digits = "".join(ch for ch in token if ch.isdigit())
    if token.lstrip().startswith("+") and digits.startswith("62"):
        return digits
    if digits.startswith("62"):
        return digits
    if digits.startswith("08"):
        return "62" + digits[1:]
    if digits.startswith("8"):
        return "62" + digits
    # Keep unusual numeric strings unchanged rather than discarding them.
    return digits


def _clean_name(text: str) -> str:
    text = re.sub(r"^[\s:;,|/\\()\[\]{}.!?]+", "", text)
    text = re.sub(r"[\s:;,|/\\()\[\]{}.!?]+$", "", text)
    # Remove punctuation around words, but retain internal apostrophes and
    # digits that distinguish similar names/initials.
    text = re.sub(r"[()\[\]{}.,;:!?|/\\]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _name_from_line(line: str, matches: List[Tuple[int, int, str]]) -> str:
    # Remove all detected number tokens while retaining the text around them.
    pieces = []
    cursor = 0
    for start, end, _ in matches:
        pieces.append(line[cursor:start])
        cursor = end
    pieces.append(line[cursor:])
    remaining = " ".join(pieces)

    # If hyphens divide a label from the actual name, the last non-empty
    # segment is the name. This also preserves "john doe - 0812..." because
    # the only non-empty segment before the number is "john doe".
    segments = [_clean_name(part) for part in re.split(r"\s*[-–—]\s*", remaining)]
    segments = [part for part in segments if part]
    if not segments:
        return ""
    return segments[-1]


def clean_phone_rows(raw_text: str) -> Tuple[str, int]:
    """Return cleaned rows and the number of output rows.

    A row without a detectable numeric token (7+ digits) is discarded.
    Every detected number produces one output row using the same name.
    """
    output: List[str] = []

    for raw_line in raw_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        # Remove leading list numbering such as "1.", "2)", or "3 -".
        line = LEADING_ROW_NUMBER_RE.sub("", line).strip()
        if not line:
            continue

        matches = _extract_number_tokens(line)
        if not matches:
            continue

        name = _name_from_line(line, matches)
        if not name:
            continue

        for _, _, token in matches:
            number = _normalize_number(token)
            if number:
                output.append(f"{name} {number}")

    return "\n".join(output), len(output)
