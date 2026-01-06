# WDC Labs AI Backend

Immersive Virtual Office AI System with Multi-Agent Architecture.

## Agents

| Agent | Role | Triggers |
|-------|------|----------|
| **Tolu** | Onboarding Officer | First login, salary, contract, hours |
| **Emem** | Project Manager | Deadline, brief, client, deliverable |
| **Sola** | Technical Supervisor | Submissions, errors, code, technical questions |
| **Kemi** | Career Coach | Help, worried, resume, career advice |

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

3. **Run the server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Test the API:**
   ```bash
   curl http://localhost:8000/health
   ```

## API Endpoints

### Chat
- `POST /chat` - Main chat endpoint (auto-routes to appropriate agent)

### Onboarding
- `POST /assess-bio` - Tolu assesses user's resume/bio and assigns level

### Submissions
- `POST /review-submission` - Sola reviews work (60% rejection rule)
- `POST /interrogate-submission` - Sola's Socratic defense

### Portfolio
- `POST /translate-to-cv` - Kemi translates task to CV bullet point

### Coaching
- `POST /soft-skills-feedback` - Kemi provides communication feedback
- `POST /mock-interview` - Mock interview practice with Kemi

### Chaos
- `POST /generate-interruption` - Generate mid-task client interruption

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Your Google Gemini API key |
| `HOST` | No | Server host (default: 0.0.0.0) |
| `PORT` | No | Server port (default: 8000) |
