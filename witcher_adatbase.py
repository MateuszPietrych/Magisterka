import os
import re
import html
from pathlib import Path

def extract_label_value_pairs(text):
    pairs = []
    decoded = html.unescape(text)
    data_blocks = re.findall(r"<data.*?>(.*?)</data>", decoded, re.DOTALL)
    for block in data_blocks:
        label_match = re.search(r"<label>(.*?)</label>", block)
        value_match = re.search(r"<format>(.*?)</format>", block) or \
                      re.search(r"<default>(.*?)</default>", block)
        if label_match and value_match:
            label = label_match.group(1).strip()
            value = value_match.group(1).strip()
            if value:  # ✅ skip empty values
                pairs.append((label, value))
    return pairs


def clean_article_text(raw_lines):
    text = []
    for line in raw_lines:
        decoded = html.unescape(line)
        cleaned = re.sub(r"<[^>]+>", "", decoded).strip()
        # Skip "standalone labels" like "Head of State", "Religion", etc.
        if cleaned and not re.match(r"^[A-Z][a-zA-Z\s()\"-]+:?$", cleaned):
            text.append(cleaned)
    return text

def combine_processed_files(input_folder_path, combined_output_path):
    input_folder = Path(input_folder_path)
    with open(combined_output_path, 'w', encoding='utf-8') as combined_file:
        for file in sorted(input_folder.glob("wiki_*")):
            if file.is_file():
                buffer = []
                inside_doc = False
                with open(file, 'r', encoding='utf-8') as infile:
                    for line in infile:
                        if line.startswith("<doc "):
                            inside_doc = True
                            buffer = []
                            continue
                        elif line.startswith("</doc>"):
                            inside_doc = False
                            content = ''.join(buffer)
                            pairs = extract_label_value_pairs(content)
                            text_lines = clean_article_text(buffer)

                            for label, value in pairs:
                                combined_file.write(f"{label}: {value}\n")
                            if pairs:
                                combined_file.write("\n")

                            for text in text_lines:
                                combined_file.write(text + "\n")

                            combined_file.write("\n" + "-" * 80 + "\n")
                            continue

                        if inside_doc:
                            buffer.append(line)

# Example usage
input_folder = "input"  # e.g. "./data"
output_file = "combined_output.txt"
combine_processed_files(input_folder, output_file)
