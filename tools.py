import os
import subprocess

def list_files(directory="."):
    """Lists files in the given directory."""
    try:
        files = os.listdir(directory)
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {e}"

def read_file(filepath):
    """Reads the content of a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def write_file(filepath, content):
    """Writes content to a file."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True) if os.path.dirname(filepath) else None
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {e}"

def execute_command(command):
    """Executes a shell command and returns the output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
        output = result.stdout
        error = result.stderr
        if result.returncode == 0:
            return f"Command executed successfully.\nOutput:\n{output}"
        else:
            return f"Command failed with return code {result.returncode}.\nError:\n{error}\nOutput:\n{output}"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds."
    except Exception as e:
        return f"Error executing command: {e}"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Lists files in a given directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "description": "The directory to list."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "The path to the file."}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Writes content to a file. Use this for creating scripts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "The path to save the file."},
                    "content": {"type": "string", "description": "The file content."}
                },
                "required": ["filepath", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_command",
            "description": "Executes a shell command. IMPORTANT: This is NON-INTERACTIVE. The command must finish automatically or use piped input (e.g. 'echo 1 | python script.py'). Do NOT run commands that wait for user input indefinitely.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The command to execute."}
                },
                "required": ["command"]
            }
        }
    }
]

TOOL_MAP = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "execute_command": execute_command
}

