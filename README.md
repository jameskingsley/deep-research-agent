# Deep Research Agent 
### Professional Multi-Agent Research Framework

A production-grade, autonomous research system leveraging **Multi-Agent Orchestration** to perform deep, iterative web searches and synthesize professional reports. Built with a decoupled architecture for high performance and scalability.

---

##  Live Deployments
* **Frontend UI:** [https://deep-research-agent-5u8apq7tljgqz9mcv9sxva.streamlit.app/](https://deep-research-agent-5u8apq7tljgqz9mcv9sxva.streamlit.app/)
* **Backend API:** [https://deep-research-agent-3nl8.onrender.com](https://deep-research-agent-3nl8.onrender.com)

---

##  System Architecture
The framework follows a "Planner-Executor-Reporter" agentic pattern:

1.  **Planner Agent:** Deconstructs complex user queries into high-density search sub-tasks.
2.  **Research Agent:** Executes autonomous, iterative searches via **Tavily AI**, refining search parameters based on data density.
3.  **Synthesis Agent:** Aggregates findings into a structured, professional Markdown report.
4.  **API Layer:** **FastAPI** handles the heavy-lifting orchestration, keeping the UI lightweight.

---

## Technical Stack
* **Agentic Orchestration:** `LlamaIndex Workflows`
* **Inference Engine:** `Groq` (Llama 3.1 70B)
* **Intelligence:** `Tavily AI` (LLM-optimized search)
* **Backend:** `FastAPI` + `Uvicorn`
* **Frontend:** `Streamlit`
* **Deployment:** `Render` (Backend) & `Streamlit Cloud` (Frontend)

---

##  Key Features
* **Autonomous Iteration:** The agent evaluates search results and triggers further research if data quality is low.
* **Professional Exports:** Native support for **TXT** and **PDF** generation for academic or corporate use.
* **Macro-Aware Analysis:** Specialized in synthesizing complex technical and economic data.
* **Production-Ready:** Decoupled architecture using CI/CD via GitHub.

---

##  Project Structure
```text
├── src/
│   ├── tools/
│   │   ├── search.py       # Tavily AI Search integration
│   │   └── writer.py       # PDF/Markdown formatting logic
│   ├── agent.py            # LlamaIndex Multi-Agent Workflow
│   └── api.py              # FastAPI Service
├── ui/
│   └── app.py              # Streamlit User Interface
├── requirements.txt        # Production dependencies
└── render.yaml             # Render Blueprint configuration