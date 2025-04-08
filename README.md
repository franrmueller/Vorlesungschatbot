# Classroom-Chatbot

[English](#english) | [Deutsch](#deutsch)

<a name="english"></a>
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
- **Orchestration**: ![LangChain](https://img.shields.io/badge/LangChain-Yes-green) (Python)
- **LLM Serving**: ![Ollama](https://img.shields.io/badge/Ollama-Yes-green) (Llama 2)
- **Embedding Model**: Ollama or dedicated service
- **Database**: ![Neo4j](https://img.shields.io/badge/Neo4j-Yes-green) (Graph + Vector Index)
- **Backend**: ![FastAPI](https://img.shields.io/badge/FastAPI-Yes-green) (Python)
- **Frontend**: ![Jinja2](https://img.shields.io/badge/Jinja2-Yes-green) + ![HTML/JS](https://img.shields.io/badge/HTML%2FJS-Yes-green)
- **Containerizing**: ![Docker](https://img.shields.io/badge/Docker-Yes-green) & ![Docker%20Compose](https://img.shields.io/badge/Docker%20Compose-Yes-green)

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

│ └── chat.html # Chat interface 

└── static/ 

│  ├── css/ # Stylesheets 

│ ├── js/ # JavaScript files 

│  └── images/ # Static images
  

JavaScript is used to enhance the templates with dynamic features like real-time chat interactions.


## Potential Enhancements & Future Work
- Support for `.docx`, `.pptx`, `.txt`, URLs.
- Chat history per user/class.
- Feedback (thumbs up/down) on answers.
- Advanced retrieval (e.g., HyDE, query rewriting).
- Graph-native queries (e.g., "How many documents in Class X?").
- Enhanced UI/UX.
- Multi-modal support (e.g., querying images in PDFs).
- Document/class summarization.
- Source transparency with improved citation (exact page numbers, paragraphs, and document sections).
## Installation
1. Clone the repository:
   ```bashhe repository:
   git clone https://github.com/your-username/classroom-chatbot.git
2. Run docker:ttps://github.com/your-username/classroom-chatbot.git
   ```bashker:
   docker compose up --build
   docker compose up --build
## Usage
1. Access the web interface at http://localhost:8000.
3. Create user or login with your credentials.t:8000.
3. Create user or login with your credentials.
## Contributing
1. Fork the repository.
2. Create a new branch for your feature.
3. Commit your changes.for your feature.
4. Push to your branch.
5. Open a pull request.
5. Open a pull request.
## License
See the LICENSE file for details.
See the LICENSE file for details.
---
---
<a name="deutsch"></a>
# Vorlesungschatbot/a>
# Vorlesungschatbot
Ein KI-gestützter Chatbot, der Studierenden ermöglicht, durch direktes Stellen von Fragen zu ihren Kursmaterialien zu lernen. Mit einer modernen RAG-Architektur und Neo4j bietet der Chatbot kontextuell genaue Antworten, die ausschließlich auf Dokumenten basieren, die von verifizierten Professoren für bestimmte Kurse hochgeladen wurden.
Ein KI-gestützter Chatbot, der Studierenden ermöglicht, durch direktes Stellen von Fragen zu ihren Kursmaterialien zu lernen. Mit einer modernen RAG-Architektur und Neo4j bietet der Chatbot kontextuell genaue Antworten, die ausschließlich auf Dokumenten basieren, die von verifizierten Professoren für bestimmte Kurse hochgeladen wurden.
## Inhaltsverzeichnis
- [Vision](#vision-de)
- [Gelöstes Kernproblem](#gelöstes-kernproblem)
- [Hauptfunktionen & Benutzerrollen](#hauptfunktionen--benutzerrollen)
- [Kern-Chatbot-Funktionalität](#kern-chatbot-funktionalität)errollen)
- [Technologie-Stack](#technologie-stack)tbot-funktionalität)
- [Datenbankschema](#datenbankschema)ack)
- [Frontend-Implementierung](#frontend-implementierung)
- [Mögliche Erweiterungen & Zukünftige Arbeiten](#mögliche-erweiterungen--zukünftige-arbeiten)
- [Installation](#installation-de)tige Arbeiten](#mögliche-erweiterungen--zukünftige-arbeiten)
- [Nutzung](#nutzung)tallation-de)
- [Mitwirken](#mitwirken)
- [Lizenz](#lizenz)irken)
- [Lizenz](#lizenz)
<a name="vision-de"></a>
## Visionvision-de"></a>
Einen intuitiven und effizienten KI-gestützten Chatbot zu entwickeln, der Studierenden ermöglicht, durch direktes Stellen von Fragen zu ihren Kursmaterialien zu lernen. Mit einer modernen RAG-Architektur und Neo4j bietet der Chatbot kontextuell genaue Antworten, die ausschließlich auf Dokumenten basieren, die von verifizierten Professoren für bestimmte Kurse hochgeladen wurden.
Einen intuitiven und effizienten KI-gestützten Chatbot zu entwickeln, der Studierenden ermöglicht, durch direktes Stellen von Fragen zu ihren Kursmaterialien zu lernen. Mit einer modernen RAG-Architektur und Neo4j bietet der Chatbot kontextuell genaue Antworten, die ausschließlich auf Dokumenten basieren, die von verifizierten Professoren für bestimmte Kurse hochgeladen wurden.
<a name="gelöstes-kernproblem"></a>
## Gelöstes Kernproblemroblem"></a>
Studierende haben oft Schwierigkeiten, bestimmte Informationen in umfangreichen Kursmaterialien (PDFs) zu finden. Dieser Chatbot bietet eine interaktive Möglichkeit, diese Dokumente direkt abzufragen, spart Zeit und verbessert das Verständnis durch zielgerichtete Antworten auf Basis der bereitgestellten Inhalte.
Studierende haben oft Schwierigkeiten, bestimmte Informationen in umfangreichen Kursmaterialien (PDFs) zu finden. Dieser Chatbot bietet eine interaktive Möglichkeit, diese Dokumente direkt abzufragen, spart Zeit und verbessert das Verständnis durch zielgerichtete Antworten auf Basis der bereitgestellten Inhalte.
<a name="hauptfunktionen--benutzerrollen"></a>
## Hauptfunktionen & Benutzerrollenollen"></a>
## Hauptfunktionen & Benutzerrollen
### Benutzerrollen
- **Administrator**: Systemverantwortlicher.
- **Professor**: Inhaltsanbieter und Kursmanager.
- **Student**: Inhaltsnutzer.ter und Kursmanager.
- **Student**: Inhaltsnutzer.
### Authentifizierung & Autorisierung
- Sichere Anmeldung für alle Rollen mit Passwörtern, die mit `bcrypt` gehasht werden.
- Rollenbasierte Zugriffssteuerung (RBAC) durchgesetzt.e mit `bcrypt` gehasht werden.
- Selbstregistrierung für Studierende.AC) durchgesetzt.
- Admin/Professor-Konten werden über Setup-Skript oder Admin-Oberfläche erstellt.
- Admin/Professor-Konten werden über Setup-Skript oder Admin-Oberfläche erstellt.
### Administrator-Ansicht
- **Benutzerverwaltung**: Erstellung/Verwaltung von Professorenkonten; Einsehen/Verwalten von Studentenkonten (z.B. Deaktivieren, Löschen, Passwort zurücksetzen).
- **Systemstruktur**: Erstellung/Anzeige/Löschung von Kursen; Zuweisung von Professoren zu Kursen (optional: Professoren erstellen ihre eigenen).rt zurücksetzen).
- **Inhaltsaufsicht**: Anzeigen/Entfernen von hochgeladenen PDFs und zugehörigen Kursen bei Bedarf.optional: Professoren erstellen ihre eigenen).
- **Inhaltsaufsicht**: Anzeigen/Entfernen von hochgeladenen PDFs und zugehörigen Kursen bei Bedarf.
### Professor-Ansicht
- **Kursverwaltung**: Erstellung/Verwaltung ihrer Kurse.
- **Inhaltsverwaltung**: Hochladen/Entfernen von PDFs für ihre spezifischen Kurse.
- **Studentenverwaltung**: Anzeige eingeschriebener Studierender; ggf. Entfernung von Studierenden aus einem Kurs.
- **Chatbot-Zugriff**: Testen des Chatbots im Rahmen ihrer Kurse. ggf. Entfernung von Studierenden aus einem Kurs.
- **Chatbot-Zugriff**: Testen des Chatbots im Rahmen ihrer Kurse.
### Studierenden-Ansicht
- **Einschreibung**: Beitritt zu Kursen mittels einzigartiger Codes von Professoren.
- **Kursauswahl**: Anzeige und Auswahl eingeschriebener Kurse.Codes von Professoren.
- **Chatbot-Interaktion**: Stellen von Fragen, die ausschließlich aus Dokumenten des ausgewählten Kurses beantwortet werden, mit Anzeige der Quellinformationen (z.B. PDF-Name, Seitennummer).
- **Chatbot-Interaktion**: Stellen von Fragen, die ausschließlich aus Dokumenten des ausgewählten Kurses beantwortet werden, mit Anzeige der Quellinformationen (z.B. PDF-Name, Seitennummer).
<a name="kern-chatbot-funktionalität"></a>
## Kern-Chatbot-Funktionalitätalität"></a>
## Kern-Chatbot-Funktionalität
### 1. Dokumentenaufnahme & Indexierung (Professor-Upload)
- **Upload**: Professoren laden PDFs hoch, die mit ihren Kursen verknüpft sind.
- **Laden**: PDFs werden mit LangChain's `PyPDFLoader` verarbeitet.knüpft sind.
- **Chunking**: Text wird mit `Sentence-Transformers` in Chunks mit Überlappung aufgeteilt.
- **Einbettung**: Vektor-Einbettungen werden über `OllamaEmbeddings` generiert. aufgeteilt.
- **Speicherung (Neo4j)**:inbettungen werden über `OllamaEmbeddings` generiert.
  - `PDF`-Knoten speichern Metadaten (Titel, Dateiname, Zeitstempel).
  - `PdfChunk`-Knoten speichern Inhalt, Einbettungen und Metadaten (z.B. Seitennummer).
  - Beziehungen: `(:Class)-[:HAS_DOCUMENT]->(:PDF)-[:HAS_CHUNK]->(:PdfChunk)`.nnummer).
- **Vektor-Indexierung**: Neo4j Vector Index auf `embedding_vector` für Ähnlichkeitssuche, gefiltert nach Kurs.
- **Vektor-Indexierung**: Neo4j Vector Index auf `embedding_vector` für Ähnlichkeitssuche, gefiltert nach Kurs.
### 2. Abfragenbearbeitung (Studierenden-Interaktion)
- **Eingabe**: Studierende wählen einen Kurs aus und stellen eine Frage.
- **Query-Einbettung**: Frage wird mit demselben Modell eingebettet.age.
- **Abruf**:nbettung**: Frage wird mit demselben Modell eingebettet.
  - Vektor-Ähnlichkeitssuche in Neo4j, gefiltert auf die `PdfChunk`-Knoten des ausgewählten Kurses.
  - Die relevantesten `k` Chunks werden mit Metadaten abgerufen.nk`-Knoten des ausgewählten Kurses.
- **Generierung**: Prompt mit Frage und Kontext wird über `Chatollama` an `Llama 2` gesendet.
- **Antwort**: Antwort wird mit Quellen-PDF/Seitenzitaten angezeigt.a` an `Llama 2` gesendet.
- **Antwort**: Antwort wird mit Quellen-PDF/Seitenzitaten angezeigt.
<a name="technologie-stack"></a>
## Technology Stacke-stack"></a>
- **Orchestrierung**: ![LangChain](https://img.shields.io/badge/LangChain-Yes-green) (Python)
- **LLM Serving**: ![Ollama](https://img.shields.io/badge/Ollama-Yes-green) (Llama 2)(Python)
- **Embedding Model**: Ollama or dedicated serviceo/badge/Ollama-Yes-green) (Llama 2)
- **Datenbank**: ![Neo4j](https://img.shields.io/badge/Neo4j-Yes-green) (Graph + Vector Index)
- **Backend**: ![FastAPI](https://img.shields.io/badge/FastAPI-Yes-green) (Python)ector Index)
- **Frontend**: ![Jinja2](https://img.shields.io/badge/Jinja2-Yes-green) + ![HTML/JS](https://img.shields.io/badge/HTML%2FJS-Yes-green)
- **Containerisierung**: ![Docker](https://img.shields.io/badge/Docker-Yes-green) & ![Docker%20Compose](https://img.shields.io/badge/Docker%20Compose-Yes-green)
- **Containerisierung**: ![Docker](https://img.shields.io/badge/Docker-Yes-green) & ![Docker%20Compose](https://img.shields.io/badge/Docker%20Compose-Yes-green)
<a name="datenbankschema"></a>
## Datenbankschemaschema"></a>
## Datenbankschema
### Knoten
- `User {uuid, username, password_hash, name, role: ['ADMIN', 'PROFESSOR', 'STUDENT'], created_at}`
- `Class {uuid, name, enrollment_code, created_at, created_by_uuid}`SSOR', 'STUDENT'], created_at}`
- `PDF {uuid, title, source_filename, upload_timestamp, uploaded_by_uuid}`
- `PdfChunk {uuid, chunk_index, content, embedding_vector, source_page}`}`
- `PdfChunk {uuid, chunk_index, content, embedding_vector, source_page}`
### Beziehungen
- `(User {role:'PROFESSOR'})-[:TEACHES]->(:Class)`
- `(User {role:'STUDENT'})-[:ENROLLED_IN {enrolled_at}]->(:Class)`
- `(:Class)-[:HAS_DOCUMENT]->(:PDF)`D_IN {enrolled_at}]->(:Class)`
- `(:PDF)-[:HAS_CHUNK]->(:PdfChunk)`
- `(:PDF)-[:UPLOADED_BY]->(:User {role:'PROFESSOR'})`
- `(:PDF)-[:UPLOADED_BY]->(:User {role:'PROFESSOR'})`
<a name="frontend-implementierung"></a>
## Frontend-Implementierungierung"></a>
## Frontend-Implementierung
Das Frontend wird mit Jinja2-Templates implementiert, die direkt in FastAPI integriert sind. Dieser Ansatz bietet:
Das Frontend wird mit Jinja2-Templates implementiert, die direkt in FastAPI integriert sind. Dieser Ansatz bietet:
- **Server-seitiges Rendering**: Schnell ladende Seiten mit von FastAPI gerenderten Inhalten
- **Einfache Struktur**: HTML-Templates mit eingebettetem JavaScript für Interaktivitätalten
- **Direkte Integration**: Templates werden direkt vom FastAPI-Backend bereitgestelltät
- **Rollenbasierte Benutzeroberfläche**: Unterschiedliche Ansichten für Studierende, Professoren und Administratoren
- **Rollenbasierte Benutzeroberfläche**: Unterschiedliche Ansichten für Studierende, Professoren und Administratoren
Die Template-Struktur folgt dieser Organisation:
Die Template-Struktur folgt dieser Organisation:
app/
app/
├── templates/ 
├── templates/ 
│ ├── base.html # Gemeinsame Layout-Vorlage 
│ ├── base.html # Gemeinsame Layout-Vorlage 
│ ├── index.html # Startseite 
│ ├── index.html # Startseite 
│ ├── login.html # Authentifizierungsseiten 
│ ├── login.html # Authentifizierungsseiten 
│ ├── register.html 
│ ├── register.html 
│ ├── admin/ # Admin-spezifische Ansichten 
│ ├── admin/ # Admin-spezifische Ansichten 
│ ├── professor/ # Professor-spezifische Ansichten 
│ ├── professor/ # Professor-spezifische Ansichten 
│ └── student/ # Studierenden-spezifische Ansichten 
│ └── student/ # Studierenden-spezifische Ansichten 
│ └── chat.html # Chat-Oberfläche 
│ └── chat.html # Chat-Oberfläche 
└── static/ 
└── static/ 
│  ├── css/ # Stylesheets 
│  ├── css/ # Stylesheets 
│ ├── js/ # JavaScript-Dateien 
│ ├── js/ # JavaScript-Dateien 
│  └── images/ # Statische Bilder
   └── images/ # Statische Bilder
JavaScript wird verwendet, um die Templates mit dynamischen Funktionen wie Echtzeit-Chat-Interaktionen zu erweitern.
JavaScript wird verwendet, um die Templates mit dynamischen Funktionen wie Echtzeit-Chat-Interaktionen zu erweitern.
<a name="mögliche-erweiterungen--zukünftige-arbeiten"></a>
## Mögliche Erweiterungen & Zukünftige Arbeiteneiten"></a>
- Unterstützung für `.docx`, `.pptx`, `.txt`, URLs.
- Chat-Verlauf pro Benutzer/Kurs.tx`, `.txt`, URLs.
- Feedback (Daumen hoch/runter) zu Antworten.
- Erweiterter Abruf (z.B. HyDE, Query-Umformulierung).
- Graph-native Abfragen (z.B. "Wie viele Dokumente gibt es in Kurs X?").
- Verbesserte UI/UX.gen (z.B. "Wie viele Dokumente gibt es in Kurs X?").
- Multimodale Unterstützung (z.B. Abfrage von Bildern in PDFs).
- Dokument-/Kurszusammenfassung.. Abfrage von Bildern in PDFs).
- Quellentransparenz mit verbesserter Zitierung (genaue Seitenzahlen, Absätze und Dokumentabschnitte).- Dokument-/Kurszusammenfassung.
sserter Zitierung (genaue Seitenzahlen, Absätze und Dokumentabschnitte).
<a name="installation-de"></a>
## Installation>
1. Klonen Sie das Repository:ation
   ```bash
   git clone https://github.com/your-username/classroom-chatbot.git
2. Führen Sie Docker aus:ne https://github.com/your-username/classroom-chatbot.git
   ```bash
   docker compose up --build   ```bash
-build
<a name="nutzung"></a>
## Nutzung
1. Greifen Sie auf die Weboberfläche unter http://localhost:8000 zu.
3. Erstellen Sie einen Benutzer oder melden Sie sich mit Ihren Anmeldedaten an.1. Greifen Sie auf die Weboberfläche unter http://localhost:8000 zu.
enutzer oder melden Sie sich mit Ihren Anmeldedaten an.
<a name="mitwirken"></a>
## Mitwirken
1. Forken Sie das Repository.
2. Erstellen Sie einen neuen Branch für Ihre Funktion.
3. Commiten Sie Ihre Änderungen.anch für Ihre Funktion.
4. Pushen Sie auf Ihren Branch.
5. Öffnen Sie einen Pull Request.4. Pushen Sie auf Ihren Branch.
ull Request.
<a name="lizenz"></a>
## Lizenz
Siehe LICENSE-Datei für Details.## Lizenz


[def]: https://img.shields.io/badge/Docker%Compose-Yes-green
[def]: https://img.shields.io/badge/Docker%Compose-Yes-green