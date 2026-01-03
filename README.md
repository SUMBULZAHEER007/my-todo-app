# AI-Powered Todo App - Hackathon Project

## Project Overview
This project demonstrates a complete AI-powered todo application built in 4 distinct phases as per the hackathon specifications. Each phase builds upon the previous one, showcasing progressive development with AI integration.

## Project Structure
The project is organized into 4 phases, each representing a milestone in the development:

### Phase 1: Basic CRUD & Database
- **Features**: Basic todo management with Create, Read, Update, Delete operations
- **Technology**: FastAPI, SQLAlchemy, SQLite database
- **Functionality**: Add, view, update, and delete tasks with persistent storage
- **Files**: Located in `Phase_1/` directory

### Phase 2: AI Integration - Task Summaries
- **Features**: AI-powered task summaries using Hugging Face models
- **Technology**: Hugging Face Inference API, enhanced FastAPI endpoints
- **Functionality**: Generates 2-sentence summaries of all tasks
- **Files**: Located in `Phase_2/` directory

### Phase 3: Agentic Features - Task Categorization
- **Features**: AI-powered task categorization (Urgent/Work/Personal)
- **Technology**: Enhanced AI model integration with categorization logic
- **Functionality**: Automatically categorizes tasks using AI instead of keyword matching
- **Files**: Located in `Phase_3/` directory

### Phase 4: Complete Solution with UI Branding
- **Features**: Complete AI-powered todo app with RAG, chat, and "Sumbul Zaheer" branding
- **Technology**: Full stack with FastAPI backend, enhanced frontend UI
- **Functionality**: All previous features plus AI chat, RAG implementation, and polished UI
- **Files**: Located in `Phase_4/` directory

## Tech Stack
- **Backend**: FastAPI
- **Database**: SQLAlchemy with SQLite
- **AI Integration**: Hugging Face Inference API
- **Frontend**: HTML/CSS/JavaScript with Tailwind CSS
- **Vector Storage**: Qdrant (in-memory)
- **AI Framework**: LangChain

## Setup Instructions
1. Clone the repository
2. Navigate to the desired phase directory (Phase_1, Phase_2, Phase_3, or Phase_4)
3. Install dependencies: `pip install -r requirements.txt`
4. Set up environment variables (see .env.example)
5. Run the application: `uvicorn main:app --reload`

## Created by: Sumbul Zaheer
This project was developed as part of the Todo Spec-Driven Development Hackathon, showcasing progressive implementation of AI-powered features in a todo application.