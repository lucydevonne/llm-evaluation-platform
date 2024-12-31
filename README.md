# LLM Evaluation Platform

A modern web application for comparing responses from different AI language models side by side. Built with FastAPI and React, this platform allows real-time comparison of Groq's Mixtral-8x7b and HuggingFace's GPT-2 models.

## Features
- 🤖 Real-time AI model comparison
- 📊 Performance metrics tracking (response time, accuracy, relevancy)
- 🎯 Clean, intuitive user interface
- ⚡ Fast, asynchronous API calls
- 🔄 Extensible architecture for adding new models

## Tech Stack
### Backend
- FastAPI (Python)
- SQLAlchemy
- SQLite
- Async HTTP clients

### Frontend
- React 18
- TypeScript
- Material-UI
- Recharts for visualizations
- Axios for API calls

## Quick Start

1. Clone the repository
```bash
git clone https://github.com/lucydevonne/llm-evaluation-platform.git
cd llm-evaluation-platform
```

2. Set up the backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables
Create .env in the backend directory:
```bash
GROQ_API_KEY=your_groq_key_here
HUGGING_FACE_API_KEY=your_huggingface_key_here
```

4. Start the backend server
```bash
uvicorn app.main:app --reload
```

5. Set up the frontend
```bash
cd frontend
npm install
npm start
```

6. Access the application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## License
MIT
EOL




