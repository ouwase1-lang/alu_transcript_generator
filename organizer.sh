#!/bin/bash
# organizer.sh - archives grades.csv with a timestamp and logs the action.

ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"
SOURCE="grades.csv"

# Create the archive directory if it does not exist
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR" || { echo "Error: could not create $ARCHIVE_DIR"; exit 1; }
fi

if [ ! -f "$SOURCE" ]; then
    echo "Error: $SOURCE not found in $(pwd)."
    exit 1
fi

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
NEW_NAME="grades_${TIMESTAMP}.csv"

# Archive the file under its new name
if ! mv "$SOURCE" "$ARCHIVE_DIR/$NEW_NAME"; then
    echo "Error: failed to archive $SOURCE."
    exit 1
fi

# Reset the workspace with a fresh, empty grades.csv
: > "$SOURCE"

# Append to the log (accumulates across runs)
echo "[$TIMESTAMP] Original: $SOURCE | Archived as: $ARCHIVE_DIR/$NEW_NAME" >> "$LOG_FILE"

echo "Archived $SOURCE to $ARCHIVE_DIR/$NEW_NAME and created a new empty $SOURCE."
