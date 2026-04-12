# Open Targets MCP Server 🧬

A powerful, workflow-oriented Model Context Protocol (MCP) server for therapeutic discovery and drug repurposing. This server provides a seamless bridge between agentic AI platforms and the [Open Targets Platform](https://platform.opentargets.org/), leveraging its comprehensive GraphQL API.

## 🚀 Features

The server implements a suite of specialized tools for automated drug discovery:

*   **Entity Resolution**: Resolve common names (e.g., 'BRCA2', 'aspirin', 'asthma') to standardized identifiers (Ensembl, ChEMBL, EFO).
*   **Target Prioritization**: Retrieve top associated targets for any disease, ranked by multi-faceted association scores.
*   **Safety Assessments**: Quickly pull safety liabilities, toxicities, and risk information for gene/protein targets.
*   **Pharmacovigilance**: Access statistical FDA FAERS data (adverse events) for known drugs using log-likelihood ratios.
*   **Druggability Analysis**: View comprehensive tractability summaries for targets across multiple modalities (Small Molecule, Antibody, etc.).
*   **Disease Phenotyping**: Map diseases to their clinical signs and symptoms using the Human Phenotype Ontology (HPO).
*   **Cancer Profiling**: Retrieve cancer hallmarks (COSMIC) and gene essentiality scores from the Cancer Dependency Map (DepMap).
*   **Animal Models**: Access significant phenotypes observed in biological mouse models for human targets.

## 🛠 Tech Stack

*   **Core**: Python 3.10+
*   **MCP Framework**: [FastMCP](https://github.com/jlowin/fastmcp)
*   **API Interface**: Open Targets GraphQL API (v4)
*   **Runtime**: HTTP/Streamable transport for modern agentic platforms.

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd OpentargetMCP
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**:
   ```bash
   python server.py
   ```

## 🤖 Usage with AI Agents

To use this with an MCP-compatible agent (like Claude Desktop or Cursor), add the following to your configuration:

```json
{
  "mcpServers": {
    "opentarget": {
      "command": "python",
      "args": ["/path/to/OpentargetMCP/server.py"]
    }
  }
}
```

## 📜 Example Questions

*   "Find repurposing candidates for Imatinib and identify its top associated diseases."
*   "What are the top therapeutic targets for Alzheimer's and their safety profiles?"
*   "Check the cancer essentiality of KRAS across various tissues."
*   "What are the clinical signs of Parkinson's Disease according to HPO?"

## 📄 License
MIT License
