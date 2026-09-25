import os
from datetime import datetime
from agents.planner import PlannerAgent
from agents.worker import WorkerAgent
from services.document_writer import DocumentWriter


class Orchestrator:

    def __init__(self):
        self.planner = PlannerAgent()
        self.worker = WorkerAgent()
        self.writer = DocumentWriter()

    def generate_document(self, request: str) -> str:
        # Step 1: Create Plan with Search Queries
        print(f"[Orchestrator] Planning document for: '{request}'")
        planned_sections = self.planner.create_plan(request)

        # Fallback if planner returns empty
        if not planned_sections:
            planned_sections = [
                {"section": "Overview", "search_query": request},
                {"section": "Detailed Findings", "search_query": None},
                {"section": "Conclusion", "search_query": None},
            ]

        # Step 2: Research & Generate Content
        print("[Orchestrator] Generating sections and researching facts...")
        generated_dict, sources = self.worker.generate_sections(
            request, planned_sections
        )

        # Step 3: Align content and build section list
        final_sections = []
        for item in planned_sections:
            title = item.get("section")
            # Robust lookup: exact match or fallback to empty string
            content = generated_dict.get(
                title,
                generated_dict.get(
                    title.replace("Write ", ""), "Content could not be generated."
                ),
            )
            final_sections.append({"heading": title, "content": content})

        # Step 4: Write Word Document
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(
            "outputs", f"Generated_Document_{timestamp}.docx"
        )

        print(f"[Orchestrator] Saving document to: {output_file}")
        self.writer.create_document(
            title=request,
            sections=final_sections,
            sources=sources,
            output_file=output_file,
        )

        return output_file