import glob
import sys

from decimal import Decimal
from collections import Counter, defaultdict, OrderedDict

positions = defaultdict(OrderedDict)
results = defaultdict(Counter)

def parse_position(pos, fn):
    if pos == 'y':
        return "yes"
    if pos == 'n':
        return "no"
    if pos == 'a':
        return "abs"
    raise Exception("Invalid position: %s [%s]" % (pos, fn))

for fn in glob.glob(sys.argv[1]):
    with open(fn) as f:
        lines = f.readlines()
        name = None

        for line in lines:
            if line == '---':
                break

        for line in lines:
            if line == "---":
                break

            if line.startswith("%"):
                name = line.split(":")[-1].strip()

            if line.startswith("*"):
                if name is None:
                    raise Exception("No country code found for ballot '%s'" % fn)
                proposal, position = line[1:].split(":")
                proposal = proposal.strip()
                position = parse_position(position.strip(), fn)

                positions[proposal][name] = position
                results[proposal][position] += 1


two_thirds = Decimal('2') / Decimal('3')
half = Decimal('1') / Decimal('2')

for proposal, x in positions.items():
    print("== %s ==\n" % proposal)

    names = []
    vals = []
    for name, val in x.items():
        names.append(name)
        vals.append(val)

    print("{| class='wikitable'")
    print("! %s" % " !! ".join(names))
    print("|-")
    print("| %s" % " || ".join(vals))
    print("|}\n")

    yes = Decimal(results[proposal]['yes'])
    no = Decimal(results[proposal]['no'])
    abstain = Decimal(results[proposal]['abs'])

    total = yes + no

    print("=== Tally ===\n")

    print("{| class='wikitable'")
    print("! Yes !! No !! Abstain")
    print("|-")
    print("| %s || %s || %s" % (yes, no, abstain))
    print("|}\n")

    print("=== Outcome ===")

    if proposal.startswith("SAP"):
        if yes / total > two_thirds:
            print("Motion carries.")
        else:
            print("Motion lapses.")
    else:
        if yes / total > half:
            print("Motion carries.")
        else:
            print("Motion lapses.")
    print()
