import json
import os
import whisper
import tkinter as tk
from tkinter import filedialog, messagebox

def transcribe_to_json(file_path):
    print(f"\n--- Loading HIGH ACCURACY Model (Medium) ---")
    # Switch 'base' to 'medium' for a massive jump in quality. 
    # Use 'turbo' if you want speed + accuracy (requires latest whisper update).
    model = whisper.load_model("small") 
    
    print(f"--- Transcribing with Context Hints ---")
    
    # PRO TIP: The 'prompt' helps the AI not mess up specific names or accents
    context_prompt = "Clara AI project, audio transcription, m4a file, technical data."

    try:
        # We specify the language and give it the prompt hint
        result = model.transcribe(
            file_path, 
            language='en', 
            initial_prompt=context_prompt,
            fp16=False # Set to True if you have a GPU/CUDA to make it faster
        )
        
        text = result['text'].strip()

        data = {
            "file_info": {"name": os.path.basename(file_path)},
            "transcription": text
        }

        json_path = os.path.splitext(file_path)[0] + ".json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"--- Success! ---")
        messagebox.showinfo("Done", f"Improved transcription saved to:\n{json_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

def main():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(filetypes=[("Audio", "*.m4a")])
    if file_path:
        transcribe_to_json(file_path)

if __name__ == "__main__":
    main()
