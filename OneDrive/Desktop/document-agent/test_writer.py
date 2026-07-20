from services.document_writer import DocumentWriter

writer = DocumentWriter()

sections = [
    {
        "task": "Executive Summary",
        "content": "This proposal presents a business opportunity."
    },
    {
        "task": "Market Analysis",
        "content": "The coffee market continues to grow steadily."
    },
    {
        "task": "Financial Plan",
        "content": "Initial investment is estimated at $50,000."
    }
]

writer.write(
    title="Coffee Shop Business Proposal",
    sections=sections,
    output_file="BusinessProposal.docx"
)

print("Document created successfully!")