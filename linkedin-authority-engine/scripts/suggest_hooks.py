#!/usr/bin/env python3
"""
LinkedIn Hook Suggester - Suggests hooks based on category and objective
Usage: python suggest_hooks.py --category <cat> --objective <obj> [--topic "your topic"] [--seed N]

The types and the category->type mapping mirror skills/hooks/SKILL.md.
"""

import argparse
import random
import re

# Hook library organized by type (subset of skills/hooks/SKILL.md)
HOOKS = {
    "proof_of_work": [
        "I spent ${value} testing {topic}. Here's what I found:",
        "I analyzed {number} {items} over the last {time}. The pattern I found:",
        "I tested {number} {topic} tools. Only {smaller_number} work:",
        "I invested {time} in {topic}. Result: {result}",
        "I lost ${value} by ignoring this about {topic}:",
        "From {before} to {after} in {time}. What changed:",
        "{number} experiments later, here's what I can say about {topic}:",
        "I spent {time} so you don't have to: {topic}",
    ],
    "authority_proof": [
        "What {number} years in {industry} taught me about {topic}:",
        "As a {role}, I found that {topic}:",
        "Leading {number} people, I learned something about {topic}:",
        "After {number} {topic} projects, I can say this:",
        "{number} clients later, the pattern about {topic} is clear:",
        "The mistake I see in 90% of companies about {topic}:",
        "The truth that {number} years of experience showed me:",
    ],
    "transformation": [
        "From {before} to {after} in {time}.",
        "It used to be {situation_before}. Today {situation_after}.",
        "{time} ago, I {before}. Now I {after}.",
        "{number}% growth in {time}. Here's how:",
        "From zero to {result} in {time}. The path:",
        "Before: {before}. After: {after}. The difference:",
    ],
    "contrarian": [
        "Everyone says {common_belief}. I did it differently:",
        "Unpopular opinion: {opinion}",
        "The most common advice about {topic} is wrong.",
        "Stop {common_mistake}. Start {alternative}.",
        "95% of people do {topic} wrong. Here's why:",
        "You should NOT {common_advice}. Do this instead:",
        "{common_belief}? Wrong. The truth:",
    ],
    "confession": [
        "I lost ${value} because of {mistake}.",
        "My biggest mistake in {topic}:",
        "I got fired. And it was the best thing that happened.",
        "I failed {number} times at {topic}. What I learned:",
        "The mistake that almost destroyed {result}:",
        "I'll admit it: I was wrong about {topic}.",
    ],
    "curiosity": [
        "Did you know that {statistic}?",
        "{number} mistakes you're making in {topic}:",
        "The easiest way to {objective}:",
        "What nobody tells you about {topic}:",
        "Why {common_practice} no longer works:",
        "The secret to {result} in {time}:",
    ],
    "story": [
        "I'll never forget when {moment}.",
        "In {year}, I was {situation}. Today...",
        "My mentor told me something that changed everything:",
        "One call changed my career. Here's what happened:",
        "The day {event} taught me about {topic}:",
    ],
    # Highest Saves Potential (the 30%-weight dimension in scoring). See hooks.md §8.
    "lists_frameworks": [
        "My {number}-step framework for {result}:",
        "{number} lessons from {experience}:",
        "My {number}-item checklist for {objective}:",
        "The {number} principles that changed my {result}:",
        "{number} non-negotiable rules in {topic}:",
        "The {number}-step system I use for {objective}:",
        "My {topic} template (copy-paste ready):",
        "{number} red flags in {topic}:",
    ],
}

# Category -> recommended hook types mapping (mirrors hooks.md)
CATEGORY_HOOKS = {
    "career_lesson": ["story", "authority_proof", "transformation"],
    "achievement": ["proof_of_work", "transformation", "authority_proof"],
    "failure": ["confession", "story", "proof_of_work"],
    "debunk": ["contrarian", "authority_proof", "curiosity"],
    "practical_tip": ["proof_of_work", "lists_frameworks", "curiosity"],
    "opinion": ["contrarian", "authority_proof"],
    "behind_the_scenes": ["story", "confession", "proof_of_work"],
    "other": ["curiosity", "proof_of_work", "lists_frameworks"],
}

# Objective -> adjustments mapping (lists_frameworks drives saves for any objective)
OBJECTIVE_BONUS = {
    "authority": ["authority_proof", "proof_of_work", "lists_frameworks"],
    "sales": ["transformation", "proof_of_work", "lists_frameworks"],
    "engagement": ["contrarian", "curiosity", "confession"],
}


def get_recommended_types(category: str, objective: str) -> list:
    """Returns recommended hook types for category + objective"""
    base_types = CATEGORY_HOOKS.get(category, CATEGORY_HOOKS["other"])
    bonus_types = OBJECTIVE_BONUS.get(objective, [])

    all_types = []
    for t in base_types:
        if t in bonus_types:
            all_types.insert(0, t)  # Priority: appears in both
        else:
            all_types.append(t)

    for t in bonus_types:
        if t not in all_types:
            all_types.append(t)

    return all_types[:4]  # Top 4


def fill_placeholders(hook: str, topic: str) -> str:
    """Fills {topic} with the real topic and the remaining placeholders with [markers]."""
    hook = hook.replace("{topic}", topic)
    hook = hook.replace("{number}", "X").replace("{smaller_number}", "X")
    return re.sub(r"\{(\w+)\}", lambda m: "[" + m.group(1).replace("_", " ") + "]", hook)


def suggest_hooks(category: str, objective: str, topic: str = "[your topic]", count: int = 5) -> list:
    """Generates hook suggestions"""
    recommended_types = get_recommended_types(category, objective)
    suggestions = []

    for hook_type in recommended_types:
        hooks = HOOKS.get(hook_type, [])
        selected = random.sample(hooks, min(2, len(hooks)))
        for hook in selected:
            suggestions.append({
                "type": hook_type.replace("_", " ").title(),
                "template": hook,
                "example": fill_placeholders(hook, topic),
            })

    return suggestions[:count]


def print_suggestions(suggestions: list, category: str, objective: str, topic: str):
    """Prints formatted suggestions"""
    print("\n" + "=" * 60)
    print("HOOK SUGGESTIONS - LinkedIn 360Brew")
    print("=" * 60)

    print("\nConfiguration:")
    print(f"   - Category: {category.replace('_', ' ').title()}")
    print(f"   - Objective: {objective.title()}")
    print(f"   - Topic: {topic}")

    print("\n" + "-" * 60)
    print("RECOMMENDED HOOKS:")
    print("-" * 60)

    for i, sug in enumerate(suggestions, 1):
        print(f"\n{i}. [{sug['type']}]")
        print(f"   Template: {sug['template']}")
        print(f"   Example:  {sug['example']}")

    print("\n" + "-" * 60)
    print("HOOKS TO AVOID (punished by 360Brew):")
    print("   X 'What do you think?'")
    print("   X 'Agree?'")
    print("   X 'Good morning, LinkedIn!'")
    print("   X 'Thought of the day'")
    print("   X Generic clickbait with no proof")
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Suggest hooks for LinkedIn posts")
    parser.add_argument("--category", "-c", required=True,
                        choices=["career_lesson", "achievement", "failure",
                                 "debunk", "practical_tip", "opinion",
                                 "behind_the_scenes", "other"],
                        help="Post category")
    parser.add_argument("--objective", "-o", required=True,
                        choices=["authority", "sales", "engagement"],
                        help="Post objective")
    parser.add_argument("--topic", "-t", default="[your topic]",
                        help="Specific topic of the post")
    parser.add_argument("--count", "-n", type=int, default=5,
                        help="Number of suggestions (default: 5; present 3 to the user)")
    parser.add_argument("--seed", type=int, default=None,
                        help="Seed for reproducible output")
    parser.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    suggestions = suggest_hooks(args.category, args.objective, args.topic, args.count)

    if args.json:
        import json
        print(json.dumps(suggestions, ensure_ascii=False, indent=2))
    else:
        print_suggestions(suggestions, args.category, args.objective, args.topic)


if __name__ == "__main__":
    main()
