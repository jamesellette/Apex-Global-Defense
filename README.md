# Apex Global Defense (AGD)

<div align="center">

🛡️ **Enterprise Defense Simulation & Strategic Planning Platform**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.12-green)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-19-61DAFB)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)](https://fastapi.tiangolo.com/)

</div>

---

## Overview

Apex Global Defense (AGD) is an enterprise-level defense simulation and strategic planning platform designed for:

- **Military Strategists** - Comprehensive conflict modeling and wargaming
- **Defense Analysts** - Order of battle data and force assessments
- **Intelligence Professionals** - OSINT integration and analysis tools
- **Security Planners** - Multi-domain threat assessment and response planning

### Core Capabilities

- 🗺️ **Global Map Integration** - Multi-layer visualization with Mapbox GL
- 📊 **Military Database** - Order of battle for top 50+ nations
- ⚔️ **Scenario Planning** - Create and simulate conflict scenarios
- 🤖 **AI-Assisted Analysis** - Optional AI features with fallback modes
- 👥 **Multi-User Collaboration** - Role-based access control
- 📁 **Project Management** - Organize analyses and scenarios

### Warfare Domains Covered

| Domain | Capabilities |
|--------|-------------|
| **Conventional** | Land, Air, Sea force modeling |
| **CBRN** | Nuclear, Biological, Chemical analysis |
| **Cyber** | Infrastructure mapping, attack vectors |
| **Asymmetric** | Insurgent/guerrilla modeling |
| **Terror Response** | Vulnerability assessment, response protocols |

---

## Tech Stack

### Frontend
- **React 19** with TypeScript
- **Vite** for build tooling
- **Mapbox GL** for mapping
- **Zustand** for state management
- **React Query** for data fetching
- **React Router** for navigation

### Backend
- **Python 3.12** with FastAPI
- **PostgreSQL** with PostGIS
- **SQLAlchemy** ORM
- **JWT Authentication**
- **Pydantic** for validation

### Infrastructure
- **Docker** & Docker Compose
- **Kubernetes** ready (air-gapped optional)

---

## Quick Start

### Prerequisites

- Node.js 20+
- Python 3.12+
- Docker & Docker Compose
- PostgreSQL 15+ (or use Docker)

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/apex-global-defense.git
   cd apex-global-defense
   ```

2. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Or run manually:**

   **Backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

   **Frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/api/v1/docs

### Environment Variables

Create `.env` files in both `backend/` and `frontend/`:

**Backend (.env):**
```env
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=agd
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=apex_global_defense
SECRET_KEY=your_secret_key
DEBUG=true
```

**Frontend (.env):**
```env
VITE_API_URL=http://localhost:8000
VITE_MAPBOX_TOKEN=your_mapbox_token
```

---

## Project Structure

```
apex-global-defense/
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Page components
│   │   ├── layouts/       # Layout components
│   │   ├── services/      # API services
│   │   ├── store/         # Zustand state management
│   │   ├── types/         # TypeScript types
│   │   └── hooks/         # Custom React hooks
│   └── package.json
│
├── backend/               # Python FastAPI backend
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core config & security
│   │   ├── db/           # Database session & seeds
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic
│   ├── tests/
│   └── requirements.txt
│
├── database/              # Database scripts
│   └── init/             # Initialization SQL
│
├── docker-compose.yml     # Development Docker setup
└── build_sheet.md         # Full specification document
```

---

## API Documentation

Once running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

### Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /api/v1/auth/register` | Register new user |
| `POST /api/v1/auth/login` | Login and get JWT |
| `GET /api/v1/countries` | List all countries |
| `GET /api/v1/countries/{id}` | Get country with military data |
| `GET /api/v1/projects` | List user's projects |
| `POST /api/v1/projects` | Create new project |
| `GET /api/v1/ai/config` | Get AI configuration |
| `POST /api/v1/ai/analyze` | Perform AI analysis |

---

## Development Phases

### Phase 1: MVP ✅ (Current)
- [x] Global map integration
- [x] Top 50 nation military database
- [x] Basic scenarios
- [x] User auth & project management
- [x] AI configuration UI

### Phase 2: Simulation Core
- [ ] Conventional simulation engine
- [ ] Wargaming mode
- [ ] Probability modeling
- [ ] AI-assisted scenario builder

### Phase 3: Domain Expansion
- [ ] Cyber module
- [ ] CBRN modeling
- [ ] Insurgent tools
- [ ] Terror planning module

### Phase 4: Enterprise
- [ ] Multi-user collaboration
- [ ] Intel feed integration
- [ ] External system API
- [ ] Mobile app

---

## Security & Compliance

- **Classification Handling** - Support for unclassified through classified builds
- **Audit Logging** - All actions are logged
- **RBAC** - Role-based access control (Admin, Analyst, Reviewer, Commander, Viewer)
- **FedRAMP Path** - Architecture supports IL4-IL6 compliance

⚠️ **IMPORTANT**: AI features process data through external services. Do not use with classified information.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Military data sourced from open sources (GlobalFirepower, SIPRI, etc.)
- Map tiles provided by Mapbox
- Built with React, FastAPI, and PostgreSQL

---

<div align="center">
<strong>Apex Global Defense</strong> - Strategic Intelligence Platform

Built for defense professionals by defense professionals.
</div>
