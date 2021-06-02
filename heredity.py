import csv
import itertools
import sys

PROBS = {

    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        2: {
            True: 0.65,
            False: 0.35
        },

        1: {
            True: 0.56,
            False: 0.44
        },

        0: {
            True: 0.01,
            False: 0.99
        }
    },

    "mutation": 0.01
}


def main():

    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    names = set(people)
    for have_trait in powerset(names):

        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    normalize(probabilities)

    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):

    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):

    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):

    probability = 1

    for person in people:
        gene_number = 1 if person in one_gene else 2 if person in two_genes else 0
        trait = True if person in have_trait else False

        gene_numb_prop = PROBS['gene'][gene_number]
        trait_prop = PROBS['trait'][gene_number][trait]

        if people[person]['mother'] is None:
            # no parents, use probability distribution
            probability *= gene_numb_prop * trait_prop
        else:
            # info about parents is available
            mother = people[person]['mother']
            father = people[person]['father']
            percentages = {}

            for ppl in [mother, father]:
                number = 1 if ppl in one_gene else 2 if ppl in two_genes else 0
                perc = 0 + PROBS['mutation'] if number == 0 else 0.5 if number == 1 else 1 - PROBS['mutation']
                percentages[ppl] = perc

            if gene_number == 0:
                # 0, none of parents gave gene
                probability *= (1 - percentages[mother]) * (1 - percentages[father])
            elif gene_number == 1:
                # 1, one of parents gave gene
                probability *= (1 - percentages[mother]) * percentages[father] + percentages[mother] * (1 - percentages[father])
            else:
                # 2, both of parents gave gene
                probability *= percentages[mother] * percentages[father]

            probability *= trait_prop

    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):

    for person in probabilities:
        gene_number = 1 if person in one_gene else 2 if person in two_genes else 0
        probabilities[person]["gene"][gene_number] += p
        probabilities[person]["trait"][person in have_trait] += p


def normalize(probabilities):

    normalized = probabilities.copy()
    for person in probabilities:
        for typ in ['gene', 'trait']:
            summed = sum(probabilities[person][typ].values())
            for category in probabilities[person][typ]:
                val = probabilities[person][typ][category]
                normalized_val = val / summed
                normalized[person][typ][category] = normalized_val
    return normalized


if __name__ == "__main__":
    main()