# PocketSmart AI

PocketSmart AI is a FastAPI + Jinja2 web application based on the supplied project documentation. It provides three budget planners:

- Home Interior: furniture/decor recommendations across IKEA, Amazon and Flipkart.
- Party Planning: food, venue/accommodation and decoration planning using Swiggy, Zomato and OYO-style links.
- Jewelry: occasion/style recommendations with an optional outfit image upload.

The app includes registration/login, JWT cookie authentication, recommendation history, an optional Gemini integration, and deterministic fallback recommendations when no Gemini API key is configured or the AI request fails.

## Windows / VS Code setup

1. Open this folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Run:

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and change `SECRET_KEY`.
5. Gemini is optional. To enable it, put your API key in `GEMINI_API_KEY`.
6. Start the app:

```powershell
python -m uvicorn app.main:app --reload
```

7. Open http://127.0.0.1:8000

## Useful URLs

- `/` home page
- `/register` registration
- `/login` login
- `/dashboard` dashboard
- `/home-planner`
- `/party-planner`
- `/jewelry-planner`
- `/history`
- `/docs` FastAPI API documentation
- `/health` health check
- `/startup` startup/configuration check

## API planner endpoints

- `POST /generate-home`
- `POST /generate-party`
- `POST /generate-jewelry`
- `GET /recommendation/{id}`

## Important

Keep the terminal running while using the website. If you close the terminal or press Ctrl+C, `127.0.0.1:8000` will stop responding.
