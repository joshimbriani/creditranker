import csv
import random
import sys

def run():
    method = ""
    while method.lower() != "f" and method.lower() != "q":
        method = input("[F]ull or [Q]uick rank:   ")

    if method.lower() == "f":
        full_rank()
    else:
        quick_rank()

def quick_rank():
    print("Starting quick rank")
    credits = get_input_data()

def full_rank():
    print("Starting full rank")
    credits = get_input_data()
    credits = credits[0:7]
    matchups = generate_matchups(credits)
    results = {}
    populate_results(results, credits)
    evaluate_matchups(results, matchups)
    sorted_results = score_results(results)
    print("Scoring complete")
    export_results(sorted_results, credits)

def generate_matchups(credits):
    print("Generating head to head pairs")
    matchups = []
    for coaster1_index in range(len(credits)):
        for coaster2_index in range(coaster1_index+1, len(credits)):
            matchups.append((credits[coaster1_index], credits[coaster2_index]))

    random.shuffle(matchups)
    return matchups

def populate_results(results, credits):
    for credit in credits:
        results[credit[0]] = []

def evaluate_matchups(results, matchups):
    for matchup in matchups:
        i = ""
        while i.lower() != "a" and i.lower() != "d":
            i = input(matchup[0][0] + " [a]         or              " + matchup[1][0] + " [d]:    ")

        if i.lower() == "a":
            # A won the matchup
            results[matchup[0][0]].append(matchup[1][0])
        else:
            # D won the matchup
            results[matchup[1][0]].append(matchup[0][0])

def score_results(results):
    sorted_results = sorted(results.items(), key=lambda i:-len(i[1]))
    return sorted_results

def export_results(sorted_results, credits):
    action = ""
    while action.lower() != "q":
        while action.lower() != "e" and action.lower() != "p" and action.lower() != "d" and action.lower() != "q":
            action = input("[E]xport rankings to csv, [P]rint rankings, [D]etails of running, [Q]uit:  ")

        if action == "e":
            export_rankings(sorted_results)
        elif action == "p":
            print_rankings(sorted_results)
        elif action == "d":
            details_rankings(sorted_results, credits)
        else:
            sys.exit(0)

        action = ""

def export_rankings(results):
    with open('results.csv', mode='w') as results_file:
        results_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for result in results:
            results_writer.writerow([result[0], len(result[1]), ";".join(result[1])])

        print("Results written")

def print_rankings(results):
    for result in results:
        print("Coaster ", result[0], " won ", len(result[1]), " of its matchups")

def details_rankings(results, credits):
    cred_names = [x[0] for x in credits]
    for result in results:
        victories = set(result[1])
        victories.add(result[0])
        losses = list(set(cred_names) - victories)
        print("Coaster ", result[0], " won ", len(result[1]), " of its matchups")
        print("     Over: ", (", ".join(result[1]) if len(result[1]) > 0 else "None"))
        print("     Lost to: ", (", ".join(losses) if len(losses) > 0 else "None"))

def get_input_data():
    with open('credits.csv') as credit_file:
        readCSV = csv.reader(credit_file, delimiter=',')
        credits = []
        for row in readCSV:
            credits.append(row)

        return credits

if __name__ == "__main__":
    run()