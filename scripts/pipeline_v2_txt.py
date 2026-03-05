import whisper
import json
import re
import tkinter as tk
from tkinter import filedialog, messagebox


# ---------------- FILE DIALOG ----------------

def choose_file():

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select Onboarding Input",
        filetypes=[
            ("Audio or Transcript", "*.m4a *.mp3 *.wav *.txt"),
            ("Audio", "*.m4a *.mp3 *.wav"),
            ("Text", "*.txt")
        ]
    )

    return file_path


# ---------------- TRANSCRIPTION ----------------

def transcribe(audio_file):

    print("Loading Whisper model...")
    model = whisper.load_model("small")

    print("Transcribing audio...")
    result = model.transcribe(audio_file)

    return result["text"]


# ---------------- TXT TRANSCRIPT CLEANER ----------------

def load_txt_transcript(file_path):

    cleaned_lines = []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # remove speaker metadata lines
        if line.startswith("Speaker"):
            continue

        cleaned_lines.append(line)

    return " ".join(cleaned_lines)


# ---------------- CHUNKING ----------------

def chunk_text(text, size=80):

    words = text.split()
    chunks = []

    for i in range(0, len(words), size):

        chunk = " ".join(words[i:i+size])

        chunks.append(chunk)

    return chunks


# ---------------- EXTRACTION ----------------

SERVICE_KEYWORDS = [
    "pressure washing",
    "sprinkler",
    "fire alarm",
    "electrical",
    "inspection",
    "maintenance",
    "repair"
]

EMERGENCY_KEYWORDS = [
    "emergency",
    "urgent",
    "sprinkler leak",
    "alarm going off"
]


def extract_updates(chunks):

    update = {
        "company_name": "",
        "business_hours": "",
        "office_address": "",
        "services_supported": [],
        "emergency_definition": [],
        "emergency_routing_rules": "",
        "non_emergency_routing_rules": "",
        "call_transfer_rules": "",
        "integration_constraints": [],
        "after_hours_flow_summary": "",
        "office_hours_flow_summary": "",
        "notes": []
    }

    for chunk in chunks:

        text = chunk.lower()

        for s in SERVICE_KEYWORDS:
            if s in text:
                update["services_supported"].append(s)

        for e in EMERGENCY_KEYWORDS:
            if e in text:
                update["emergency_definition"].append(e)

        if "after hours" in text:
            update["after_hours_flow_summary"] = chunk

        if "transfer" in text or "dispatch" in text:
            update["call_transfer_rules"] = chunk

        phones = re.findall(r"\+?\d[\d\s\-]{8,}\d", chunk)
        if phones:
            update["notes"].append(f"phone detected: {phones}")

    return update


# ---------------- MERGE LOGIC ----------------

def merge_memos(v1, update):

    v2 = v1.copy()

    for key in update:

        if isinstance(update[key], list):

            v2[key] = list(set(v1.get(key, []) + update[key]))

        else:

            if update[key] != "":
                v2[key] = update[key]

    return v2


# ---------------- DIFF ENGINE ----------------

def diff(v1, v2):

    changes = []

    for key in v1:

        if v1[key] != v2[key]:

            changes.append({
                "field": key,
                "before": v1[key],
                "after": v2[key]
            })

    return changes


# ---------------- AGENT SPEC ----------------

def generate_agent_spec(memo, version):

    agent = {
        "agent_name": f"{memo.get('company_name','Company')} Receptionist",
        "voice_style": "professional",

        "key_variables": {
            "business_hours": memo.get("business_hours",""),
            "services": memo.get("services_supported",[]),
            "emergency_definition": memo.get("emergency_definition",[])
        },

        "system_prompt": f"""
You are the receptionist for {memo.get('company_name','the company')}.

BUSINESS HOURS FLOW
- greet caller
- ask purpose
- collect name and phone
- route call
- confirm next steps
- ask if anything else
- close politely

AFTER HOURS FLOW
- greet caller
- ask purpose
- determine emergency
- if emergency collect name, phone, address
- attempt transfer
- if transfer fails reassure caller someone will follow up
""",

        "call_transfer_protocol": memo.get("call_transfer_rules",""),
        "fallback_protocol": "If transfer fails apologize and promise callback.",
        "version": version
    }

    return agent


# ---------------- MAIN PIPELINE ----------------

def main():

    input_file = choose_file()

    if not input_file:
        messagebox.showerror("Error", "No file selected")
        return

    print("Loading transcript...")

    # determine input type
    if input_file.endswith(".txt"):

        transcript = load_txt_transcript(input_file)

    else:

        transcript = transcribe(input_file)

    print("Chunking transcript...")
    chunks = chunk_text(transcript)

    print("Extracting updates...")
    updates = extract_updates(chunks)

    print("Loading v1 memo...")
    with open("account_memo_v1.json") as f:
        memo_v1 = json.load(f)

    print("Merging updates...")
    memo_v2 = merge_memos(memo_v1, updates)

    print("Generating diff...")
    changes = diff(memo_v1, memo_v2)

    agent_v2 = generate_agent_spec(memo_v2, "v2")

    with open("account_memo_v2.json", "w") as f:
        json.dump(memo_v2, f, indent=4)

    with open("agent_spec_v2.json", "w") as f:
        json.dump(agent_v2, f, indent=4)

    with open("changes.json", "w") as f:
        json.dump(changes, f, indent=4)

    print("Pipeline v2 completed successfully")
    messagebox.showinfo("Done", "v2 pipeline finished")


if __name__ == "__main__":
    main()
