from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from rich.panel import Panel
from rich.theme import Theme

# Define a premium theme for Cuantox
cuantox_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "prompt": "bold magenta",
    "user": "bold blue",
    "assistant": "bold white"
})

console = Console(theme=cuantox_theme)

def welcome_message():
    console.print(Panel.fit(
        "[bold cyan]Cuantox-AI[/bold cyan] v1.0\n[italic]Your ultimate AI coding companion[/italic]",
        border_style="cyan",
        subtitle="Powered by Minimax M2.5"
    ))

def print_user_prompt():
    console.print("\n[user]❯ [/user]", end="")

class StreamingRenderer:
    def __init__(self):
        self.full_content = ""

    def render(self, content_chunk):
        self.full_content += content_chunk
        return Markdown(self.full_content)

def print_tool_call(name, args):
    console.print(Panel(
        f"[bold blue]🔧 Tool Call:[/bold blue] [cyan]{name}[/cyan]\n[dim]{args}[/dim]",
        border_style="blue",
        title="[bold blue]Executing Tool[/bold blue]"
    ))

def print_tool_result(result):
    console.print(f"[bold green]✅ Result:[/bold green] [dim]{result}[/dim]")

def get_confirmation(question):
    """Asks the user for confirmation (Y/N)."""
    console.print(f"\n[bold yellow]⚠️  {question} (y/n): [/bold yellow]", end="")
    choice = input().lower().strip()
    return choice in ['y', 'yes']

def stream_response(generator):
    renderer = StreamingRenderer()
    
    # Show loading status before streaming starts
    with console.status("[bold cyan]Cuantox-AI is thinking...[/bold cyan]", spinner="dots") as status:
        try:
            # We wait for the first chunk/event to know we have a connection
            first_event = next(generator)
            status.update("[bold cyan]Response received, processing...[/bold cyan]")
        except StopIteration:
            # If nothing was yielded, the AI might have finished silently or errored out
            return ("done", None)
        except Exception as e:
            console.print(f"[error]Stream Error: {e}[/error]")
            return ("error", str(e))

    # Handle the first event
    ev_type, ev_content = first_event
    
    if ev_type == "content":
        console.print(f"[assistant]Cuantox-AI:[/assistant]")
        with Live(renderer.render(ev_content), refresh_per_second=10, vertical_overflow="visible") as live:
            for ev_type, ev_content in generator:
                if ev_type == "content":
                    live.update(renderer.render(ev_content))
                elif ev_type == "tool_calls":
                    return ("tool_calls", ev_content)
    elif ev_type == "tool_calls":
        return ("tool_calls", ev_content)
    elif ev_type == "error":
        console.print(f"[error]AI Error: {ev_content}[/error]")
    
    return ("done", None)

