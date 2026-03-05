import json
import tkinter as tk
from tkinter import filedialog, messagebox


def load_file():
    file_path = filedialog.askopenfilename(
        title="Select Transcript File",
        filetypes=[
            ("Transcript Files", "*.json *.txt"),
            ("JSON Files", "*.json"),
            ("Text Files", "*.txt")
        ]
    )

    if not file_path:
        return

    try:
        if file_path.endswith(".json"):
            transcript = load_json(file_path)

        elif file_path.endswith(".txt"):
            transcript = load_txt(file_path)

        else:
            messagebox.showerror("Error", "Unsupported file type")
            return

        if not transcript:
            messagebox.showerror("Error", "Transcript is empty")
            return

        chunks = chunk_transcript(transcript)

        display_chunks(chunks)

    except Exception as e:
        messagebox.showerror("Error", str(e))


def load_json(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("transcription", "")


def load_txt(file_path):

    cleaned_lines = []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # skip speaker metadata
        if line.startswith("Speaker"):
            continue

        cleaned_lines.append(line)

    return " ".join(cleaned_lines)


def chunk_transcript(text, chunk_size=80):

    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):

        chunk = " ".join(words[i:i + chunk_size])

        chunks.append(chunk)

    return chunks


def display_chunks(chunks):

    text_box.delete("1.0", tk.END)

    for i, chunk in enumerate(chunks):

        text_box.insert(tk.END, f"\n--- CHUNK {i+1} ---\n")

        text_box.insert(tk.END, chunk + "\n")


def save_chunks():

    content = text_box.get("1.0", tk.END)

    save_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text File", "*.txt")]
    )

    if save_path:

        with open(save_path, "w", encoding="utf-8") as f:

            f.write(content)

        messagebox.showinfo("Saved", "Chunks saved successfully")


# GUI Setup
root = tk.Tk()
root.title("Transcript Chunker")
root.geometry("900x600")

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

load_button = tk.Button(button_frame, text="Load Transcript (JSON/TXT)", command=load_file)
load_button.pack(side="left", padx=10)

save_button = tk.Button(button_frame, text="Save Chunks", command=save_chunks)
save_button.pack(side="left", padx=10)

text_box = tk.Text(root, wrap="word")
text_box.pack(expand=True, fill="both")

root.mainloop()
