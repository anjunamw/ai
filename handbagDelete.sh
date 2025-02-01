#!/bin/bash

# Check if a filename argument is passed
if [ -z "$1" ]; then
  echo "Usage: $0 <filename>"
  exit 1
fi

# Store the filename
filename="$1"

# Check if the file exists
if [ ! -f "$filename" ]; then
  echo "Error: File '$filename' not found!"
  exit 1
fi

# Remove lines containing '## #####' and save the result back to the file
sed -i '' '/## #####/d' "$filename"

echo "Lines containing '## #####' have been removed from $filename."