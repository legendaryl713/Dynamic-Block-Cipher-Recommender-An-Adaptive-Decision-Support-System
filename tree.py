#!/usr/bin/env python3

import csv


def load_table(file_path):
    """Load the implementation usage table from a CSV file and validate its structure."""
    try:
        with open(file_path, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            ciphers = [row for row in reader]

        # Validate structure
        required_columns = [
            "Cipher", "Speed", "Security Level", "Memory Usage",
            "Hardware Compatibility", "Energy Efficiency"
        ]
        for col in required_columns:
            if col not in ciphers[0]:
                raise ValueError(f"Missing required column: {col}")
        print("CSV structure validated successfully.")
        print("Sample row from CSV:", ciphers[0])  # Debugging
        return ciphers
    except Exception as e:
        print(f"Error loading or validating CSV: {e}")
        return []


def normalize_value(attribute, value):
    """Normalize user input to match CSV data."""
    mappings = {
        "Security Level": {
            "high": ["high", "very high"],
            "medium": ["medium"],
            "low": ["low"]
        },
        "Speed": {
            "high": ["high"],
            "medium": ["medium"],
            "low": ["low"]
        },
        "Memory Usage": {
            "high": ["high"],
            "medium": ["medium"],
            "low": ["low"]
        },
        "Hardware Compatibility": {
            "high": ["yes"],
            "low": ["no"]
        },
        "Energy Efficiency": {
            "high": ["high"],
            "medium": ["medium"],
            "low": ["low"]
        }
    }
    if attribute in mappings and value.lower() in mappings[attribute]:
        return mappings[attribute][value.lower()]
    return [value.lower()]


def ask_question(question, options=None):
    """Ask the user a question and validate their response."""
    while True:
        if options:
            print(f"{question} (Options: {', '.join(options)})")
        else:
            print(f"{question} (yes/no/I don't know)")

        response = input("> ").strip().lower()

        # Validation for yes/no/I don't know
        if not options and response in ["yes", "no", "i don't know"]:
            return response

        # Validation for multiple-choice questions
        if options and response in [opt.lower() for opt in options]:
            return response

        # If input is invalid, prompt again
        print("Invalid input. Please try again.")


def score_ciphers(ciphers, answers):
    """Score ciphers based on user answers."""
    scores = {cipher["Cipher"]: 0 for cipher in ciphers}  # Initialize scores

    # Define scoring weights
    exact_match_score = 3
    weak_match_score = 1
    opposite_match_score = -2

    for cipher in ciphers:
        for attribute, value in answers.items():
            if value == "unknown":  # Skip scoring for "I don't know" answers
                continue

            normalized_values = normalize_value(attribute, value)
            cipher_value = cipher[attribute].strip().lower()

            if cipher_value in normalized_values:
                scores[cipher["Cipher"]] += exact_match_score  # Exact match
            elif value.lower() == "high" and cipher_value == "medium":  # Weak match example
                scores[cipher["Cipher"]] += weak_match_score
            elif value.lower() == "low" and cipher_value == "high":  # Opposite match example
                scores[cipher["Cipher"]] += opposite_match_score

    return scores


def main():
    # Load implementation usage table
    table_path = "block_cipher_implementation_usage.csv"
    ciphers = load_table(table_path)
    if not ciphers:
        print("Unable to load or validate the CSV file. Exiting.")
        return

    # Define questions and corresponding attributes
    questions = [
        {"question": "Is high security a priority?", "attribute": "Security Level"},
        {"question": "Is speed critical for your use case?", "attribute": "Speed"},
        {"question": "Do you need low memory consumption?", "attribute": "Memory Usage"},
        {"question": "Does your system support hardware acceleration?", "attribute": "Hardware Compatibility"},
        {"question": "Is low energy consumption required?", "attribute": "Energy Efficiency"}
    ]

    # Collect user answers
    print("Welcome to the Block Cipher Decision Tree!")
    print("Answer the following questions to find the best cipher for your needs.")

    user_answers = {}
    for q in questions:
        answer = ask_question(q["question"])
        user_answers[q["attribute"]] = {
            "yes": "High",
            "no": "Low",
            "i don't know": "unknown"
        }.get(answer, answer)

    print("\nCollected User Answers:")
    print(user_answers)

    # Score ciphers based on answers
    scores = score_ciphers(ciphers, user_answers)

    # Sort and display top 2 ciphers
    # Sort and display top 2 ciphers
    sorted_ciphers = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print("\nRecommended Ciphers (Top 2):")
    for cipher, score in sorted_ciphers[:2]:
        explanation = next(
            (c.get("Explanation", "No explanation available") for c in ciphers if c["Cipher"] == cipher),
            "No explanation available"
        )
        print(f"- {cipher}: Score {score}. {explanation}")


if __name__ == "__main__":
    main()