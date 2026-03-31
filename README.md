# Cuantox-AI 🤖

Cuantox-AI is a powerful, agentic AI coding companion powered by **Minimax-M2.5** via the NVIDIA API. It's designed to help you write, debug, and test code directly from your terminal with a beautiful and interactive interface.

## 🚀 Features

- **Agentic Tool Calling**: Cuantox-AI can list files, read code, and write new files autonomously.
- **Interactive Execution**: Run your Python scripts or shell commands directly from the chat.
- **Safety First**: Every command execution requires your explicit confirmation (`y/n`).
- **Auto-Fix Loop**: If a command fails or returns an error, Cuantox-AI automatically receives the output and attempts to fix the code for you.
- **Modern UI**: Styled with `rich` for a premium, color-coded terminal experience with live streaming and status animations.
- **Windows Optimized**: Fully compatible with Windows shell syntax and paths.

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/cuantox/cuantox-ai.git
   cd cuantox-ai
   ```

2. **Install dependencies**:
   ```bash
   pip install openai rich prompt_toolkit
   ```

3. **Set up your API Key**:
   Set the `NVIDIA_API_KEY` environment variable:
   ```powershell
   # Windows (PowerShell)
   $env:NVIDIA_API_KEY="your_api_key_here"
   
   # Linux/Mac
   export NVIDIA_API_KEY="your_api_key_here"
   ```

## 🔑 How to get an API Key

1. Go to [NVIDIA Build - Minimax M2.5](https://build.nvidia.com/minimaxai/minimax-m2.5).
2. Click on the **"View Code"** button.
3. Click on **"Generate API Key"**.
4. Copy your key and save it securely!

## 📖 Usage

Run the tool using:
```bash
python main.py
```

### Example Commands:
- "Create a web scraper in scraper.py and run it to test."
- "Explain how the current project works by reading the files."
- "Fix the bug in my calculator.py file."

## ⚠️ Requirements

- Python 3.8+
- An active NVIDIA API Key

## 📄 License

This project is licensed under the MIT License.
