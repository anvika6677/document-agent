import os
from datetime import datetime
from langgraph.graph import StateGraph, START, END

from agents.state import AgentState
from agents.planner import PlannerAgent
from agents.worker import WorkerAgent
from services.document_writer import DocumentWriter
from tools.search_tool import TavilySearchTool
from prompts.worker_prompt import WORKER_PROMPT
from utils.json_parser import extract_json


class ResearchGraphOrchestrator:

    def __init__(self):
        self.planner = PlannerAgent()
        self.search_tool = TavilySearchTool()
        self.writer = DocumentWriter()
        self.worker = WorkerAgent()
        self.graph = self._build_graph()

    # --- NODE 1: PLANNER ---
    def planner_node(self, state: AgentState) -> dict:
        request = state["request"]
        print(f"\n[LangGraph: Planner] Planning outline for: '{request}'")

        plan = self.planner.create_plan(request)
        if not plan:
            plan = [
                {"section": "Overview", "search_query": request},
                {"section": "Detailed Findings", "search_query": None},
                {"section": "Conclusion", "search_query": None},
            ]
        return {"planned_sections": plan}

    # --- NODE 2: RESEARCHER ---
    def researcher_node(self, state: AgentState) -> dict:
        planned_sections = state["planned_sections"]
        research_snippets = []
        collected_sources = []

        print("[LangGraph: Researcher] Checking and executing search queries...")
        for item in planned_sections:
            title = item.get("section")
            query = item.get("search_query")

            if query:
                print(f"  -> Tavily Query: '{query}'")
                results = self.search_tool.search_web(query, max_results=2)
                for res in results:
                    research_snippets.append(
                        f"[{title}] {res['title']}: {res['content']}"
                    )
                    collected_sources.append(
                        {"title": res["title"], "url": res["url"]}
                    )

        context = (
            "\n\n".join(research_snippets)
            if research_snippets
            else "No external search required."
        )
        return {"research_context": context, "sources": collected_sources}

    # --- NODE 3: WRITER ---
    def writer_node(self, state: AgentState) -> dict:
        print("[LangGraph: Writer] Generating content for all sections...")
        topic = state["request"]
        planned = state["planned_sections"]
        research_context = state["research_context"]

        section_titles = [item.get("section") for item in planned]
        prompt = WORKER_PROMPT.format(
            topic=topic,
            sections="\n".join([f"- {title}" for title in section_titles]),
            research_context=research_context,
        )

        response = self.worker.llm.generate(prompt)

        try:
            content_dict = extract_json(response)
            if not isinstance(content_dict, dict):
                content_dict = {}
        except Exception as e:
            print(f"[LangGraph Writer Error] JSON parse failure: {e}")
            content_dict = {}

        # Align content to planned sections
        final_sections = []
        for item in planned:
            title = item.get("section")
            content = content_dict.get(
                title,
                content_dict.get(
                    title.replace("Write ", ""),
                    "Content could not be generated.",
                ),
            )
            final_sections.append({"heading": title, "content": content})

        return {
            "generated_content": content_dict,
            "final_sections": final_sections,
        }

    # --- NODE 4: DOCUMENT EXPORT ---
    def docx_node(self, state: AgentState) -> dict:
        print("[LangGraph: DocxWriter] Assembling Word document...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(
            "outputs", f"Generated_Document_{timestamp}.docx"
        )

        self.writer.create_document(
            title=state["request"],
            sections=state["final_sections"],
            sources=state["sources"],
            output_file=output_file,
        )
        return {"output_file": output_file}

    # --- GRAPH COMPILATION ---
    def _build_graph(self):
        builder = StateGraph(AgentState)

        # Register Nodes
        builder.add_node("planner", self.planner_node)
        builder.add_node("researcher", self.researcher_node)
        builder.add_node("writer", self.writer_node)
        builder.add_node("docx_writer", self.docx_node)

        # Define Directed Flow
        builder.add_edge(START, "planner")
        builder.add_edge("planner", "researcher")
        builder.add_edge("researcher", "writer")
        builder.add_edge("writer", "docx_writer")
        builder.add_edge("docx_writer", END)

        return builder.compile()

    def generate_document(self, request: str) -> str:
        initial_state: AgentState = {
            "request": request,
            "planned_sections": [],
            "research_context": "",
            "sources": [],
            "generated_content": {},
            "final_sections": [],
            "output_file": None,
            "error": None,
        }

        # Run the full graph
        final_state = self.graph.invoke(initial_state)
        return final_state["output_file"]