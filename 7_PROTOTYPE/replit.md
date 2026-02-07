# Health Innovators - AI-Based IVR Healthcare Triage System

## Overview

Health Innovators is an AI-powered Interactive Voice Response (IVR) simulation system designed to triage healthcare requests through a web interface. Users interact with a wizard-style flow that mimics an IVR call system — pressing 1 for Emergency or 2 for Non-Emergency — and the system collects patient details, symptoms, and medical history. An AI decision engine (powered by OpenAI) analyzes non-emergency cases and may reclassify them as emergencies. Emergency cases receive prioritized appointment booking with unique token generation.

The application follows a full-stack TypeScript architecture with a React frontend and Express backend, backed by PostgreSQL via Drizzle ORM.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend (client/)
- **Framework**: React 18 with TypeScript, bundled by Vite
- **Routing**: Wouter (lightweight client-side router) with three main pages: Home (`/`), Emergency (`/emergency`), Non-Emergency (`/non-emergency`)
- **State Management**: TanStack React Query for server state; local React state for wizard form steps
- **UI Components**: shadcn/ui (new-york style) built on Radix UI primitives, styled with Tailwind CSS
- **Animations**: Framer Motion for wizard step transitions and page entries
- **Form Handling**: React Hook Form with Zod validation via @hookform/resolvers
- **Design Pattern**: Multi-step wizard flows (WizardStep component) for both emergency and non-emergency paths. The Home page simulates IVR-style input (type "1" or "2" to navigate).
- **Path aliases**: `@/` maps to `client/src/`, `@shared/` maps to `shared/`

### Backend (server/)
- **Framework**: Express 5 on Node.js, running with tsx in development
- **API Design**: REST API with routes defined in `server/routes.ts`. API contracts (paths, input schemas, response schemas) are shared between client and server via `shared/routes.ts`
- **AI Integration**: OpenAI client configured via Replit AI Integrations environment variables (`AI_INTEGRATIONS_OPENAI_API_KEY`, `AI_INTEGRATIONS_OPENAI_BASE_URL`). Used for triage analysis of non-emergency cases.
- **Database**: PostgreSQL via Drizzle ORM. Connection pool managed in `server/db.ts`. Schema defined in `shared/schema.ts`.
- **Storage Pattern**: Repository pattern via `IStorage` interface in `server/storage.ts`, implemented by `DatabaseStorage` class.
- **Dev Server**: Vite dev server runs as middleware in development (`server/vite.ts`); static files served in production (`server/static.ts`)
- **Build**: Custom build script (`script/build.ts`) uses Vite for client and esbuild for server, outputting to `dist/`

### Shared Layer (shared/)
- `shared/schema.ts` — Drizzle table definitions and Zod schemas for the `triage_sessions` table. Also defines TypeScript types for API requests/responses and AI analysis results.
- `shared/routes.ts` — API contract definitions with paths, HTTP methods, input schemas, and response schemas. Includes a `buildUrl` helper for parameterized routes.
- `shared/models/chat.ts` — Additional Drizzle tables (`conversations`, `messages`) for a chat/voice feature provided by Replit integrations.

### Database Schema
Single primary table:
- **triage_sessions**: Stores all triage data including type (emergency/non_emergency), status, patient info (name, phone), issue description, symptoms array, age, gender, pregnancy/child flags, medication details, AI analysis results (JSONB), unique token, and timestamp.

Secondary tables (from Replit integrations):
- **conversations**: Chat conversation records
- **messages**: Individual chat messages linked to conversations

### Key API Endpoints
- `POST /api/triage` — Create a new triage session
- `PATCH /api/triage/:id` — Update an existing triage session (add patient details, symptoms, etc.)
- `GET /api/triage/:id` — Retrieve a triage session
- `POST /api/triage/:id/analyze` — Trigger AI analysis on a session

### Replit Integrations (server/replit_integrations/)
Pre-built modules for audio/voice chat, text chat, image generation, and batch processing. These use OpenAI via Replit's AI integration proxy. They are available but not all are actively used in the main triage flow.

## External Dependencies

- **PostgreSQL** — Primary database, connected via `DATABASE_URL` environment variable. Uses `pg` driver with Drizzle ORM. Schema migrations managed via `drizzle-kit push`.
- **OpenAI API** (via Replit AI Integrations) — Powers the AI triage analysis engine. Configured through `AI_INTEGRATIONS_OPENAI_API_KEY` and `AI_INTEGRATIONS_OPENAI_BASE_URL` environment variables.
- **Key npm packages**:
  - `drizzle-orm` + `drizzle-zod` — ORM and schema validation
  - `express` v5 — HTTP server
  - `@tanstack/react-query` — Client-side data fetching
  - `framer-motion` — Animations
  - `react-hook-form` + `zod` — Form validation
  - `wouter` — Client-side routing
  - `shadcn/ui` + `@radix-ui/*` — UI component library
  - `openai` — OpenAI SDK
  - `connect-pg-simple` — Session storage (available but not actively used for auth)