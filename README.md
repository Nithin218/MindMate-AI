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
MindMateAI is a full-stack application that allows users to interact with an AI chatbot for mental health support. The system rewrites user queries, analyzes emotions, provides CBT-based responses, suggests resources, and ensures ethical compliance before delivering a final answer. The project is built with modularity and extensibility in mind, using Python for the backend and agents, and a modern HTML/CSS/JS frontend for the user interface.

---

## How It Works
1. **User Interaction**: Users interact with a beautiful, responsive chat UI.
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
```
MindMate-AI/
│
├── app.py                  # (Legacy) Streamlit UI (for reference)
├── main.py                 # Main backend server (FastAPI)
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Project metadata
├── setup.py                # Setup script
├── README.md               # Project documentation
│
├── config/
│   └── config.yaml         # Configuration settings
│
├── logs/
│   └── mindmate.log        # Application logs
│
├── research/
│   └── research.ipynb      # Research and prototyping notebook
│
├── src/
│   └── MindMateAI/
│       ├── Agents/
│       │   ├── __init__.py
│       │   ├── cbt_agent.py              # CBT response agent
│       │   ├── emotion_analysis_agent.py # Emotion analysis agent
│       │   ├── ethical_guardian_agent.py # Ethical compliance agent
│       │   ├── mental_health_state.py    # State schema for workflow
│       │   ├── resource_schedule_agent.py# Resource/schedule agent
│       │   ├── rewrite_agent.py          # Query rewriting agent
│       │   └── writer_agent.py           # Final output formatting agent
│       │
│       ├── logger/
│       │   └── __init__.py              # Logging setup
│       │
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── cbt_guide_tool.py        # CBT techniques tool
│       │   ├── emotion_analysis_tool.py # Emotion analysis tool
│       │   ├── ethical_guardian_tool.py # Ethical compliance tool
│       │   ├── resource_schedule_tool.py# Resource scheduling tool
│       │   └── web_search_tool.py       # Web search tool
│       │
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── common.py                # Common utilities
│       │   └── model_loader.py          # LLM/model loader
│       │
│       └── Workflow/
│           ├── __init__.py
│           └── workflow.py              #Workflow logic
│
├── templates/
│   └── index.html           # Main chat UI (HTML/CSS/JS)
│
└── .gitignore               # Git ignore rules
```

---

## Agents & Tools
### Workflow (src/MindMateAI/Workflow/)
- **workflow.py**: Central workflow logic, orchestrates the sequence of agents.

### Agents (src/MindMateAI/Agents/)
- **rewrite_agent.py**: Reformulates user queries for clarity and LLM compatibility.
- **emotion_analysis_agent.py**: Analyzes the emotional content of the query.
- **cbt_agent.py**: Provides CBT-based therapeutic responses.
- **resource_schedule_agent.py**: Suggests helpful resources or schedules.
- **ethical_guardian_agent.py**: Checks for ethical compliance and safety.
- **writer_agent.py**: Formats the final output for the user.
- **mental_health_state.py**: Defines the state schema passed between agents.

### Tools (src/MindMateAI/tools/)
- **cbt_guide_tool.py**: Provides CBT techniques and strategies based on emotion.
- **emotion_analysis_tool.py**: Detects and classifies emotions in text.
- **ethical_guardian_tool.py**: Ensures responses are ethical and safe.
- **resource_schedule_tool.py**: Suggests schedules and resources.
- **web_search_tool.py**: (Optional) Enables web search for additional information.

### Utilities (src/MindMateAI/utils/)
- **model_loader.py**: Loads and configures the LLM (e.g., Groq, OpenAI).
- **common.py**: Shared utility functions.

### Logging (src/MindMateAI/logger/)
- **__init__.py**: Sets up logging for the application.

---

## UI/Frontend
- **templates/index.html**: Modern, responsive chat interface with dark/light mode toggle, scrollable chat, and beautiful design. Handles user input and displays bot responses dynamically.
- **app.py**: (Legacy) Streamlit-based UI for quick prototyping (not used in production).

---

## Backend/API
- **main.py**: Main backend server (FastAPI). Handles POST requests to `/query`, processes user input through the agentic workflow, and returns the AI's response.
- **config/config.yaml**: Stores configuration settings (e.g., API keys, model provider).
- **logs/mindmate.log**: Application logs for debugging and monitoring.

---

## Setup & Installation
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
   - Edit `config/config.yaml` with your API keys and settings as needed.
5. **Run the backend server:**
   ```bash
   python main.py
   ```
6. **Access the UI:**
   - Open your browser and go to `http://localhost:5000` (or the port specified in your backend).

---

## Contributors
- **Nithin**: Frontend/UI design, tools development, and user experience.
- **Likith**: Backend development, agent design, and workflow orchestration.

This project was completed by Likith and Nithin. Likith focused on the backend, agents, and workflow logic, while Nithin built the UI, frontend, and tools.

---

## License
See [LICENSE](LICENSE) for details.

---

*Thank you for using MindMateAI!*
# MindMate-AI