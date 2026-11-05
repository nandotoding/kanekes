# Kanekes

Kanekes is a modular web app for small office-work automation tools. The first available tool is **Phone Number Cleanser**.

## Features

- Clean plain-text contact rows.
- Normalize common Indonesian mobile formats (`08...`, `8...`, `+62...`, `62...`).
- Keep unusual numeric strings rather than silently discarding them.
- Expand multiple numbers in one input row into multiple output rows.
- Remove rows that do not contain a detectable numeric token.
- Copy or download the cleaned result.
- English-language responsive interface.

## Project structure

```text
kanekes/
├── api/
│   └── index.py
├── tools/
│   └── phone_cleanser.py
├── templates/
│   └── index.html
├── static/
│   ├── css/styles.css
│   └── js/app.js
├── main.py
├── requirements.txt
├── vercel.json
└── README.md
```

## Run locally

Python 3.10+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000.

## Deploy to Vercel

1. Push this project to a GitHub repository.
2. In Vercel, choose **Add New → Project** and import the repository.
3. Keep the project root as the repository root.
4. Deploy. Vercel uses `vercel.json` and `api/index.py` to serve the FastAPI application.

The app is stateless: submitted text is processed in memory and is not written to a database or file.

## Add another tool

Keep each tool's processing logic in its own module under `tools/`. Then:

1. Add a route in `main.py` (or move routes into a dedicated router module).
2. Add a tool card in `templates/index.html`.
3. Add the tool's interface and client-side behavior in `static/`.

For a larger collection, create one `APIRouter` per tool (for example, `tools/pdf_tool.py`) and include it in `main.py`. The shared layout and deployment configuration can remain unchanged.

## Phone cleanser behavior notes

- Leading list numbering such as `1.` or `2)` is removed.
- Hyphen-separated leading descriptions are discarded by retaining the last non-empty text segment associated with the numbers.
- A trailing hyphen before a number preserves the preceding name (for example, `John Doe - 0812...`).
- Every detected number is emitted as a separate row with the same name.
- Numeric candidates currently require at least seven digits. Shorter digit strings are treated as text, not phone-number candidates.
- Number formats outside the Indonesian `08`, `8`, `+62`, and `62` patterns are retained as their digit sequence.
