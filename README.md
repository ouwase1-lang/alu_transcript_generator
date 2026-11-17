# ALU Transcript Generator

Lab 2 - Introduction to Python Programming and Databases (BSE Year 1, Trimester 2)
African Leadership University

A Python application that works out a student's final academic standing from a CSV file
of course grades, plus a Bash script that archives the grade file after each batch.

## Files

| File | Purpose |
|------|---------|
| `grade-evaluator.py` | Validates grades and weights, calculates GPA, decides PASSED/FAILED and lists resubmission options |
| `organizer.sh` | Archives `grades.csv` with a timestamp, resets the workspace and logs the action |
| `grades.csv` | Sample grade data (`assignment,group,score,weight`) |

## Grade Evaluator

Run:

```bash
python3 grade-evaluator.py
```

Enter the CSV file name when prompted (for example `grades.csv`).

### CSV format

```
assignment,group,score,weight
Quiz,Formative,85,20
Midterm Project - Simple Calculator,Summative,70,20
```

`group` must be `Formative` or `Summative`.

### What it does

1. **Score validation** - every score must be between 0 and 100.
2. **Weight validation** - all weights must total exactly 100, Summative exactly 40 and Formative exactly 60.
3. **GPA** - `GPA = (Total Grade / 100) * 5.0`, where Total Grade is the sum of `score * weight / 100`.
4. **Pass/Fail** - the student is PASSED only with at least 50% in both the Formative and Summative categories; otherwise FAILED.
5. **Resubmission** - among failed Formative assignments (score below 50), the one(s) with the highest weight are eligible. If several share that highest weight, all are listed.

### Error handling

The program prints a clear message and exits cleanly (no crash) for: a missing file, an empty file,
a missing header or required column, blank rows (ignored), rows with missing fields, non-numeric
scores or weights, an unknown group, scores outside 0-100, and weights that do not add up correctly.

### Example output (`grades.csv`)

```
Formative: 34.00/60 (56.7%)
Summative: 26.00/40 (65.0%)
Total Grade: 60.00/100
GPA: 3.00
Final Status: PASSED

Eligible for resubmission:
  - Group Exercise (score 40, weight 20)
  - Functions and Debugging Lab (score 45, weight 20)
```

## Organizer Script

Run:

```bash
chmod +x organizer.sh
./organizer.sh
```

Each run:

1. Creates the `archive/` directory if it does not exist.
2. Moves `grades.csv` into `archive/` as `grades_YYYYMMDD-HHMMSS.csv`.
3. Creates a new, empty `grades.csv` in the current directory.
4. Appends a line (timestamp, original filename, archived filename) to `organizer.log`. The log accumulates across runs.

If `grades.csv` is missing, the script prints an error and exits without changing anything.

## Requirements

Python 3 and Bash. No external packages are needed.
