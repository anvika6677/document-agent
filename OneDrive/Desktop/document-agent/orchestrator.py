from agents.planner import PlannerAgent
from agents.worker import WorkerAgent
from services.document_writer import DocumentWriter
import os
from datetime import datetime


class Orchestrator:

    def __init__(self):

        self.planner = PlannerAgent()
        self.worker = WorkerAgent()
        self.writer = DocumentWriter()

    def generate_document(self, request: str):

        print("\n========== STEP 1 ==========")
        print("Planning document...")

        tasks = self.planner.create_plan(request)

        print(tasks)

        generated_sections = self.worker.generate_sections(
            request,
            tasks
        )

        sections = []

        for task in tasks:

            sections.append({
                "heading": task,
                "content": generated_sections.get(
                    task,
                    "Content could not be generated."
                )
            })

            

        print("\n========== STEP 3 ==========")
        print("Creating Word document...")

        os.makedirs("outputs", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        output_file = f"outputs/Generated_Document_{timestamp}.docx"

        self.writer.write(
            title=request,
            sections=sections,
            output_file=output_file
        )

        return output_file