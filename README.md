# TrustLens

TrustLens is an Android-first cybersecurity application for detecting social-engineering manipulation in SMS, email, and chat messages. Its Flutter client calls a FastAPI API that authenticates users, calculates an explainable Trust Score, and persists scan history in MongoDB.

## Features

- JWT registration, login, protected profile, and secure mobile token storage
- Real analysis for urgency, threats, authority, impersonation, credential and financial requests, suspicious URLs, prizes, and emotional pressure
- Explainable 0–100 Trust Score: 80–100 low, 50–79 medium, 0–49 high risk
- Scan history and complete previous-result views
- Demo messages are analyzed by the same backend engine

## Architecture

`Flutter Android app → FastAPI → preprocessing → NLP/detection rules → Trust Score → MongoDB`

The detection service has a structured, explainable NLP fallback enabled by default. Set `NLP_MODEL_ENABLED=true` only after adding a compatible locally hosted DistilBERT classifier; the app never claims DistilBERT is active otherwise.

## Structure

```text
mobile/       Flutter Android application
backend/app/  FastAPI routers, security, detector, database
backend/tests/ backend tests
```

## Setup

1. Copy `.env.example` to `backend/.env` and supply a strong `JWT_SECRET` and local MongoDB or MongoDB Atlas `MONGODB_URI`.
2. Create a Python virtual environment, install `backend/requirements.txt`, then run `uvicorn app.main:app --reload --port 8000` from `backend/`.
3. From `mobile/`, run `flutter pub get`, then `flutter run`. The Android emulator defaults to `http://10.0.2.2:8000`; configure a LAN address in the app for a physical phone.

## API

| Endpoint | Purpose |
|---|---|
| `GET /api/health` | Health check |
| `POST /api/auth/register`, `/login` | Authentication |
| `GET /api/auth/me` | Authenticated profile |
| `POST /api/analyze` | Analyze and persist a scan |
| `GET /api/history`, `GET/DELETE /api/history/{id}` | Scan history |

## Security and limitations

Passwords are bcrypt-hashed; secrets remain in environment variables; protected APIs validate bearer JWTs; URLs are never opened or executed. Detection is a transparent heuristic NLP fallback and cannot prove a message is safe. A production deployment should add a calibrated DistilBERT classifier, rate limiting, HTTPS, email verification, and device-attestation controls.

## Tests

Run `pytest` in `backend/`, then `flutter analyze` and `flutter test` in `mobile/` after Flutter is installed.
