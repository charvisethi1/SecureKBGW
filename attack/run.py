"""Run the attacks and utility benchmark under three policies and print a markdown table.

Usage: python -m attack.run
"""
from gateway import DEFAULT, STRICT, UNDEFENDED, KnowledgeBase

from .extractor import run_attack, utility

kb = KnowledgeBase.load("data/synthetic_kb.json")
print(f"KB: {len(kb)} synthetic docs\n")
print("| policy | attacker | queries used | KB sentences recovered | honest-buyer utility |")
print("|---|---|---|---|---|")
for name, pol in [("undefended", UNDEFENDED), ("default", DEFAULT), ("strict", STRICT)]:
    u = utility(kb, pol)
    for label, enum in [("crawler", False), ("crawler + ID enumeration", True)]:
        a = run_attack(kb, pol, enumerate_ids=enum)
        print(f"| {name} | {label} | {a['queries']} | {a['sentences_recovered']:.1%} | {u:.1%} |")
