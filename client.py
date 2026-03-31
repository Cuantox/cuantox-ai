import os
import platform
import json
from openai import OpenAI
from tools import TOOLS

class CuantoxClient:
    def __init__(self, api_key=None, base_url="https://integrate.api.nvidia.com/v1", model="minimaxai/minimax-m2.5"):
        self.api_key = api_key or os.getenv("NVIDIA_API_KEY")
        if not self.api_key:
            raise ValueError("API Key not found. Set NVIDIA_API_KEY environment variable or pass it to the constructor.")
        self.client = OpenAI(base_url=base_url, api_key=self.api_key)
        self.model = model
        os_info = platform.system()
        self.history = [
            {"role": "system", "content": f"You are Cuantox-AI, a powerful AI coding assistant on {os_info}. "
                                         f"IMPORTANT: 'execute_command' is NON-INTERACTIVE. "
                                         f"You MUST use piped input (e.g. 'echo 1 | python script.py') for any command that needs user input. "
                                         f"Avoid '<< EOF' (use 'echo line1 & echo line2 | python' style or write a test script). "
                                         f"Prefer 'python' over 'python3' on Windows. Use tools when needed."}
        ]

    def chat_stream(self, message=None, tool_results=None):
        if message:
            self.history.append({"role": "user", "content": message})
        if tool_results:
            for result in tool_results:
                self.history.append(result)
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                temperature=0.1, # Lower temperature for better tool usage
                top_p=0.95,
                max_tokens=8192,
                stream=True,
                tools=TOOLS,
                tool_choice="auto"
            )
            
            full_response = ""
            tool_calls = []
            
            for chunk in completion:
                if not getattr(chunk, "choices", None):
                    continue
                
                delta = chunk.choices[0].delta
                
                # Handle Tool Calls
                if hasattr(delta, 'tool_calls') and delta.tool_calls:
                    for tc_chunk in delta.tool_calls:
                        if len(tool_calls) <= tc_chunk.index:
                            tool_calls.append({
                                "id": tc_chunk.id,
                                "type": "function",
                                "function": {"name": "", "arguments": ""}
                            })
                        
                        if tc_chunk.function.name:
                            # Some models might send the same name in multiple chunks
                            if not tool_calls[tc_chunk.index]["function"]["name"].endswith(tc_chunk.function.name):
                                tool_calls[tc_chunk.index]["function"]["name"] += tc_chunk.function.name
                        if tc_chunk.function.arguments:
                            tool_calls[tc_chunk.index]["function"]["arguments"] += tc_chunk.function.arguments

                # Handle Content
                content = delta.content
                if content is not None:
                    full_response += content
                    yield ("content", content)
            
            if tool_calls:
                # Add tool calls to history
                self.history.append({
                    "role": "assistant",
                    "content": full_response if full_response else None,
                    "tool_calls": tool_calls
                })
                yield ("tool_calls", tool_calls)
            else:
                self.history.append({"role": "assistant", "content": full_response})
                
        except Exception as e:
            yield ("error", str(e))
