# Sumbul Zaheer - AI Agent Todo App

A sophisticated todo application with AI-powered features, built using FastAPI, SQLAlchemy, and Hugging Face models.

## Hackathon Phases

This project follows the 4-phase Hackathon Spec with progressive development:

### Phase 1: CRUD Operations
- Basic Create, Read, Update, Delete functionality
- Database integration with SQLAlchemy
- Simple API endpoints
- No AI features

### Phase 2: AI Integration
- Added AI Summary functionality
- Fixed the 'AI is currently unavailable' error
- Implemented proper error handling
- Added 2-sentence summary generation

### Phase 3: Agentic Features
- Implemented auto-categorization of tasks
- Tasks automatically tagged as 'Work', 'Personal', or 'Urgent'
- Enhanced AI functionality with keyword-based categorization
- Smart task processing

### Phase 4: Branding 'Sumbul Zaheer'
- Professional UI with 'Sumbul Zaheer' branding
- Modern, responsive design with Slate and Indigo color palette
- Complete documentation
- Production-ready code with all features

## Features

- **AI-Powered Task Management**: Automatically categorizes tasks as Work, Personal, or Urgent
- **Smart Summaries**: Generates intelligent summaries of your tasks using LLMs
- **AI Assistant**: Interactive chat interface to ask questions about your tasks
- **Modern UI/UX**: Clean, responsive design with Slate and Indigo color palette
- **Full CRUD Operations**: Create, read, update, and delete tasks
- **Real-time Updates**: UI updates automatically when tasks change

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript with Tailwind CSS
- **Database**: SQLite
- **AI Integration**: Hugging Face Inference API
- **Vector Storage**: Qdrant for RAG functionality

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SUMBULZAHEER007/my-todo-app.git
   ```

2. Navigate to the project directory:
   ```bash
   cd my-todo-app
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Create a `.env` file in the root directory with your Hugging Face token:
   ```
   HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
   ```

7. Run the application:
   ```bash
   python main.py
   ```

8. Open your browser and go to `http://127.0.0.1:8000`

## Usage

1. Add tasks using the "Add Task" form
2. Mark tasks as complete/incomplete using the checkboxes
3. Delete tasks using the trash icon
4. Click "Regenerate Summary" to get an AI-generated summary of your tasks
5. Use the "AI Assistant" button to chat with the AI about your tasks

## AI Features

### Auto-Categorization
Tasks are automatically categorized based on keywords:
- **Work**: meetings, projects, reports, emails, presentations, clients
- **Personal**: family, friends, shopping, appointments, doctors
- **Urgent**: urgent, asap, immediately, today, now, critical, important

### Smart Summaries
The AI generates a 2-sentence overview of your tasks and suggests the next best action.

### AI Assistant
Ask questions about your tasks and get intelligent responses based on your current todo list.

## API Endpoints

- `GET /` - Home page with the todo app interface
- `POST /todos` - Create a new todo
- `GET /todos` - Get all todos
- `GET /todos/{id}` - Get a specific todo
- `PUT /todos/{id}` - Update a specific todo
- `DELETE /todos/{id}` - Delete a specific todo
- `POST /api/tasks/summary` - Get AI-generated task summary
- `POST /api/chat` - Chat with the AI assistant

## Environment Variables

- `HUGGINGFACEHUB_API_TOKEN` - Your Hugging Face API token for AI model access

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI for the excellent web framework
- Hugging Face for the AI models
- Qdrant for vector storage
- Tailwind CSS for styling