# Classroom-Chatbot

An AI-powered chatbot that empowers students to learn by asking questions directly about their course materials. Leveraging a modern RAG architecture with Neo4j, the chatbot provides contextually accurate answers based solely on documents uploaded by verified professors for specific classes.

## Table of Contents
- [Vision](#vision)
- [Core Problem Solved](#core-problem-solved)
- [Key Features & User Roles](#key-features--user-roles)
- [Core Chatbot Functionality](#core-chatbot-functionality)
- [Technology Stack](#technology-stack)
- [Database Schema](#database-schema)
- [Frontend Implementation](#frontend-implementation)
- [Potential Enhancements & Future Work](#potential-enhancements--future-work)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Vision
To create an intuitive and efficient AI-powered chatbot that empowers students to learn by asking questions directly about their course materials. Leveraging a modern RAG architecture with Neo4j, the chatbot provides contextually accurate answers based solely on documents uploaded by verified professors for specific classes.

## Core Problem Solved
Students often struggle to find specific information within extensive course materials (PDFs). This chatbot provides an interactive way to query these documents directly, saving time and improving comprehension by delivering targeted answers based on the provided content.

## Key Features & User Roles

### User Roles
- **Administrator**: System overseer.
- **Professor**: Content provider and class manager.
- **Student**: Content consumer.

### Authentication & Authorization
- Secure login for all roles with passwords hashed using `bcrypt`.
- Role-based access control (RBAC) enforced.
- Student self-registration.
- Admin/Professor accounts created via setup script or Admin interface.

### Administrator View
- **User Management**: Create/manage professor accounts; view/manage student accounts (e.g., deactivate, delete, reset password).
- **System Structure**: Create/view/delete classes; assign professors to classes (optional: professors create their own).
- **Content Oversight**: View/remove uploaded PDFs and associated classes if necessary.

### Professor View
- **Class Management**: Create/manage their classes.
- **Content Management**: Upload/remove PDFs specific to their classes.
- **Student Management**: View enrolled students; potentially remove students from a class.
- **Chatbot Access**: Test the chatbot scoped to their classes.

### Student View
- **Enrollment**: Join classes using unique codes from professors.
- **Class Selection**: View and select enrolled classes.
- **Chatbot Interaction**: Ask questions answered solely from documents of the selected class, with source info (e.g., PDF name, page number) displayed.

## Core Chatbot Functionality

### 1. Document Ingestion & Indexing (Professor Upload)
- **Upload**: Professors upload PDFs tied to their classes.
- **Loading**: PDFs processed with LangChain's `PyPDFLoader`.
- **Chunking**: Text split into chunks using `Sentence-Transformers` with overlap.
- **Embedding**: Vector embeddings generated via `OllamaEmbeddings`.
- **Storage (Neo4j)**:
  - `PDF` nodes store metadata (title, filename, timestamp).
  - `PdfChunk` nodes store content, embeddings, and metadata (e.g., page number).
  - Relationships: `(:Class)-[:HAS_DOCUMENT]->(:PDF)-[:HAS_CHUNK]->(:PdfChunk)`.
- **Vector Indexing**: Neo4j Vector Index on `embedding_vector` for similarity search, filtered by class.

### 2. Query Handling (Student Interaction)
- **Input**: Student selects a class and asks a question.
- **Query Embedding**: Question embedded with the same model.
- **Retrieval**:
  - Vector similarity search in Neo4j, filtered to the selected class’s `PdfChunk` nodes.
  - Top `k` relevant chunks retrieved with metadata.
- **Generation**: Prompt with question and context sent to `Llama 2` via `Chatollama`.
- **Response**: Answer displayed with source PDF/page citations.

## Technology Stack
- ![LangChain](https://img.shields.io/badge/LangChain-Yes-green)
- ![Ollama](https://img.shields.io/badge/Ollama-Yes-green)
- ![Neo4j](https://img.shields.io/badge/Neo4j-Yes-green)
- ![FastAPI](https://img.shields.io/badge/FastAPI-Yes-green)
- ![React](https://img.shields.io/badge/React-Yes-green)
- ![Docker](https://img.shields.io/badge/Docker-Yes-green)

- **Orchestration**: LangChain (Python)
- **LLM Serving**: Ollama (Llama 2)
- **Embedding Model**: Ollama or dedicated service
- **Database**: Neo4j (Graph + Vector Index)
- **Backend**: FastAPI (Python)
- **Frontend**: React/Vue or Jinja2/Thymeleaf
- **Containerization**: Docker & Docker Compose

## Database Schema

### Nodes
- `User {uuid, username, password_hash, name, role: ['ADMIN', 'PROFESSOR', 'STUDENT'], created_at}`
- `Class {uuid, name, enrollment_code, created_at, created_by_uuid}`
- `PDF {uuid, title, source_filename, upload_timestamp, uploaded_by_uuid}`
- `PdfChunk {uuid, chunk_index, content, embedding_vector, source_page}`

### Relationships
- `(User {role:'PROFESSOR'})-[:TEACHES]->(:Class)`
- `(User {role:'STUDENT'})-[:ENROLLED_IN {enrolled_at}]->(:Class)`
- `(:Class)-[:HAS_DOCUMENT]->(:PDF)`
- `(:PDF)-[:HAS_CHUNK]->(:PdfChunk)`
- `(:PDF)-[:UPLOADED_BY]->(:User {role:'PROFESSOR'})`

## Frontend Implementation

The frontend is implemented using Jinja2 templates integrated directly with FastAPI. This approach provides:

- **Server-Side Rendering**: Fast loading pages with content rendered by FastAPI
- **Simple Structure**: HTML templates with embedded JavaScript for interactivity
- **Direct Integration**: Templates are served directly from the FastAPI backend
- **Role-Based UI**: Different views for students, professors, and administrators

The template structure follows this organization:

app/

├── templates/ 

│ ├── base.html # Common layout template 

│ ├── index.html # Landing page 

│ ├── login.html # Authentication pages 

│ ├── register.html 

│ ├── admin/ # Admin-specific views 

│ ├── professor/ # Professor-specific views 

│ └── student/ # Student-specific views 

│ └── chat.html # Student chat interface 

└── static/ 

  ├── css/ # Stylesheets 

  ├── js/ # JavaScript files 

  └── images/ # Static images

JavaScript is used to enhance the templates with dynamic features like real-time chat interactions.


## Potential Enhancements & Future Work
- Support for `.docx`, `.pptx`, `.txt`, URLs.
- Chat history per user/class.
- Feedback (thumbs up/down) on answers.
- Advanced retrieval (e.g., HyDE, query rewriting).
- Graph-native queries (e.g., "How many documents in Class X?").
- Asynchronous PDF processing with task queues (Celery, RQ).
- Enhanced UI/UX.
- Multi-modal support (e.g., querying images in PDFs).
- Document/class summarization.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/classroom-chatbot.git
2. Run docker:
   ```bash
   docker compose up --build

## Usage
1. Access the web interface at http://localhost:8000.
3. Create user or login with your credentials.

## Contributing
1. Fork the repository.
2. Create a new branch for your feature.
3. Commit your changes.
4. Push to your branch.
5. Open a pull request.

## License
See the LICENSE file for details.