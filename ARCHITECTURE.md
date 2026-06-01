# AI PPT Designer V2 - System Architecture

## 1. System Architecture

The system follows a Port and Adapters (Hexagonal Architecture) design. This ensures that external dependencies (Database, AI Providers, Authentication, Storage) are abstracted behind interfaces, allowing seamless swapping from local/mock implementations to production services.

### Core Philosophy
* **Source of Truth:** Custom Internal Slide Schema. The schema is framework-agnostic.
* **Rendering:** Fabric.js reads the schema to render the Canvas editor.
* **Exporting:** Python backend reads the schema to generate PPTX via `python-pptx`.
* **State Management:** Backend serves as the absolute source of truth; frontend synchronizes via REST/WebSockets.

### High-Level Components
* **Client (Frontend):** React/Next.js application, handling the Hybrid Editor (Fabric.js), Asset management, and API communication.
* **API Gateway / Backend:** Python-based (e.g., FastAPI) handling authentication, business logic, document parsing, slide generation, and export.
* **Adapters / Providers:**
  * **Auth Provider:** Local Mock -> Google OAuth
  * **LLM Provider:** Local Mock -> DeepSeek API
  * **Image Gen Provider:** Local Mock -> Flux API
  * **Storage Provider:** Local File System -> Supabase Storage (S3 compatible)
  * **Database Provider:** Local PostgreSQL -> Production PostgreSQL

## 2. Frontend Architecture

### Tech Stack
* **Framework:** Next.js (React) - App Router
* **State Management:** Zustand (for editor state, slide schema sync) + React Query (for API data fetching)
* **Canvas Engine:** Fabric.js (wrapped in custom React components)
* **Styling:** Tailwind CSS + Radix UI (or similar headless UI for accessible components)

### Editor Architecture (The "Hybrid" Canvas)
1. **Schema Store (Zustand):** Holds the current Custom Slide Schema (JSON).
2. **Schema-to-Fabric Engine:** A layer that subscribes to the Schema Store, translates it to Fabric.js objects, and renders them.
3. **Fabric-to-Schema Engine:** Listens to user interactions (drag, drop, resize, text edit) on the Fabric canvas, translates them back to schema updates, and updates the Zustand store.
4. **Animation Timeline Context:** Manages the playback state and synchronizes Fabric.js properties with time-based keyframes defined in the schema.

### Core Modules
* **Dashboard:** Project listing, usage tracking, template gallery.
* **Editor Workspace:**
  * Left Sidebar: Asset library, slides thumbnail view, AI prompt interface.
  * Center: Fabric.js Canvas.
  * Right Sidebar: Contextual properties (text formatting, animation settings).
  * Bottom: Advanced Animation Timeline.

## 3. Backend Architecture

### Tech Stack
* **Framework:** FastAPI (Python) - High performance, native async, automatic OpenAPI docs.
* **ORM:** SQLAlchemy (async) + Alembic for migrations.
* **Dependencies:** `python-pptx` (Export), `python-magic` (Security), `PyMuPDF`, `mammoth`, `openpyxl` (Parsing).

### Architecture Layers (Hexagonal)
1. **Controllers / Routers:** FastAPI endpoints (REST).
2. **Services / Use Cases:** Core business logic (e.g., `GeneratePresentationService`, `ExportPPTXService`).
3. **Domain Entities:** Python dataclasses/Pydantic models representing the Custom Slide Schema, Users, Assets, etc.
4. **Ports (Interfaces):**
  * `IAuthProvider`, `ILLMProvider`, `IImageProvider`, `IStorageProvider`.
5. **Adapters:** Implementations of the ports (e.g., `MockLLMAdapter`, `DeepSeekAdapter`).

### Data Flow for AI Generation (e.g., Deep Research Mode)
1. User uploads a PDF and triggers "Deep Research" generation.
2. **Upload Endpoint:** Validates file (magic bytes via `python-magic`), stores in `IStorageProvider`, returns Asset ID.
3. **Parsing Service:** Retrieves file, extracts text via `PyMuPDF`.
4. **Generation Service:** Calls `ILLMProvider` (DeepSeek) with text and context.
5. **Schema Builder:** Translates LLM output into the Custom Slide Schema.
6. **Save & Return:** Persists schema to PostgreSQL, returns JSON to frontend.

## 4. Database Schema

*(Designed for PostgreSQL)*

### `users`
* `id` (UUID, PK)
* `google_id` (String, Unique) - *Nullable during mock auth phase*
* `email` (String, Unique)
* `name` (String)
* `created_at` (Timestamp)
* `last_login` (Timestamp)
* `credits_used` (Int) - *For usage tracking*

### `projects` (Presentations)
* `id` (UUID, PK)
* `user_id` (UUID, FK -> users)
* `title` (String)
* `schema_data` (JSONB) - *The Custom Slide Schema*
* `generation_mode` (Enum: Fast, DeepResearch, Academic, PitchDeck, BusinessReport)
* `theme_id` (UUID, Nullable, FK -> themes)
* `created_at` (Timestamp)
* `updated_at` (Timestamp)

### `assets` (Uploads & Generated Images)
* `id` (UUID, PK)
* `user_id` (UUID, FK -> users)
* `type` (Enum: image, document)
* `mime_type` (String) - *Validated via python-magic*
* `storage_path` (String) - *Path in local storage or Supabase S3*
* `original_filename` (String)
* `size_bytes` (Int)
* `created_at` (Timestamp)

### `templates`
* `id` (UUID, PK)
* `user_id` (UUID, FK -> users, Nullable for Global Templates)
* `title` (String)
* `schema_data` (JSONB)
* `is_public` (Boolean)
* `created_at` (Timestamp)

### `themes` (Theme Intelligence)
* `id` (UUID, PK)
* `name` (String)
* `color_palette` (JSONB)
* `typography` (JSONB)
* `background_styles` (JSONB)

## 5. API Inventory

### Auth (Mock -> Google OAuth later)
* `POST /api/v1/auth/login` - Authenticate and return JWT
* `GET /api/v1/auth/me` - Get current user profile

### Projects & Editor
* `GET /api/v1/projects` - List user projects
* `POST /api/v1/projects` - Create new empty project
* `GET /api/v1/projects/{id}` - Get project schema
* `PUT /api/v1/projects/{id}` - Update project schema (auto-save)
* `DELETE /api/v1/projects/{id}` - Delete project

### AI Generation
* `POST /api/v1/ai/generate` - Trigger AI generation (Fast, Deep Research, etc.). Accepts document IDs and prompt.
* `POST /api/v1/ai/generate-image` - Trigger AI image generation (Flux).

### Assets & Uploads
* `POST /api/v1/assets/upload` - Upload file (Validates magic bytes, extension, MIME, size).
* `GET /api/v1/assets` - List user's asset library.
* `DELETE /api/v1/assets/{id}` - Remove asset.

### Export
* `POST /api/v1/export/{project_id}/pptx` - Translates schema via `python-pptx` and returns a `.pptx` file download URL/stream.

### Templates & Themes
* `GET /api/v1/templates` - Get gallery templates.
* `POST /api/v1/templates` - Save project as a user template.
* `GET /api/v1/themes` - List intelligent themes.

## 6. Folder Structure

```text
ai-ppt-designer/
├── frontend/                     # Next.js Application
│   ├── src/
│   │   ├── app/                  # App router (pages, layouts)
│   │   ├── components/
│   │   │   ├── editor/           # Fabric.js wrappers, Canvas engine
│   │   │   ├── dashboard/
│   │   │   └── ui/               # Reusable UI components (buttons, modals)
│   │   ├── store/                # Zustand stores (editorStore.ts)
│   │   ├── hooks/                # React Query hooks, Custom React hooks
│   │   ├── lib/                  # Schema definitions, Fabric.js adapters
│   │   └── services/             # API client services
│   ├── package.json
│   └── next.config.js
│
├── backend/                      # FastAPI Application
│   ├── app/
│   │   ├── api/                  # Routers / Endpoints
│   │   ├── core/                 # Config, security, exceptions
│   │   ├── domain/               # Pydantic schemas, Custom Slide Schema definitions
│   │   ├── models/               # SQLAlchemy DB models
│   │   ├── ports/                # Interfaces (IAuthProvider, ILLMProvider)
│   │   ├── adapters/             # Implementations (MockLLM, DeepSeek, LocalStorage)
│   │   └── services/             # Business logic (Generation, Export, Parsing)
│   ├── tests/
│   ├── requirements.txt
│   └── main.py
│
├── docker/                       # Local development environment
│   ├── docker-compose.yml        # PostgreSQL database service
│   └── .env.example
│
└── .gitignore
```

## 7. Development Phases

### Phase 1: Foundation & Custom Schema
* Define the Custom Slide Schema specification (JSON structure for shapes, text, images, animations).
* Setup FastAPI backend with Local PostgreSQL and Local Storage.
* Implement `python-magic` security checks and asset upload endpoints.
* Setup Next.js frontend with Zustand for schema state.

### Phase 2: Hybrid Editor Rendering
* Implement Schema-to-Fabric.js rendering engine on the frontend.
* Implement Fabric.js-to-Schema update engine (drag, resize, text edit).
* Build basic UI for the editor workspace.

### Phase 3: Export Engine (The Hard Part)
* Implement the Python backend service that translates the Custom Slide Schema into a `.pptx` file using `python-pptx`.
* Test fidelity against various schema configurations (text styling, grouping, images).

### Phase 4: Mock AI & Document Parsing
* Implement document parsing services (`PyMuPDF`, `mammoth`, `openpyxl`).
* Implement the Adapter pattern for AI Providers.
* Build the Mock LLM Adapter and Mock Image Gen Adapter to simulate DeepSeek and Flux outputs returning valid Custom Slide Schemas.

### Phase 5: Production Integration & Polish
* Swap Mock Auth for Google OAuth.
* Swap Mock LLM for DeepSeek API.
* Swap Mock Image Gen for Flux API.
* Swap Local Storage for Supabase Storage.
* Implement Usage Tracking and Advanced Animation Timeline.
* Final QA for 95% export fidelity.

## 8. Technical Risks

1. **Schema Translation Complexity (High):**
   * *Risk:* Mapping the exact coordinate systems, unit types (EMUs vs Pixels), and styling quirks from Fabric.js/Web to `python-pptx`/Office Open XML is historically very difficult. Achieving 95% fidelity will require meticulous math and transformation logic.
   * *Mitigation:* The Custom Slide Schema is the source of truth. Keep the schema strictly defined and unit-agnostic (or use standard units like percentages or points) to make the math easier for both rendering and exporting.

2. **Advanced Animation Export (High):**
   * *Risk:* Fabric.js animations do not natively map to PowerPoint animations. `python-pptx` has very limited built-in support for advanced slide animations.
   * *Mitigation:* The export service may need to inject custom XML fragments into the generated PPTX directly to support complex animation sequences if `python-pptx` lacks the required high-level API functions.

3. **LLM Schema Hallucination (Medium):**
   * *Risk:* DeepSeek might generate invalid JSON or hallucinate schema properties when generating presentations, breaking the frontend renderer.
   * *Mitigation:* Strict Pydantic validation on the backend before saving/returning the generated schema. Use fallback parsers or prompt engineering to enforce strict JSON schemas.

4. **Document Parsing Consistency (Medium):**
   * *Risk:* User-uploaded PDFs and Word documents can have wildly inconsistent structures, making text extraction garbage.
   * *Mitigation:* Use robust libraries (like `PyMuPDF`) and pass the raw extracted text through a fast LLM pass to clean and structure it before feeding it into the main generation prompt.
