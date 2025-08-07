# URL Risk Predicter

A full-stack application that predicts the risk level of a given URL using machine learning and heuristic analysis. This project demonstrates modern web development, backend API design, and practical cybersecurity applications.

## Features
- **URL Risk Scoring:** Analyze and score URLs for potential phishing, malware, or suspicious activity.
- **Modern Frontend:** Responsive React + Tailwind CSS interface for user-friendly interaction.
- **Python Backend:** FastAPI backend for risk analysis and ML integration.
- **Extensible Architecture:** Modular codebase for easy feature expansion.

## Tech Stack
- **Frontend:** React, TypeScript, Tailwind CSS, Vite
- **Backend:** Python, FastAPI
- **Other:** Docker (optional), Jupyter Notebooks (for ML prototyping)

## Project Structure
```
url-risk-predicter/
  ├── backend/         # FastAPI backend and ML logic
  ├── frontend/        # React frontend
  ├── notebooks/       # Jupyter notebooks for ML experiments
  └── README.md
```

## Getting Started

### Prerequisites
- Node.js (v16+)
- Python (3.8+)
- pip
- (Optional) Docker

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Usage
1. Start the backend server.
2. Start the frontend dev server.
3. Open the frontend in your browser and enter a URL to analyze its risk.
