import os
import re
import sys
import shutil

def extract_code_blocks(markdown_file):
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    code_blocks = []
    pattern = re.compile(r'```(?:python)?\n(.*?)\n```', re.DOTALL)
    matches = pattern.finditer(content)

    for match in matches:
        code = match.group(1)
        filename_match = re.search(r'^[ \t]*#[ \t]*(.*?)(?:\n|$)', code, re.MULTILINE)
        filename = filename_match.group(1).strip() if filename_match else None
        if filename:
          code_blocks.append((filename, code, match.group(0)))
        else:
          print(f"Warning: skipping a code block without a filename at position {match.start()}")
    return code_blocks, content

def create_files(code_blocks, output_dir='output_files'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename, code, _ in code_blocks:
        filepath = os.path.join(output_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            print(f"Created file: {filepath}")
        except Exception as e:
            print(f"Error creating file: {filepath}, Error: {e}")

def remove_processed_code_blocks(content, code_blocks, processed_markdown_file):
    for _, _, full_match in reversed(code_blocks):
        content = content.replace(full_match, '', 1)

    with open(processed_markdown_file, 'w', encoding='utf-8') as f:
        f.write(content)

def copy_markdown_file(markdown_file, processed_markdown_file):
    try:
        shutil.copyfile(markdown_file, processed_markdown_file)
        print(f"Created copy of markdown file: {processed_markdown_file}")
    except Exception as e:
        print(f"Error copying markdown file: {markdown_file}, Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <markdown_file>")
        sys.exit(1)

    markdown_file = sys.argv[1]
    if not os.path.exists(markdown_file):
        print(f"Error: Markdown file '{markdown_file}' not found.")
        sys.exit(1)

    processed_markdown_file = os.path.splitext(markdown_file)[0] + "_processed.md"
    copy_markdown_file(markdown_file, processed_markdown_file)

    code_blocks, original_content = extract_code_blocks(markdown_file)
    create_files(code_blocks)
    remove_processed_code_blocks(original_content, code_blocks, processed_markdown_file)

    print("Finished processing, files can be found in output_files directory and a copy of the markdown can be found in the same directory")