# 🏆 The Top 1% MCP Server Guidebook

This guide outlines the architectural standards and best practices for building world-class Model Context Protocol (MCP) servers. Follow this blueprint to ensure your project is modular, scalable, and highly reliable for AI agents.

---

## 1. Project Architecture (Modular over Monolithic)
Avoid single-file servers for complex projects. Use a standard Python professional layout:

```text
├── src/
│   └── my_mcp_server/
│       ├── __init__.py
│       ├── server.py          # Entry point and server initialization
│       ├── clients/           # API handlers (Open Targets, Google, etc.)
│       │   └── graphql.py     # Network logic & authentication
│       ├── tools/             # One file per major tool/workflow
│       │   ├── discovery.py
│       │   └── analysis.py
│       ├── lib/               # Shared utilities and logic
│       └── models/            # Pydantic models for data validation
├── tests/                     # Automated testing suite
├── pyproject.toml             # Modern packaging (uv, poetry, or pip)
├── Dockerfile                 # For containerized deployment
└── README.md                  # Comprehensive user documentation
```

---

## 2. Tool Design Philosophy
A Top 1% MCP server serves the **AI Agent**, not just the human.

### **Workflow-Oriented Tools**
Instead of giving the AI raw access to a DB, give it "Job-Specific" tools. 
*   ❌ **Bad**: `run_query(sql_string)`
*   ✅ **Good**: `get_cancer_profile(target_id)` 
*   *Why*: Reduces AI hallucination and prevents schema errors.

### **Prompt-Engineered Descriptions**
The AI chooses tools based on their descriptions. Use "AI Instructions" inside the docstrings:
```python
@mcp.tool()
async def analyze_safety(target_id: str):
    """
    Analyzes safety liabilities for a given protein target.
    USE THIS tool when the user asks about side effects, toxicities, or risk factors.
    Args:
        target_id: Standard Ensembl ID (e.g., ENSG...)
    """
```

---

## 3. Data Integrity & Validation
Always use **Type Hints** and **Pydantic Models**. 
1.  **Strict Typing**: Ensures the AI sends the correct data format.
2.  **Flattened Responses**: Don't return nested, complex JSON. The AI struggles with deeply nested data. Flatten your responses into clean, key-value pairs.
3.  **Token Efficiency**: Only return data the AI actually needs. Massive responses waste "context window" and cost more.

---

## 4. Error Handling & Resilience
A professional server never "crashes" for the agent.
*   **API Retries**: Use libraries like `tenacity` for flaky network calls.
*   **Friendly Errors**: Don't return a Traceback. Return a JSON error message explaining *how* the AI can fix the input.
    *   *Example*: `"Error: Disease 'Heart' is too broad. Please use 'resolve_id' first to get a specific EFO ID."`

---

## 5. The "Discovery" Layer
Always include a `resolve_id` or `search` tool. 
AI agents are bad at guessing IDs (ChEMBL IDs, Ensembl IDs). Every high-quality MCP should have:
1.  **Search Tool**: Name $\rightarrow$ ID.
2.  **Schema Tool**: (Optional) If providing raw query access, provide a tool that returns the database fields.

---

## 6. Development Workflow
To build like the Top 1%:
1.  **Use a Virtual Environment**: Always isolate your dependencies (`.venv`).
2.  **Requirement Lockfiles**: Use `uv.lock` or `requirements.txt` to ensure consistent runs.
3.  **Grep & Inspect**: Use introspection to verify API schemas (as we did with the Open Targets GraphQL today).

---

## 7. Packaging & "The Look"
A great repository must have:
*   **Professional Branding**: A descriptive `About` section and clear `Topics`.
*   **One-Click Install**: Support `npx` (if JS) or clear `pip` instructions.
*   **Documentation**: Include an "Example Questions" section in the README to tell the user *how* to interact with the server.

---
*Created with insights from the OpentargetMCP Development Cycle.*
