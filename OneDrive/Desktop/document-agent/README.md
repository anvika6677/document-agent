# 🤖 Autonomous Document Agent

An AI-powered multi-agent document generation system that automatically creates structured Microsoft Word documents from natural language requests. The system uses a **Planner Agent** to design the document outline and a **Worker Agent** to generate high-quality content for each section, orchestrated through a FastAPI backend with an interactive web interface.

---

# 📌 Features

- Multi-Agent Architecture
  - Planner Agent
  - Worker Agent
  - Orchestrator

- AI-powered document generation

- Dynamic user input through web interface

- Automatic Microsoft Word (.docx) generation

- FastAPI REST API

- Interactive HTML/CSS/JavaScript frontend

- Robust JSON parsing for LLM responses

- Automatic fallback across multiple OpenRouter free models

- Timestamp-based document storage

- Error handling and validation

- Optimized to use only **2 AI API calls** per document generation

---

# 🏗️ System Architecture

```
                    +----------------------+
                    |       User           |
                    +----------+-----------+
                               |
                               |
                               v
                +------------------------------+
                | HTML / CSS / JavaScript UI   |
                +--------------+---------------+
                               |
                               |
                               v
                      FastAPI Backend
                               |
                               |
                               v
                    +------------------+
                    |   Orchestrator   |
                    +------------------+
                      |            |
          Step 1      |            | Step 2
                      |            |
                      v            v
              Planner Agent    Worker Agent
                      |            |
         Generates Outline   Generates Content
                      |            |
                      +------+-----+
                             |
                             v
                    Document Writer
                             |
                             v
              Microsoft Word (.docx)
                             |
                             v
                      Download to User
```

---

# 📁 Project Structure

```
document-agent/

├── agents/
│   ├── planner.py
│   └── worker.py
│
├── prompts/
│   ├── planner_prompt.py
│   └── worker_prompt.py
│
├── services/
│   ├── llm_service.py
│   └── document_writer.py
│
├── schemas/
│   └── document_request.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── utils/
│   └── json_parser.py
│
├── outputs/
│
├── app.py
├── orchestrator.py
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙️ Technologies Used

- Python 3.x
- FastAPI
- OpenRouter API
- OpenAI Python SDK
- HTML
- CSS
- JavaScript
- Jinja2
- python-docx
- python-dotenv

---

# 🚀 Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into the project directory

```bash
cd document-agent
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

```env
OPENROUTER_API_KEY=your_api_key_here
```

Obtain a free API key from:

https://openrouter.ai

---

# ▶️ Running the Project

Start the FastAPI server

```bash
uvicorn app:app --reload
```

Open your browser

```
http://127.0.0.1:8000
```

---

# 📝 Example Usage

User Request

```
Create a comprehensive business plan for an online grocery delivery startup.
```

Planner Agent generates

```
[
    "Executive Summary",
    "Company Overview",
    "Market Analysis",
    "Products and Services",
    "Marketing Strategy",
    "Financial Plan",
    "Conclusion"
]
```

Worker Agent generates detailed content for each section.

Finally, the system produces a downloadable Microsoft Word document.

---

# 🌐 API Endpoints

## Home Page

```
GET /
```

Returns the web interface.

---

## Generate Document

```
POST /generate-document
```

Request Body

```json
{
    "request": "Create a business proposal for a coffee shop."
}
```

Response

```
Microsoft Word (.docx)
```

---

# 🔄 Workflow

1. User enters a document request.

2. FastAPI sends the request to the Orchestrator.

3. Planner Agent creates the document outline.

4. Worker Agent generates content for each section.

5. Document Writer creates a formatted Microsoft Word document.

6. The document is returned to the user for download.

---

# 📊 AI Workflow

```
User Request
      │
      ▼
Planner Agent
      │
      ▼
Document Sections
      │
      ▼
Worker Agent
      │
      ▼
Generated Content
      │
      ▼
Document Writer
      │
      ▼
Word Document (.docx)
```

---

# ✨ Key Design Decisions

- Multi-agent architecture for modularity.
- Planner and Worker responsibilities are separated.
- Robust JSON parser handles inconsistent LLM outputs.
- Uses multiple OpenRouter free models with automatic fallback.
- Optimized to minimize API usage by generating the entire document in only **2 LLM calls** (1 Planner + 1 Worker).
- Timestamped output files prevent overwriting previous documents.

---

# 📸 Screenshots

Add screenshots here after running the project.

Example:

- Home Page
- Document Generation in Progress
- Generated Word Document

---

# 🔮 Future Enhancements

- PDF document generation
- Rich text formatting
- Cloud deployment
- User authentication
- Document templates
- AI-generated document titles
- Multi-language document generation
- Document history management

---

# 👨‍💻 Author

Developed as part of an AI Agent assignment using Python, FastAPI, OpenRouter, and a Multi-Agent Architecture.

---

# 📄 License

This project is developed for educational purposes.