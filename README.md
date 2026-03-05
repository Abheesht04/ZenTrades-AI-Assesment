\# Clara AI Automation Assignment



\## Overview

This project converts demo and onboarding call transcripts into

structured Retell agent configurations.



Pipeline A:

Demo call → account memo v1 → agent spec v1



Pipeline B:

Onboarding call → updated memo v2 → updated agent spec → changelog



\## Architecture



audio / transcript

        ↓

text extraction

        ↓

chunking

        ↓

information extraction

        ↓

account memo

        ↓

agent configuration

        ↓

version diff



\## How to Run



1\. Generate v1



python text\_extraction.py

python chunk.py

python analyzer.py

python agent\_generator.py



2\. Generate v2



python pipeline\_v2.py



\## Output Files



outputs/accounts/account\_001/v1

outputs/accounts/account\_001/v2



changelog/changes.json







Credits \& References

Project Context



This repository was developed as part of the Clara AI Automation Assignment, which focuses on converting customer demo and onboarding conversations into structured Retell AI agent configurations.



OpenAI Whisper (Speech-to-Text)



Used for converting demo and onboarding call audio into transcripts.

Repo:https://github.com/openai/whisper

paper:https://cdn.openai.com/papers/whisper.pdf


PyTorch

Deep learning framework used by Whisper for model inference.

Website:https://pytorch.org/

repo:https://github.com/pytorch/pytorch



NumPy

Used internally by Whisper and PyTorch for numerical computations.

Website:https://numpy.org/

Repo:https://github.com/numpy/numpy



FFmpeg

Used for decoding audio files such as .m4a, .wav, and .mp3.



Website:https://ffmpeg.org/



Python Tkinter

Used for creating simple GUI file dialogs for selecting audio/transcript files.

Docs: https://docs.python.org/3/library/tkinter.html



tqdm

Used internally by Whisper for progress bars during transcription.



Repo:https://github.com/tqdm/tqdm

