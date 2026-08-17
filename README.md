# SAHVIA

> **Status: 🚧 In Development**

SAHVIA is a Python-based voice-controlled computer assistant that I am actively building.

The goal is to let a user interact with a computer through natural voice commands instead of relying entirely on a mouse and keyboard.

## Current capabilities

- Voice input using SpeechRecognition
- Neural text-to-speech using Edge TTS
- Local LLM-based command routing through Ollama
- Tool registry and command router
- Browser actions
- Window and browser-tab controls
- Screen capture and OCR
- Screen text detection and mouse interaction
- Short-term conversation/tool memory
- Windows system controls

## Architecture

```text
Voice Input
    ↓
Speech Recognition
    ↓
SAHVIA Command Router
    ↓
Ollama Brain
    ↓
Tool Selection
    ↓
Computer / Browser / Vision Tools
    ↓
Tool Result
    ↓
Voice Response
```

## Tech stack

- Python
- Ollama
- SpeechRecognition
- Edge TTS
- PyAutoGUI
- Pytesseract + Tesseract OCR
- Pillow
- Requests
- Pygame

## Requirements

- Windows
- Python 3.11+
- Ollama installed and running locally
- The configured Ollama model available locally
- Tesseract OCR installed for screen-reading features
- A working microphone and speakers

The current configuration uses:

```text
Ollama: http://localhost:11434
Model: llama3.2:3b
Language: en-IN
```

## Setup

Clone the repository and enter the project directory:

```bash
git clone https://github.com/sakshammishra2112-byte/SAHVIA.git
cd SAHVIA
```

Create a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure Ollama is running and the configured model is available.

Then start SAHVIA:

```bash
python main.py
```

## Development status

This is an active project, not a finished production assistant. I am currently working on:

- improving command reliability
- preventing duplicate command execution
- expanding the tool set
- improving screen understanding
- making multi-step tasks more reliable
- improving the agent loop and error handling

## Notes

The project currently targets Windows because several computer-control tools use Windows-specific behavior.

Do not commit API keys, passwords, tokens, `.env` files, virtual environments, or generated local files.
