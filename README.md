# Lychee

Lychee is a Flask-based, encyclopedia-style web application focused on truth and factual accuracy.
Users submit articles and the community votes to verify and validate facts, aiming to rival major encyclopedias like Wikipedia.
Optional OpenAI Codex/GPT integration can assist in drafting and refining content.

## Requirements

- Python 3.10 or later
- SQLite 3 (for the default built-in database)

## Local Setup (Beta Testing)

1. **Clone the repository**
   ```bash
   git clone <repo-url> lychee
   cd lychee
   ```

2. **Create and activate a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and set your OPENAI_API_KEY and FLASK_SECRET_KEY
   ```

5. **Initialize the database**
```bash
python3 create_db.py
```

6. **Run the development server**
```bash
python3 main.py
```

*To run on a different port (if 8000 is in use), set the PORT environment variable, e.g.:*
```bash
PORT=8001 python3 main.py
```

## Security notes (portfolio)

- `FLASK_SECRET_KEY` is required (no insecure default). Use a long random value.
- Article content is rendered with Jinja auto-escaping (safe by default). If you later add rich-text HTML/Markdown rendering, you must sanitize to prevent stored XSS.

7. **Open in your browser**
   Visit `http://localhost:8000` (or the host/port printed by Flask).

## Notes

- The `.env` file is listed in `.gitignore` and should not be committed to source control.
- In production (e.g. Cloud Run), set `OPENAI_API_KEY` and `FLASK_SECRET_KEY` via your platform's environment/secret management.

## License

This project is released under the MIT License. See `LICENSE` for details.
