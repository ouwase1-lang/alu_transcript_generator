import csv
import sys
import os

PASS_MARK = 50.0


def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ").strip()

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    if os.path.getsize(filename) == 0:
        print(f"Error: The file '{filename}' is empty. Add grade records and try again.")
        sys.exit(1)

    required = ['assignment', 'group', 'score', 'weight']
    assignments = []
    bad_rows = 0

    try:
        with open(filename, mode='r', encoding='utf-8-sig', newline='') as file:
            reader = csv.DictReader(file)
            if reader.fieldnames is None:
                print(f"Error: The file '{filename}' has no header row.")
                sys.exit(1)
            reader.fieldnames = [h.strip().lower() for h in reader.fieldnames]
            missing = [c for c in required if c not in reader.fieldnames]
            if missing:
                print(f"Error: Missing required column(s): {', '.join(missing)}.")
                print("The header must be: assignment,group,score,weight")
                sys.exit(1)

            for line_no, row in enumerate(reader, start=2):
                values = [(row[c] or '').strip() for c in required]
                # Skip completely blank rows silently
                if not any(values):
                    continue
                name, group, score_text, weight_text = values
                if not name or not group or not score_text or not weight_text:
                    print(f"Warning: line {line_no} skipped - it has missing fields.")
                    bad_rows += 1
                    continue
                if group.lower() not in ('formative', 'summative'):
                    print(f"Warning: line {line_no} skipped - group '{group}' "
                          "must be Formative or Summative.")
                    bad_rows += 1
                    continue
                try:
                    # Convert numeric fields to floats for calculations
                    score = float(score_text)
                    weight = float(weight_text)
                except ValueError:
                    print(f"Warning: line {line_no} skipped - score and weight must be numbers.")
                    bad_rows += 1
                    continue
                assignments.append({
                    'assignment': name,
                    'group': group,
                    'score': score,
                    'weight': weight
                })
    except UnicodeDecodeError:
        print(f"Error: '{filename}' is not a readable text/CSV file.")
        sys.exit(1)
    except (OSError, csv.Error) as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    if bad_rows:
        print(f"{bad_rows} invalid row(s) were skipped.")
    if not assignments:
        print("Error: No valid assignment records were found in the file.")
        sys.exit(1)
    return assignments


def validate_scores(data):
    """All scores must be between 0 and 100."""
    valid = True
    for a in data:
        if not 0 <= a['score'] <= 100:
            print(f"Error: score for '{a['assignment']}' is {a['score']:g}; it must be between 0 and 100.")
            valid = False
    return valid


def validate_weights(data):
    """Total = 100, Summative = 40, Formative = 60."""
    total = sum(a['weight'] for a in data)
    formative = sum(a['weight'] for a in data if a['group'].strip().lower() == 'formative')
    summative = sum(a['weight'] for a in data if a['group'].strip().lower() == 'summative')
    valid = True
    if abs(total - 100) > 1e-9:
        print(f"Error: total weight is {total:g}, expected 100.")
        valid = False
    if abs(summative - 40) > 1e-9:
        print(f"Error: Summative weight is {summative:g}, expected 40.")
        valid = False
    if abs(formative - 60) > 1e-9:
        print(f"Error: Formative weight is {formative:g}, expected 60.")
        valid = False
    return valid


def evaluate_grades(data):
    """
    Validates the data, computes the final grade and GPA, decides
    PASSED/FAILED and lists assignments eligible for resubmission.
    """
    print("\n--- Processing Grades ---")

    # a) and b) validation
    scores_ok = validate_scores(data)
    weights_ok = validate_weights(data)
    if not (scores_ok and weights_ok):
        print("\nValidation failed. Please correct the CSV file and try again.")
        sys.exit(1)

    # c) weighted totals per category and overall
    totals = {}
    for group, category_weight in (('formative', 60), ('summative', 40)):
        earned = sum(a['score'] * a['weight'] / 100
                     for a in data if a['group'].strip().lower() == group)
        totals[group] = {'earned': earned, 'percent': earned / category_weight * 100}

    total_grade = totals['formative']['earned'] + totals['summative']['earned']
    gpa = (total_grade / 100) * 5.0

    # d) pass only if >= 50% in BOTH categories
    passed = all(t['percent'] >= PASS_MARK for t in totals.values())

    # e) failed formative assignments with the highest weight
    failed_formative = [a for a in data
                        if a['group'].strip().lower() == 'formative' and a['score'] < PASS_MARK]
    resubmit = []
    if failed_formative:
        highest = max(a['weight'] for a in failed_formative)
        resubmit = [a for a in failed_formative if a['weight'] == highest]

    # f) report
    print(f"Formative: {totals['formative']['earned']:.2f}/60 ({totals['formative']['percent']:.1f}%)")
    print(f"Summative: {totals['summative']['earned']:.2f}/40 ({totals['summative']['percent']:.1f}%)")
    print(f"Total Grade: {total_grade:.2f}/100")
    print(f"GPA: {gpa:.2f}")
    print(f"Final Status: {'PASSED' if passed else 'FAILED'}")

    if resubmit:
        print("\nEligible for resubmission:")
        for a in resubmit:
            print(f"  - {a['assignment']} (score {a['score']:g}, weight {a['weight']:g})")
    else:
        print("\nNo assignments eligible for resubmission.")


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()

    # 2. Process the features
    evaluate_grades(course_data)
