import json
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from client import CuantoxClient
from interface import welcome_message, stream_response, console, print_tool_call, print_tool_result, get_confirmation
from tools import TOOL_MAP

# Modern REPL style
style = Style.from_dict({
    'prompt': 'ansicyan bold',
})

def main():
    welcome_message()
    
    # Initialize client
    client = CuantoxClient()
    
    session = PromptSession(history=FileHistory('.cuantox_history'), style=style)
    
    while True:
        try:
            user_input = session.prompt('\nUser: ')
            
            if not user_input.strip():
                continue
                
            if user_input.lower() in ['exit', 'quit', 'bye']:
                console.print("[info]Goodbye![/info]")
                break
                
            if user_input.lower() == 'clear':
                console.clear()
                continue
            
            # Agent Loop
            next_msg = user_input
            tool_results = None
            
            while True:
                # Call the AI
                res_type, res_val = stream_response(client.chat_stream(next_msg, tool_results))
                
                if res_type == "tool_calls":
                    tool_results = []
                    for call in res_val:
                        name = call["function"]["name"]
                        args_str = call["function"]["arguments"]
                        try:
                            args = json.loads(args_str)
                        except:
                            args = {}
                        
                        # Confirmation for dangerous tools
                        if name == "execute_command":
                            if not get_confirmation(f"Allow execution of: {args.get('command', 'unknown')}?"):
                                result = "User denied execution."
                                print_tool_result(result)
                                tool_results.append({
                                    "role": "tool",
                                    "tool_call_id": call["id"],
                                    "name": name,
                                    "content": result
                                })
                                continue
                        
                        print_tool_call(name, args_str)
                        
                        # Execute Tool
                        if name in TOOL_MAP:
                            result = TOOL_MAP[name](**args)
                            # Specialized hint for Windows execution failures
                            if name == "execute_command":
                                if "timed out" in str(result).lower():
                                    result += "\nHint: The command timed out. This usually happens if it's waiting for interactive input. Use piped input instead."
                                elif "failed" in str(result).lower():
                                    result += "\nHint: You are on Windows. Avoid Linux-specific syntax like '<< EOF' or 'python3' (use 'python' instead)."
                        else:
                            result = f"Error: Tool {name} not found."
                        
                        print_tool_result(result)
                        
                        tool_results.append({
                            "role": "tool",
                            "tool_call_id": call["id"],
                            "name": name,
                            "content": str(result)
                        })
                    
                    # AI needs to process tool results
                    next_msg = None # Clear user input for next turn
                    continue
                else:
                    break # Finished or Error
            
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        except Exception as e:
            console.print(f"[error]An error occurred: {e}[/error]")

if __name__ == "__main__":
    main()
