from services.llm_service import LLMService
from prompts.worker_prompt import WORKER_PROMPT
from utils.json_parser import extract_json
from tools.search_tool import TavilySearchTool


class WorkerAgent:

    def __init__(self):
        self.llm = LLMService()
        self.search_tool = TavilySearchTool()

    def generate_sections(self, topic: str, planned_sections: list[dict]) -> tuple[dict, list[dict]]:
        """Conducts research for sections that require external data,

        then generates content for all sections in a single batched LLM call.

        Returns:
            tuple[dict, list[dict]]: (generated_sections_dict, sources_list)
        """
        research_snippets = []
        collected_sources = []
        section_titles = []

        # 1. Execute targeted searches where needed
        for item in planned_sections:
            title = item.get("section")
            query = item.get("search_query")
            section_titles.append(title)

            if query:
                print(f"[WorkerAgent] Researching: '{query}'...")
                results = self.search_tool.search_web(query, max_results=2)
                for res in results:
                    research_snippets.append(
                        f"[{title}] {res['title']}: {res['content']}"
                    )
                    collected_sources.append(
                        {"title": res["title"], "url": res["url"]}
                    )

        research_context = (
            "\n\n".join(research_snippets)
            if research_snippets
            else "No external search required."
        )

        # 2. Format worker prompt
        prompt = WORKER_PROMPT.format(
            topic=topic,
            sections="\n".join([f"- {title}" for title in section_titles]),
            research_context=research_context,
        )

        response = self.llm.generate(prompt)

        try:
            generated_content = extract_json(response)
            if not isinstance(generated_content, dict):
                generated_content = {}
        except Exception as e:
            print(f"[WorkerAgent Error] Failed to parse JSON: {e}")
            generated_content = {}

        return generated_content, collected_sources