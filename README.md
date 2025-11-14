# Simple Supabase TodoList MCP (FastMCP, Python)

This is a very simple Model Context Protocol (MCP) server using **FastMCP** and **Supabase** to manage a todo list.
It's intentionally minimal for learning, based on the Supabase MCP guide.

## Files

- `src/mcp_server.py` — FastMCP server exposing tools to list/add/update/delete todos in Supabase.
- `supabase_schema.sql` — SQL to create a simple `todos` table and basic policies in Supabase.
- `requirements.txt` — Python dependencies.
- `.env.example` — Example environment variables for connecting to your Supabase project.

## 1. Create the Supabase table

1. Open your Supabase project dashboard.
2. Go to **SQL** → **New query**.
3. Paste the contents of `supabase_schema.sql` and run it.
4. Confirm that the `public.todos` table exists with columns: `id`, `title`, `done`, `inserted_at`.

## 2. Environment variables (.env)

Create a `.env` file in the project root (same folder as `requirements.txt`) based on `.env.example`:

- `SUPABASE_URL` — from **Project Settings → API → Project URL**.
- `SUPABASE_ANON_KEY` — from **Project Settings → API → anon public** or service role key.

> For local learning only, using the anon key is OK. For anything serious, follow the
> security advice in the Supabase MCP guide and avoid leaking secrets.

## 3. Install dependencies

From this folder:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 4. Run the MCP server directly (for quick test)

After the virtualenv is activated and `.env` is configured:

```bash
python -m src.mcp_server
```

The server will start and FastMCP will expose the MCP interface on stdout/stdin (for
integration with clients that speak MCP). For quick debugging, you can also add print
statements or temporary test calls in `mcp_server.py`.

## 5. MCP tools exposed

The server exposes these tools:

- `list_todos(done: Optional[bool]) -> List[dict]`
- `add_todo(title: str) -> dict`
- `set_todo_done(todo_id: int, done: bool = True) -> dict`
- `delete_todo(todo_id: int) -> dict`

Example behavior:

- Add a todo: creates a new row with `done = false`.
- List todos: returns all rows, optionally filtered by `done`.
- Set todo done: updates `done` for the given `id`.
- Delete todo: deletes the row and returns the deleted row.

## 6. Security notes (summary)

This project is for **learning only**. When using MCP with Supabase:

- Do **not** commit your real `.env` with secrets to Git.
- Rotate keys if you accidentally expose them.
- Restrict RLS policies for real apps (limit access per user/session).
- Consider using service role keys only in trusted backend environments, not in
  client-side MCP servers that might run on untrusted machines.

For more detail, see the official Supabase MCP guide:

https://supabase.com/docs/guides/getting-started/mcp#security-risks
