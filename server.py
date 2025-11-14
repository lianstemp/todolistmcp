import os
from typing import List, Optional
from fastmcp import FastMCP
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    # FastMCP will surface this on startup if missing
    raise RuntimeError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment or .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Fix: Gunakan 'instructions' bukan 'description'
app = FastMCP(
    name="todolist-supabase",
    instructions="Simple todo list MCP server backed by Supabase for learning.",
)

@app.tool()
def list_todos(done: Optional[bool] = None) -> List[dict]:
    """List todo items.
    Args:
        done: If provided, filter todos by completion status.
    """
    query = supabase.table("todos").select("id, title, done, inserted_at").order("inserted_at", desc=True)
    if done is not None:
        query = query.eq("done", done)
    response = query.execute()
    return response.data or []

@app.tool()
def add_todo(title: str) -> dict:
    """Add a new todo item.
    Args:
        title: Short description of the task.
    """
    if not title.strip():
        raise ValueError("title cannot be empty")
    response = supabase.table("todos").insert({"title": title.strip(), "done": False}).execute()
    if not response.data:
        raise RuntimeError("Failed to insert todo")
    return response.data[0]

@app.tool()
def set_todo_done(todo_id: int, done: bool = True) -> dict:
    """Mark a todo as done/undone.
    Args:
        todo_id: ID of the todo.
        done: True to mark as done, False to mark as not done.
    """
    response = (
        supabase
        .table("todos")
        .update({"done": done})
        .eq("id", todo_id)
        .execute()
    )
    if not response.data:
        raise RuntimeError("Todo not found or update failed")
    return response.data[0]

@app.tool()
def delete_todo(todo_id: int) -> dict:
    """Delete a todo by id.
    Args:
        todo_id: ID of the todo to delete.
    """
    response = supabase.table("todos").delete().eq("id", todo_id).execute()
    if not response.data:
        raise RuntimeError("Todo not found or delete failed")
    return response.data[0]

def main() -> None:
    """Entry point for `poetry run dev`."""
    app.run()

if __name__ == "__main__":
    # Run as a plain FastMCP server (useful for quick local testing)
    main()