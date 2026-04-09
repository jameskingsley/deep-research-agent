import os
from pathlib import Path
from dotenv import load_dotenv
from llama_index.core.workflow import Event, StartEvent, StopEvent, Workflow, step
from llama_index.llms.groq import Groq 
from llama_index.tools.tavily_research import TavilyToolSpec
from phoenix.otel import register
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor

# Load environment variables
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Setup Arize Phoenix Tracing (Silent Mode) 
PHOENIX_KEY = os.getenv("PHOENIX_API_KEY")
if PHOENIX_KEY:
    try:
        register(
            endpoint="https://app.phoenix.arize.com/v1/traces",
            headers={"Authorization": f"Bearer {PHOENIX_KEY.strip()}"},
            project_name=os.getenv("PHOENIX_PROJECT_NAME", "deep-research-agent")
        )
        LlamaIndexInstrumentor().instrument()
    except:
        pass 

class ResearchEvent(Event):
    query: str

class ReviewEvent(Event):
    data: str
    original_query: str

class DeepResearchWorkflow(Workflow):
    MAX_SEARCH_CALLS = 3
    
    def __init__(self, timeout=600):
        super().__init__(timeout=timeout)
        self.llm = Groq(
            model="llama-3.3-70b-versatile", 
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.search_tool = TavilyToolSpec(api_key=os.getenv("TAVILY_API_KEY"))
        self.search_count = 0

    @step
    async def planner(self, ev: StartEvent) -> ResearchEvent:
        print(f"--- Planning Phase: {ev.query} ---")
        prompt = (
            f"Generate a single search query to find the latest 2026 data for: {ev.query}. "
            f"Respond with ONLY the query text."
        )
        response = await self.llm.acomplete(prompt)
        return ResearchEvent(query=response.text.strip().replace('"', ''))

    @step
    async def researcher(self, ev: ResearchEvent) -> ReviewEvent:
        if self.search_count >= self.MAX_SEARCH_CALLS:
            return ReviewEvent(data="Search limit reached.", original_query=ev.query)
        
        print(f"--- Searching Tavily: {ev.query} (Call {self.search_count + 1}) ---")
        self.search_count += 1
        
        try:
            results = self.search_tool.search(query=ev.query, max_results=5)
            return ReviewEvent(data=str(results), original_query=ev.query)
        except Exception as e:
            return ReviewEvent(data=f"Search failed: {str(e)}", original_query=ev.query)

    @step
    async def reviewer(self, ev: ReviewEvent) -> ResearchEvent | StopEvent:
        print("--- Reviewing Data ---")
        
        # Check if I'm at the limit
        is_last_attempt = self.search_count >= self.MAX_SEARCH_CALLS
        
        if is_last_attempt:
            # Force the LLM to write a report regardless of data quality
            review_prompt = (
                f"Context Data: {ev.data}\n"
                f"User Goal: {ev.original_query}\n\n"
                "ATTENTION: This is your final chance. Do NOT suggest a re-search. "
                "Write a professional research report using the available data above. "
                "If some data is missing, summarize what you have found so far. "
                "Include a 'Sources' section with the URLs provided."
            )
        else:
            # Standard refinement logic
            review_prompt = (
                f"Context Data: {ev.data}\n"
                f"User Goal: {ev.original_query}\n\n"
                "Task: If the data is sufficient to answer the user goal deeply, write a professional research report with Sources. "
                "If the data is vague or insufficient, respond ONLY with 'RE-SEARCH: [new specific query]'. "
                "Format: Use Markdown, Title, Executive Summary, Key Findings, and Sources."
            )
        
        response = await self.llm.acomplete(review_prompt)
        
        # Only loop back if it's not the last attempt
        if "RE-SEARCH" in response.text.upper() and not is_last_attempt:
            try:
                new_query = response.text.split("RE-SEARCH:")[-1].strip()
            except:
                new_query = response.text[:50]
            return ResearchEvent(query=new_query)
        
        # Stop and return whatever the LLM generated (Report or Final Summary)
        return StopEvent(result=response.text)