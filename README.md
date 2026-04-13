# Open Targets MCP Server 🧬

A professional-grade, workflow-oriented Model Context Protocol (MCP) server for therapeutic discovery and drug repurposing. This server provides a seamless bridge between agentic AI platforms and the [Open Targets Platform](https://platform.opentargets.org/), leveraging its comprehensive GraphQL API.

---

## 🚀 Key Features

*   **Modular Architecture**: Built with a clean separation of concerns (Clients, Tools, Models) following the Top 1% MCP standard.
*   **Type-Safe Validation**: Powered by **Pydantic** to ensure 100% reliable data structures for AI consumption.
*   **Workflow-Oriented Tools**: Abstracted complex queries into high-level therapeutic workflows (Cancer profiling, Safety, Tractability).
*   **Modern Transport**: Supports the latest **Streamable-HTTP** transport layer.
*   **Automated Testing**: Integrated `pytest` suite for verified API reliability.

---

## 🏗 Repository Structure

```text
├── src/
│   └── opentarget_mcp/
│       ├── clients/       # GraphQL & API Communication
│       ├── tools/         # Domain-specific logic (Analysis, Cancer, etc.)
│       ├── models/        # Pydantic data validation classes
│       └── server.py      # Modular server initialization
├── tests/                 # Automated test suite (pytest)
├── server.py              # Root entry point
└── requirements.txt       # Optimized dependencies
```

---

## 🛠 Installation & Setup

### 1. Clone & Environment
```bash
git clone https://github.com/aakashyadav27/OpentargetMCP.git
cd OpentargetMCP
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Server
```bash
export PYTHONPATH=$PYTHONPATH:.
python3 server.py
```
The server will start using the **Streamable-HTTP** transport, listening at `http://127.0.0.1:8000/mcp`.

---

## 🧪 Testing

This project includes a comprehensive test suite to ensure API compliance.
```bash
export PYTHONPATH=$PYTHONPATH:.
pytest tests/
```

---

## 🤖 Usage with AI Agents

### Option A: Automatic Setup (Recommended)
This method tells the AI client (Claude Desktop, Cursor, etc.) to start the server for you in the background.

```json
{
  "mcpServers": {
    "opentarget": {
      "command": "python3",
      "args": ["/absolute/path/to/OpentargetMCP/server.py"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/OpentargetMCP"
      }
    }
  }
}
```

### Option B: Remote / Manual Setup
Use this if you are running the server manually in a terminal or on a remote machine.

1. **Start the server:**
   ```bash
   export PYTHONPATH=.
   python3 server.py
   ```
2. **Add this to your config:**
   ```json
   {
     "mcpServers": {
       "opentarget": {
         "url": "http://127.0.0.1:8000/mcp"
       }
     }
   }
   ```

---

## 📄 License
MIT License
