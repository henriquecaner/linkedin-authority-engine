#!/usr/bin/env python3
"""
LinkedIn Post Scorer v3.5 - Computes a score based on the 6 360Brew dimensions.

Usage: python score_post.py <post_file.txt> [--objective authority|sales|engagement] [--lang auto|pt|en]

Multilingual: matches Portuguese and English posts (union matching by default).
Default output: readable report. Use --json for structured output.
Use --compact for a 1-line summary (handy for workflow integration).
"""

import argparse
import re
import sys
from pathlib import Path

import postlib

# Dimension weights (v3.5) — aligned with the Metrics section of
# skills/360brew-algorithm/SKILL.md
WEIGHTS = {
    "saves_potential": 0.30,
    "hook": 0.20,
    "algorithm": 0.20,
    "structure": 0.15,
    "cta": 0.10,
    "data": 0.05,
}


def extract_hook(text: str) -> str:
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    return '\n'.join(lines[:3])


# -----------------------------
# Dimensions (6)
# -----------------------------

def score_saves_potential(text: str, lang: str) -> tuple:
    """Evaluates save potential (30%). The strongest algorithm signal."""
    feedback = []
    score = 4.0

    matches = postlib.find_saves(text, lang)

    if len(matches) >= 3:
        score = 10.0
        feedback.append(f"[+] High save potential: {', '.join(matches[:3])}")
    elif len(matches) == 2:
        score = 8.5
        feedback.append(f"[+] Good save potential: {', '.join(matches)}")
    elif len(matches) == 1:
        score = 6.5
        feedback.append(f"[o] Moderate potential: {matches[0]}")
    else:
        score = 3.5
        feedback.append("[X] No save triggers — add a framework, checklist or numbered list")

    last_lines = '\n'.join(text.split('\n')[-5:])
    if postlib.has_save_cta(last_lines, lang):
        score = min(10, score + 1.0)
        feedback.append("[+] Explicit save CTA (+1)")

    return min(10, max(0, score)), feedback


def score_hook(text: str, lang: str) -> tuple:
    feedback = []
    score = 5.0
    hook = extract_hook(text)

    if postlib.find_punished(text, lang):
        score -= 4.0
        feedback.append("[X] Hook punished by 360Brew detected (-4)")

    if re.search(r'\d+', hook):
        score += 1.5
        feedback.append("[+] Specific numbers in the hook (+1.5)")

    if postlib.has_proof_of_work(hook, lang):
        score += 2.0
        feedback.append("[+] Proof of work detected (+2)")

    if postlib.has_authority(hook, lang):
        score += 1.5
        feedback.append("[+] Authority proof detected (+1.5)")

    if postlib.has_transformation_range(hook, lang):
        score += 1.5
        feedback.append("[+] Transformation with numbers (+1.5)")

    return min(10, max(0, score)), feedback


def score_algorithm(text: str, lang: str) -> tuple:
    """Evaluates adherence to the 360Brew specs (20%). Saves is now a separate dimension."""
    feedback = []
    score = 5.0

    if postlib.has_link_in_body(text):
        score -= 4.0
        feedback.append("[X] Link in the post body detected (-4) — move it to the 1st comment")
    else:
        score += 1.5
        feedback.append("[+] No links in the body (+1.5)")

    hashtag_count = postlib.count_hashtags(text)
    if hashtag_count == 0:
        score += 1.0
        feedback.append("[+] No hashtags (2026 default) (+1)")
    elif hashtag_count <= 2:
        score += 0.5
        feedback.append(f"[o] {hashtag_count} hashtag(s) — acceptable if hyper-specific (+0.5)")
    else:
        score -= 2.0
        feedback.append(f"[X] {hashtag_count} hashtags — excess punished (-2)")

    avg_len = postlib.avg_word_length(text)
    if avg_len <= 5:
        score += 2.0
        feedback.append(f"[+] Simple words: average {avg_len:.1f} letters (+2)")
    elif avg_len <= 6:
        score += 1.0
        feedback.append(f"[o] Words OK: average {avg_len:.1f} letters (+1)")
    else:
        score -= 1.5
        feedback.append(f"[X] Complex words: average {avg_len:.1f} letters (-1.5)")

    if postlib.find_punished(text, lang):
        score -= 1.5
        feedback.append("[X] Bait pattern detected in the hook (-1.5)")
    else:
        score += 0.5
        feedback.append("[+] No bait patterns (+0.5)")

    return min(10, max(0, score)), feedback


def score_structure(text: str, lang: str) -> tuple:
    """Structure (15%): 3 sub-components — Length, Paragraphs, Framework."""
    feedback = []
    score = 5.0

    chars = postlib.count_chars(text)
    paragraphs = postlib.count_paragraphs(text)
    specs = postlib.SPECS

    # Length
    if specs["chars_min"] <= chars <= specs["chars_max"]:
        score += 2.0
        feedback.append(f"[+] Ideal length: {chars} chars (+2)")
    elif chars < specs["chars_warning_min"]:
        score -= 2.5
        feedback.append(f"[X] Too short: {chars} chars (-2.5)")
    elif chars > specs["chars_warning_max"]:
        score -= 2.0
        feedback.append(f"[X] Too long: {chars} chars (-2)")
    else:
        feedback.append(f"[o] Length outside the optimal range: {chars} chars (0)")

    # Paragraphs
    if paragraphs >= specs["paragraphs_min"]:
        score += 2.0
        feedback.append(f"[+] Scannability: {paragraphs} paragraphs (+2)")
    elif paragraphs >= specs["paragraphs_warning"]:
        score += 1.0
        feedback.append(f"[o] Paragraphs OK: {paragraphs} (+1)")
    else:
        score -= 2.0
        feedback.append(f"[X] Too few paragraphs: {paragraphs} (-2) — break up the text more")

    # Dense blocks (paragraph longer than the spec, per skills/360brew-algorithm/SKILL.md)
    dense_blocks = sum(1 for para in postlib.split_paragraphs(text) if len(para) > specs["dense_paragraph_chars"])
    if dense_blocks > 2:
        score -= 1.5
        feedback.append(f"[X] {dense_blocks} dense blocks detected (-1.5)")

    # Framework (weak heuristic)
    if postlib.framework_signal_count(text, lang) >= 3:
        score += 1.0
        feedback.append("[+] Detectable framework (+1)")

    return min(10, max(0, score)), feedback


def score_cta(text: str, objective: str, lang: str) -> tuple:
    feedback = []
    score = 5.0
    last_lines = '\n'.join(text.split('\n')[-5:])

    detected = postlib.find_ctas(last_lines, lang)
    # Dedupe: variations of the same CTA don't count as multiple CTAs
    if "comment_dm" in detected and "dm" in detected:
        detected.remove("dm")
    if "click" in detected and "bio" in detected:
        detected.remove("click")

    if not detected:
        score = 3.5
        feedback.append("[X] CTA not detected or too weak")
    else:
        score = 7.0
        feedback.append(f"[+] CTA present ({detected[0]})")

    if "save" in detected:
        score = min(10, score + 2.0)
        feedback.append("[+] Save CTA (2026 priority) (+2)")

    if objective == "authority" and "follow" in detected:
        score = min(10, score + 1.0)
        feedback.append("[+] CTA aligned with Authority (+1)")
    elif objective == "sales" and ("comment_dm" in detected or "dm" in detected):
        score = min(10, score + 1.0)
        feedback.append("[+] CTA aligned with Sales (+1)")
    elif objective == "engagement" and detected and postlib.has_engagement_cue(last_lines, lang):
        score = min(10, score + 1.0)
        feedback.append("[+] CTA aligned with Engagement (+1)")

    if len(detected) > 1:
        score -= 1.5
        feedback.append(f"[!] Multiple CTAs detected ({len(detected)}) — use only 1 (-1.5)")

    return min(10, max(0, score)), feedback


def score_data(text: str, lang: str) -> tuple:
    feedback = []
    data_count = postlib.count_data_points(text, lang)

    if data_count >= 5:
        score = 10.0
        feedback.append(f"[+] Excellent: {data_count} data points")
    elif data_count >= 3:
        score = 8.0
        feedback.append(f"[+] Good: {data_count} data points")
    elif data_count >= 1:
        score = 6.0
        feedback.append(f"[o] Basic: {data_count} data points — add more numbers")
    else:
        score = 3.0
        feedback.append("[X] No concrete data — add numbers, %, values")

    return score, feedback


# -----------------------------
# Aggregation
# -----------------------------

def calculate_probabilities(final_score, saves_score, hook_score, algo_score):
    top1_base = (final_score / 10) * 20
    top1_bonus = 0
    if saves_score >= 9:
        top1_bonus += 7
    if hook_score >= 9:
        top1_bonus += 4
    if algo_score >= 9:
        top1_bonus += 4
    top1 = min(35, top1_base + top1_bonus)

    top5_base = (final_score / 10) * 50
    top5_bonus = 0
    if saves_score >= 8:
        top5_bonus += 10
    if hook_score >= 8:
        top5_bonus += 7
    if algo_score >= 8:
        top5_bonus += 7
    top5 = min(75, top5_base + top5_bonus)

    return {"top1": top1, "top5": top5}


def score_post(text, objective="authority", lang="auto"):
    saves_score, saves_fb = score_saves_potential(text, lang)
    hook_score, hook_fb = score_hook(text, lang)
    algo_score, algo_fb = score_algorithm(text, lang)
    structure_score, structure_fb = score_structure(text, lang)
    cta_score, cta_fb = score_cta(text, objective, lang)
    data_score, data_fb = score_data(text, lang)

    final_score = (
        saves_score * WEIGHTS["saves_potential"] +
        hook_score * WEIGHTS["hook"] +
        algo_score * WEIGHTS["algorithm"] +
        structure_score * WEIGHTS["structure"] +
        cta_score * WEIGHTS["cta"] +
        data_score * WEIGHTS["data"]
    )

    probs = calculate_probabilities(final_score, saves_score, hook_score, algo_score)

    dimensions = [
        ("Saves Potential", saves_score),
        ("Hook", hook_score),
        ("Algorithm", algo_score),
        ("Structure", structure_score),
        ("CTA", cta_score),
        ("Data", data_score),
    ]
    dimensions_sorted = sorted(dimensions, key=lambda x: x[1], reverse=True)

    return {
        "language": postlib.detect_language(text) if lang == "auto" else lang,
        "final_score": round(final_score, 1),
        "dimensions": {
            "saves_potential": {"score": saves_score, "feedback": saves_fb},
            "hook": {"score": hook_score, "feedback": hook_fb},
            "algorithm": {"score": algo_score, "feedback": algo_fb},
            "structure": {"score": structure_score, "feedback": structure_fb},
            "cta": {"score": cta_score, "feedback": cta_fb},
            "data": {"score": data_score, "feedback": data_fb},
        },
        "strongest": [d[0] for d in dimensions_sorted[:2]],
        "weakest": [d[0] for d in dimensions_sorted[-2:]],
        "probabilities": probs,
        "recommendation": get_recommendation(final_score),
    }


def get_recommendation(score):
    if score >= 9.0:
        return "PUBLISH — outlier candidate"
    elif score >= 8.0:
        return "REVIEW — quick tweaks, then publish"
    elif score >= 7.0:
        return "REWORK — clear bottlenecks"
    elif score >= 6.0:
        return "REDO — structural fix"
    else:
        return "START OVER — back to objective + structure"


def print_report(result):
    print("\n" + "=" * 60)
    print("SCORE REPORT — LinkedIn 360Brew (v3.5)")
    print("=" * 60)

    print(f"\nFINAL SCORE: {result['final_score']}/10  (language: {result['language']})")
    print(f"   {result['recommendation']}")

    print(f"\nProbabilities:")
    print(f"   Top 1%: {result['probabilities']['top1']:.0f}%")
    print(f"   Top 5%: {result['probabilities']['top5']:.0f}%")

    print(f"\nStrongest dimensions: {', '.join(result['strongest'])}")
    print(f"Weakest dimensions: {', '.join(result['weakest'])}")

    print("\n" + "-" * 60)
    print("BREAKDOWN BY DIMENSION:")
    print("-" * 60)

    labels = {
        "saves_potential": "SAVES POTENTIAL",
        "hook": "HOOK",
        "algorithm": "ALGORITHM",
        "structure": "STRUCTURE",
        "cta": "CTA",
        "data": "DATA",
    }

    for dim_key, dim_data in result['dimensions'].items():
        weight = WEIGHTS[dim_key] * 100
        print(f"\n{labels[dim_key]} ({weight:.0f}%): {dim_data['score']}/10")
        for fb in dim_data['feedback']:
            print(f"   {fb}")

    print("\n" + "=" * 60)


def print_compact(result):
    d = result["dimensions"]
    print(
        f"Score {result['final_score']}/10 [{result['language']}] | "
        f"Top1: {result['probabilities']['top1']:.0f}% | "
        f"Top5: {result['probabilities']['top5']:.0f}% | "
        f"Saves {d['saves_potential']['score']:.1f} Hook {d['hook']['score']:.1f} "
        f"Algo {d['algorithm']['score']:.1f} Struct {d['structure']['score']:.1f} "
        f"CTA {d['cta']['score']:.1f} Data {d['data']['score']:.1f} | "
        f"{result['recommendation']}"
    )


def main():
    parser = argparse.ArgumentParser(description="LinkedIn post score v3.5 based on 360Brew")
    parser.add_argument("file", help="File with the post text")
    parser.add_argument("--objective", "-o", choices=["authority", "sales", "engagement"],
                        default="authority", help="Post objective (default: authority)")
    parser.add_argument("--lang", "-l", choices=["auto", "pt", "en"], default="auto",
                        help="Post language for matching (default: auto = PT+EN)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--compact", action="store_true", help="1-line output for a pipeline")

    args = parser.parse_args()

    try:
        text = Path(args.file).read_text(encoding='utf-8')
    except FileNotFoundError:
        print(f"Error: file '{args.file}' not found")
        sys.exit(1)

    result = score_post(text, args.objective, args.lang)

    if args.json:
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.compact:
        print_compact(result)
    else:
        print_report(result)


if __name__ == "__main__":
    main()
