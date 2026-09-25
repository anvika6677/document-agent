import re

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

#from orchestrator import Orchestrator
from schemas.document_request import DocumentRequest

from graph_orchestrator import ResearchGraphOrchestrator



app = FastAPI(
    title="Autonomous Document Agent",
    description="AI-powered document generation system",
    version="1.0.0"
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML templates
templates = Jinja2Templates(directory="templates")

# AI Orchestrator
#orchestrator = Orchestrator()

orchestrator = ResearchGraphOrchestrator()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/generate-document")
def generate_document(data: DocumentRequest):

    try:

        output_file = orchestrator.generate_document(
            data.request
        )

        # Create a clean download filename from the user request
        clean_name = re.sub(r"[^A-Za-z0-9 ]", "", data.request)
        clean_name = "_".join(clean_name.split())

        # Limit filename length
        if len(clean_name) > 30:
            clean_name = clean_name[:30]

        download_name = f"Generated_{clean_name}.docx"

        return FileResponse(
            path=output_file,
            filename=download_name,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )