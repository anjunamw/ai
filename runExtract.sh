#!/bin/bash

# Array of markdown files to process
files_to_process=("pack1.md" "back1.md" "back2.md" "back3.md" "back4.md" "back5.md" "back6.md" "back7.md")
# "6.md" "7.md" "8.md")

output_dir="output_files"
source_dir="$(dirname "$0")"
report_dir="reports"
pylint_raw_output="$report_dir/pylint_raw.txt"
pylint_markdown_output="$report_dir/pylint_report_$(date +%Y%m%d_%H%M%S).md"


# Process each markdown file
for markdown_file in "${files_to_process[@]}"; do

    processed_markdown_file="${markdown_file%.*}_processed.md"
  
    # 1. Copy the file and make the "_processed" file.
    echo "Copying markdown file: $markdown_file"
    cp "$markdown_file" "$processed_markdown_file"

    # 2. Call the python method that is responsible for reviewing and making the files in "output_files" directory.
    echo "Running python code extraction and file creation: $markdown_file"
    python3 create_files.py "$markdown_file"

    # 3. Remove any leftover backticks and fix filenames, then the backtick strings
     echo "Removing any leftover backticks and fix filenames"
    find "$output_dir" -depth -name '*[\`#]*' -print0 | while IFS= read -r -d $'\0' file; do
        dir=$(dirname "$file")
        base=$(basename "$file")
        new_base=$(echo "$base" | sed -e 's/# //g' -e 's/`/ /g')
        if [[ "$base" != "$new_base" ]]; then
            mv "$file" "$dir/$new_base"
        fi
    done

    # 4. Remove any leftover ```python from files
    echo "Removing leftover backtick strings"
    find "$output_dir" -type f -exec sed -i '' 's/```python//g' {} +

done

# 5. Create a virtual environment in output_files
echo "Creating virtual environment"
python3 -m venv "$output_dir/venv"

# 6. Activate virtual environment
echo "Activating virtual environment"
source "$output_dir/venv/bin/activate"

# # 7. Add any missing files from the current project
# echo "Comparing the directories...."
# compare_script="$source_dir/compareDir.sh"
# if [ -f "$compare_script" ]; then
#     bash "$compare_script"
# else
#     echo "Warning: compareDir.sh not found in the same directory as create_files.sh"
# fi

# 8. Execute requirements.sh script
echo "Installing requirements using requirements.sh"
requirements_script="$source_dir/requirements.sh"
if [ -f "$requirements_script" ]; then
    bash "$requirements_script"
else
    echo "Warning: requirements.sh not found in the same directory as create_files.sh"
fi

# 9. Make the directory for the reports
mkdir -p "$report_dir"

# 10. Run isort
echo "Running isort"
isort "$output_dir" --skip venv > "$report_dir/isort_report_$(date +%Y%m%d_%H%M%S).txt"
echo "isort markdown report created at: $report_dir/isort_report_$(date +%Y%m%d_%H%M%S).txt"

# 11. Run black
echo "Running black"
black "$output_dir" --exclude venv > "$report_dir/black_report_$(date +%Y%m%d_%H%M%S).txt"
echo "black markdown report created at: $report_dir/black_report_$(date +%Y%m%d_%H%M%S).txt"

# 12. Run pylint
echo "Running pylint"
pylint "$output_dir" --exit-zero --rcfile="$source_dir/.pylintrc" > "$pylint_raw_output" 2>&1 || true

# 13. Format pylint output
echo "Formatting pylint output"
python3 "$source_dir/format_pylint.py" "$pylint_raw_output" "$pylint_markdown_output"
echo "pylint markdown report created at: $pylint_markdown_output"

# 14. Deactivate virtual environment
echo "Deactivating virtual environment"
deactivate

# 15. Remove the virtual environment
echo "Removing virtual environment"
rm -rf "$output_dir/venv"

echo "Finished code analysis and cleanup"
