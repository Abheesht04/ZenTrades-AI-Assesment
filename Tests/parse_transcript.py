import re

def clean_transcript(input_file, output_file):

    cleaned_lines = []

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:

        line = line.strip()

        # skip empty lines
        if not line:
            continue

        # skip speaker metadata
        if line.startswith("Speaker"):
            continue

        cleaned_lines.append(line)

    cleaned_text = " ".join(cleaned_lines)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    print("Transcript cleaned successfully")


if __name__ == "__main__":

    clean_transcript("transcript.txt", "clean_transcript.txt")
