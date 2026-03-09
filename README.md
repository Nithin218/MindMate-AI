# MindMateAI

MindMateAI is an AI-powered mental health companion designed to provide users with supportive, structured, and ethical responses to their mental health queries. The system leverages advanced LLMs, agentic workflows, and cognitive behavioral therapy (CBT) tools to deliver personalized guidance and emotional support.

---

## Table of Contents
- [Project Overview](#project-overview)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Agents & Tools](#agents--tools)
- [UI/Frontend](#uifrontend)
- [Backend/API](#backendapi)
- [Setup & Installation](#setup--installation)
- [Contributors](#contributors)

---

## Project Overview
MindMateAI is a full-stack application that allows users to interact with an AI chatbot for mental health support. The system rewrites user queries, analyzes emotions, provides CBT-based responses, suggests resources, and ensures ethical compliance before delivering a final answer. The project is built with modularity and extensibility in mind, using Python (FastAPI) for the backend and agents, and a modern React app (Vite + Tailwind CSS) for the frontend interface.

---

## How It Works
1. **User Interaction**: Users interact with a beautiful, responsiveReact chat UI.
2. **Query Handling**: User input is sent to the backend via a `/query` endpoint.
3. **Agentic Workflow**: The backend processes the query through a series of agents:
    - **Rewrite Agent**: Reformulates the query for clarity and LLM compatibility.
    - **Emotion Analysis Agent**: Detects the user's emotional state.
    - **CBT Agent**: Provides therapeutic responses based on emotion.
    - **Resource Schedule Agent**: Suggests helpful resources or schedules.
    - **Ethical Guardian Agent**: Ensures all responses are ethical and safe.
    - **Writer Agent**: Formats the final output for the user.
4. **Response Delivery**: The final answer is returned to the frontend and displayed in the chat.

---

## Project Structure
```text
MindMate-AI/
│
├── main.py                 # Main backend server (FastAPI)
├── app.py                  # (Legacy) Streamlit UI
├── requirements.txt        # Python backend dependencies
├── pyproject.toml          # Project metadata
├── setup.py                # Setup script
├── .env                    # Environment variables (API keys)
├── README.md               # Project documentation
│
├── config/
│   └── config.yaml         # Configuration settings
│
├── frontend/               # Modern React Frontend (Vite + Tailwind)
│   ├── package.json        # Frontend dependencies
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   ├── vite.config.js
│   ├── index.html
│   ├── src/                # React components and assets
│   └── public/
│
├── logs/
│   └── mindmate.log        # Application logs
│
├── research/
│   └── research.ipynb      # Research and prototyping notebook
│
├── src/
│   └── MindMateAI/
│       ├── Agents/         # LangGraph Agent nodes
│       ├── Workflow/       # Core workflow definitions
│       ├── tools/          # LangChain tools for agents
│       ├── utils/          # Common utilities and LLM loaders
│       └── logger/         # Logging setup
│
└── templates/              # (Legacy) Vanilla HTML/JS UI
    └── index.html
```

---

## Agents & Tools
### Workflow (`src/MindMateAI/Workflow/`)
- **workflow.py**: Central workflow logic that orchestrates the sequence of agents using LangGraph.

### Agents (`src/MindMateAI/Agents/`)
- **rewrite_agent.py**: Reformulates user queries for clarity and LLM compatibility.
- **emotion_analysis_agent.py**: Analyzes the emotional content of the query.
- **cbt_agent.py**: Provides CBT-based therapeutic responses.
- **resource_schedule_agent.py**: Suggests helpful resources or schedules.
- **ethical_guardian_agent.py**: Checks for ethical compliance and safety.
- **writer_agent.py**: Formats the final output for the user.
- **mental_health_state.py**: Defines the state schema passed between agents.

### Tools (`src/MindMateAI/tools/`)
- **cbt_guide_tool.py**: Provides CBT techniques and strategies based on emotion.
- **emotion_analysis_tool.py**: Detects and classifies emotions in text.
- **ethical_guardian_tool.py**: Ensures responses are ethical and safe.
- **resource_schedule_tool.py**: Suggests schedules and resources.
- **web_search_tool.py**: Enables web search for additional information.

### Utilities (`src/MindMateAI/utils/`)
- **model_loader.py**: Loads and configures the LLM (e.g., Groq, OpenAI).
- **common.py**: Shared utility functions.

---

## UI/Frontend
- **`frontend/` (Primary UI)**: A modern, responsive React application initiated with Vite and styled using Tailwind CSS. This is the primary user interface configured to interact with the backend API.
- **`templates/index.html` (Legacy)**: Previous robust vanilla HTML/JS chat interface.
- **`app.py` (Legacy)**: Streamlit-based UI for quick prototyping workflows. 

---

## Backend/API
- **`main.py`**: Main backend server built with FastAPI. Handles POST requests to `/query` (and `/health`), processes user input through the agentic workflow, and returns the AI's response while providing CORS support.
- **`config/config.yaml`**: Stores application configuration settings natively.
- **`.env`**: (Ignored in git) Houses sensitive API keys to power the LLM and search functionalities.

---

## Setup & Installation

### 1. Backend Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Nithin218/MindMate-AI.git
   cd MindMate-AI
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment:**
   - Ensure you have a `.env` file in the root directory providing necessary API credentials based on the LLM currently loaded (e.g., `GROQ_API_KEY`, `OPENAI_API_KEY`).
   - Edit `config/config.yaml` with any other specific settings as needed.
5. **Run the backend server:**
   ```bash
   uvicorn main:app --reload
   ```
   *The backend will be available at `http://localhost:8000` or `http://127.0.0.1:8000`.*

### 2. Frontend Setup
1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```
2. **Install Node dependencies:**
   ```bash
   npm install
   ```
3. **Run the development server:**
   ```bash
   npm run dev
   ```
4. **Access the Application:**
   - Open your browser and navigate to the local URL provided by Vite (typically `http://localhost:5173`).

---

## Contributors
- **Nithin**: Frontend/UI design, React implementation, tools development, and user experience.
- **Likith**: Backend development, FastAPI integration, agent design, and workflow orchestration.

This project was completed collaboratively by Likith and Nithin. Likith focused on the robust backend architecture, LLM agents, and data workflow logic, while Nithin designed and built the responsive frontend UI, the modern React stack, and LangChain toolsets.

---

## License
See [LICENSE](LICENSE) for details.

---

*Thank you for using MindMateAI!*