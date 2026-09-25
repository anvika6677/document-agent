from orchestrator import Orchestrator

orchestrator = Orchestrator()

result = orchestrator.generate_document(
    "Create a business proposal for a coffee shop."
)

print(result)