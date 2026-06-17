#!/usr/bin/env python3
"""
LinkedIn Post Validator - Validates 360Brew specs
Usage: python validate_specs.py <post_file.txt>
"""

import argparse
import re
import sys
from pathlib import Path

# 360Brew specs
SPECS = {
    "chars_min": 1250,
    "chars_max": 2500,
    "chars_warning_min": 1000,
    "chars_warning_max": 3000,
    "paragraphs_min": 14,
    "paragraphs_warning": 10,
    "avg_word_length_max": 5,
    "avg_word_length_warning": 6,
    "max_words_per_paragraph": 19,
}

# Punished patterns
# Anchored to avoid false positives (e.g. "not everyone agrees with me")
PUNISHED_PATTERNS = [
    (r"\bwhat do you think\s*\?", "What do you think?"),
    (r"(?:^|[.!?…]\s*)(?:agree|right)\s*\?", "Agree?"),
    (r"\bgood morning[,]?\s*linkedin", "Good morning, LinkedIn"),
    (r"\bthought of the day\b", "Thought of the day"),
]


def count_chars(text: str) -> int:
    return len(text.strip())


def split_paragraphs(text: str) -> list:
    """Paragraphs = blocks separated by a blank line (LinkedIn format)."""
    return [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]


def count_paragraphs(text: str) -> int:
    return len(split_paragraphs(text))


def avg_word_length(text: str) -> float:
    words = re.findall(r"\b[a-z']+\b", text.lower())
    if not words:
        return 0
    return sum(len(w) for w in words) / len(words)


def has_link_in_body(text: str) -> bool:
    """Detects a link ANYWHERE in the body. The 360Brew rule has no exception:
    links belong in the 1st comment, never in the post (-60% reach)."""
    return bool(re.search(r'https?://|www\.', text, re.IGNORECASE))


def count_hashtags(text: str) -> int:
    return len(re.findall(r'#\w+', text))


def get_long_paragraphs(text: str) -> list:
    """Returns paragraphs with more than 19 words"""
    paragraphs = split_paragraphs(text)
    long_paras = []
    for i, p in enumerate(paragraphs, 1):
        words = len(p.split())
        if words > SPECS["max_words_per_paragraph"]:
            long_paras.append((i, words, p[:50] + "..."))
    return long_paras


def check_punished_patterns(text: str) -> list:
    """Checks for patterns punished by the algorithm"""
    found = []
    for pattern, name in PUNISHED_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            found.append(name)
    return found


def validate_post(text: str) -> dict:
    """Validates a post against the 360Brew specs"""

    results = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "stats": {},
        "suggestions": []
    }

    # Basic stats
    chars = count_chars(text)
    paragraphs = count_paragraphs(text)
    avg_len = avg_word_length(text)

    results["stats"] = {
        "characters": chars,
        "paragraphs": paragraphs,
        "avg_word_length": round(avg_len, 1),
    }

    # Validate character count
    if chars < SPECS["chars_warning_min"]:
        results["errors"].append(f"Too short: {chars} chars (acceptable minimum: {SPECS['chars_warning_min']}; recommended: {SPECS['chars_min']}-{SPECS['chars_max']})")
        results["valid"] = False
        results["suggestions"].append("Expand the content with more context or examples")
    elif chars < SPECS["chars_min"]:
        results["warnings"].append(f"Below ideal: {chars} chars (recommended: {SPECS['chars_min']}-{SPECS['chars_max']})")
    elif chars > SPECS["chars_warning_max"]:
        results["errors"].append(f"Too long: {chars} chars (acceptable maximum: {SPECS['chars_warning_max']}; recommended: {SPECS['chars_min']}-{SPECS['chars_max']})")
        results["valid"] = False
        results["suggestions"].append("Cut the less essential parts")
    elif chars > SPECS["chars_max"]:
        results["warnings"].append(f"Above ideal: {chars} chars (recommended: {SPECS['chars_min']}-{SPECS['chars_max']})")

    # Validate paragraphs
    if paragraphs < SPECS["paragraphs_warning"]:
        results["errors"].append(f"Too few paragraphs: {paragraphs} (minimum: {SPECS['paragraphs_min']})")
        results["valid"] = False
        results["suggestions"].append("Break the text into more short paragraphs (1-3 lines each)")
    elif paragraphs < SPECS["paragraphs_min"]:
        results["warnings"].append(f"Paragraphs below ideal: {paragraphs} (recommended: {SPECS['paragraphs_min']}+)")

    # Validate word complexity
    if avg_len > SPECS["avg_word_length_warning"]:
        results["errors"].append(f"Words too complex: average {avg_len:.1f} letters (maximum: {SPECS['avg_word_length_max']})")
        results["valid"] = False
        results["suggestions"].append("Use simpler, shorter words")
    elif avg_len > SPECS["avg_word_length_max"]:
        results["warnings"].append(f"Words a bit complex: average {avg_len:.1f} letters (ideal: ≤{SPECS['avg_word_length_max']})")

    # Check long paragraphs
    long_paras = get_long_paragraphs(text)
    if long_paras:
        for para_num, word_count, preview in long_paras:
            results["warnings"].append(f"Paragraph {para_num} too long: {word_count} words")
        results["suggestions"].append(f"Break the {len(long_paras)} long paragraphs into smaller blocks")

    # Check punished patterns
    punished = check_punished_patterns(text)
    if punished:
        for p in punished:
            results["errors"].append(f"Punished pattern detected: '{p}'")
        results["valid"] = False
        results["suggestions"].append("Remove bait patterns and use proof-of-work / authority hooks")

    # Check for a link in the body (-60% reach)
    if has_link_in_body(text):
        results["errors"].append("Link in the post body detected (-60% reach)")
        results["valid"] = False
        results["suggestions"].append("Move the link to the 1st comment")

    # Check hashtags
    hashtag_count = count_hashtags(text)
    results["stats"]["hashtags"] = hashtag_count
    if hashtag_count > 2:
        results["errors"].append(f"Too many hashtags: {hashtag_count} (2026 default: zero, max 2 hyper-specific)")
        results["valid"] = False
        results["suggestions"].append("Remove generic hashtags, keep at most 2 ultra-specific ones")
    elif hashtag_count > 0:
        results["warnings"].append(f"{hashtag_count} hashtag(s) detected — confirm they are hyper-specific")

    return results


def print_report(results: dict):
    """Prints the validation report"""

    print("\n" + "="*60)
    print("VALIDATION OF SPECS - LinkedIn 360Brew")
    print("="*60)

    # Overall status
    if results["valid"]:
        print("\n[OK] VALID POST - 360Brew specs met")
    else:
        print("\n[X] INVALID POST - Fix the errors below")

    # Stats
    print("\nSTATISTICS:")
    for stat, value in results["stats"].items():
        print(f"   - {stat}: {value}")

    # Errors
    if results["errors"]:
        print("\nERRORS (blocks publishing):")
        for err in results["errors"]:
            print(f"   - {err}")

    # Warnings
    if results["warnings"]:
        print("\nWARNINGS (recommended to fix):")
        for warn in results["warnings"]:
            print(f"   - {warn}")

    # Suggestions
    if results["suggestions"]:
        print("\nSUGGESTIONS:")
        for sug in results["suggestions"]:
            print(f"   - {sug}")

    # Reference specs
    print("\n" + "-"*60)
    print("360BREW REFERENCE SPECS:")
    print(f"   - Characters: {SPECS['chars_min']}-{SPECS['chars_max']}")
    print(f"   - Paragraphs: {SPECS['paragraphs_min']}+ short")
    print(f"   - Words: average ≤{SPECS['avg_word_length_max']} letters")
    print(f"   - Paragraphs: max {SPECS['max_words_per_paragraph']} words each")
    print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Validate LinkedIn post specs")
    parser.add_argument("file", help="File with the post text")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--quiet", "-q", action="store_true", help="Status only (exit code)")

    args = parser.parse_args()

    # Read file
    try:
        text = Path(args.file).read_text(encoding='utf-8')
    except FileNotFoundError:
        print(f"Error: file '{args.file}' not found")
        sys.exit(1)

    # Validate
    results = validate_post(text)

    # Output
    if args.quiet:
        sys.exit(0 if results["valid"] else 1)
    elif args.json:
        import json
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_report(results)

    sys.exit(0 if results["valid"] else 1)


if __name__ == "__main__":
    main()
