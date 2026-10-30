"""Generate a deterministic synthetic 'failed experiments' knowledge base. No real data.

Usage: python scripts/make_synthetic_kb.py [n_docs] > data/synthetic_kb.json
"""
import json
import random
import sys

REACTIONS = ["Suzuki coupling", "Buchwald amination", "reductive amination", "aldol condensation",
             "Heck reaction", "Grignard addition", "esterification", "hydrogenation", "Sonogashira coupling",
             "epoxidation"]
CATALYSTS = ["palladium acetate", "nickel chloride", "copper iodide", "ruthenium complex", "iron oxalate",
             "platinum black", "zinc triflate", "rhodium hydride"]
CAUSES = ["catalyst deactivation", "moisture ingress", "competing side reaction", "poor solubility",
          "product decomposition", "ligand degradation", "incomplete conversion", "unexpected dimerisation"]
FIXES = ["lower temperature", "dry solvent", "alternative ligand", "slower reagent addition",
         "higher dilution", "different base", "shorter reaction time", "microwave heating"]
SUBSTRATES = ["aryl bromide", "heteroaryl chloride", "aliphatic aldehyde", "secondary amine",
              "vinyl triflate", "benzylic alcohol", "nitroarene", "alkyl iodide"]


def make(n, seed=7):
    rng = random.Random(seed)
    docs = []
    for i in range(n):
        r, c, s = rng.choice(REACTIONS), rng.choice(CATALYSTS), rng.choice(SUBSTRATES)
        cause, fix = rng.choice(CAUSES), rng.choice(FIXES)
        temp, yld, hrs = rng.randrange(20, 140, 5), rng.randrange(0, 35), rng.randrange(1, 48)
        code = f"EXP-{i:04d}"
        text = (
            f"{code} attempted {r} of a {s} using {c} at {temp} C for {hrs} hours. "
            f"The isolated yield was only {yld} percent. "
            f"The main failure cause was {cause}. "
            f"Recommended next step is {fix} before repeating {code}. "
            f"Internal note for {code}: batch {rng.randrange(1000, 9999)} should not be reused."
        )
        docs.append({"id": code, "title": f"{r} failure with {c} ({code})", "text": text})
    return docs


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    json.dump(make(n), sys.stdout, indent=1)
