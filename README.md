# 🧠 MSFoundryAgentMemory

> **Agent Memory Management with Microsoft Foundry**  
> Practical Python examples for building stateful AI agents using the `azure-ai-projects` SDK — covering basic memory, advanced patterns, and full CRUD lifecycle management.

---

## 📌 Overview

This repository demonstrates how to implement **persistent agent memory** on top of **Microsoft Foundry** (Azure AI Foundry). Rather than one-shot Q&A, these examples show how agents can store, retrieve, update, and delete context across multi-turn conversations — a foundational capability for production-grade AI assistants.

Three progressive examples are provided:

| File | Focus |
|---|---|
| `memory_basic.py` | Create and retrieve memory entries in a single agent session |
| `memory_advanced.py` | Contextual memory with semantic retrieval and multi-turn state |
| `memory_crud.py` | Full Create / Read / Update / Delete lifecycle for agent memory |

---

## 🏗️ Architecture

```
User Input
    │
    ▼
Microsoft Foundry Agent (azure-ai-projects)
    │
    ├── memory_basic.py    →  Store & Recall
    ├── memory_advanced.py →  Semantic + Multi-turn
    └── memory_crud.py     →  Full CRUD lifecycle
    │
    ▼
Memory Store (Thread / In-context / External)
```

Authentication is handled via **`DefaultAzureCredential`** — no hardcoded keys required.

---

## ⚙️ Prerequisites

- Python 3.9+
- An **Azure AI Foundry** project with a deployed chat model (e.g., `gpt-4o`, `gpt-4-turbo`)
- Azure CLI authenticated (`az login`) **or** a managed identity / service principal

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/praveen11singh/MSFoundryAgentMemory.git
cd MSFoundryAgentMemory
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install azure-ai-projects azure-identity
```

### 4. Configure environment variables

Copy `.env` and fill in your Foundry project details:

```env
PROJECT_CONNECTION_STRING=<your-azure-ai-foundry-connection-string>
MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

> **Tip:** The connection string is available in your Azure AI Foundry project under **Settings → Project details**.

---

## 📂 Examples

### `memory_basic.py` — Store & Retrieve

Demonstrates the simplest form of agent memory: storing a fact during a conversation and recalling it in a later turn.

```bash
python memory_basic.py
```

**Key concepts:**
- Creating an agent with system instructions
- Using conversation threads as implicit memory
- Passing prior context back to the agent

---

### `memory_advanced.py` — Contextual & Multi-turn Memory

Builds on the basic example by showing how to maintain rich context across multiple exchanges — simulating a persistent user profile or session state.

```bash
python memory_advanced.py
```

**Key concepts:**
- Structured memory payloads (user preferences, past actions)
- Injecting memory context into system prompts dynamically
- Managing token budget when context grows large

---

### `memory_crud.py` — Full CRUD Lifecycle

Demonstrates a complete memory management system: creating entries, reading them back, updating values, and deleting stale context — useful for long-running agent workflows.

```bash
python memory_crud.py
```

**Key concepts:**
- Memory entry schema design
- Update vs. append strategies
- Cleaning up expired or irrelevant memory

---

## 🔐 Authentication

All examples use `DefaultAzureCredential` from the `azure-identity` library:

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

credential = DefaultAzureCredential()
client = AIProjectClient.from_connection_string(
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
    credential=credential
)
```

`DefaultAzureCredential` automatically picks up credentials from:
- `az login` (local development)
- Managed Identity (Azure-hosted workloads)
- Environment variables (`AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`)

---

## 🔗 Related Repositories

| Repo | Description |
|---|---|
| [MSFoundryFunctionCall](https://github.com/praveen11singh/MSFoundryFunctionCall) | Auto function calling & explicit toolset registration with Microsoft Foundry |

---

## 📚 Resources

- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
- [azure-ai-projects SDK](https://pypi.org/project/azure-ai-projects/)
- [DefaultAzureCredential Reference](https://learn.microsoft.com/python/api/azure-identity/azure.identity.defaultazurecredential)

---

## 🤝 Contributing

Issues and PRs are welcome! If you build an interesting memory pattern on top of Microsoft Foundry, feel free to open a pull request.

---

License — see [LICENSE](LICENSE) for details.
