# CV Optimizer

A small toolkit for analyzing CVs (résumés) and job descriptions, and generating tailored cover letters.

This repository contains a Streamlit web app and a Jupyter notebook used during development.

## What is in this project

- `cv_optimizer_app.py` — Streamlit application for uploading a CV and a job description (PDF or TXT), performing keyword matching, a simple semantic retrieval using ChromaDB, and generating a cover letter via Ollama.
- `cv_optimizer.ipynb` — Development notebook with the original data exploration, helper functions and experiments.
- `data/` — (optional) folder for sample CVs or job descriptions.
- `requirements.txt` — minimal list of Python packages needed to run the app locally.
- `.gitignore` — recommended ignores for virtual environments and temporary files.

## What I changed / implemented

- Migrated the interactive CLI/menu from the notebook into a Streamlit app (`cv_optimizer_app.py`).
- Added a simple text-splitting helper to avoid an unnecessary dependency for basic chunking.
- Integrated ChromaDB usage for storing and querying CV/job chunks (requires `chromadb`).
- Integrated callouts to Ollama for LLM-driven analysis and cover letter generation (requires an Ollama model installed locally).
- Made the app robust to PDF and TXT uploads and fixed several text-decoding issues.
- Added safety around environment reporting (removed accidental display of local interpreter/pip output).

## Quick start (local)

1. Install Python 3.12 on your system (recommended for compatibility with all dependencies).
2. From the project root create and activate a virtual environment (example for Windows PowerShell):

```powershell
py -3.12 -m venv venv
& .\venv\Scripts\Activate.ps1
python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt
```

3. Run the Streamlit app:

```powershell
python -m streamlit run cv_optimizer_app.py
```

4. Open the URL printed by Streamlit (typically `http://localhost:8501`).

## Notes and prerequisites

- ChromaDB: used as an on-disk vector store. Installing some versions may require build tools on Windows if prebuilt wheels are not available.
- Ollama: the app calls `ollama.generate(...)`. You need Ollama installed and a compatible local model (e.g. `llama3.2`) configured if you want LLM features to work.
- If you prefer not to install `chromadb` or `ollama`, you can still use the basic keyword-matching features of the app.

## How to push to GitHub

If you want to add these files to the GitHub repo `https://github.com/BerkayBeratBayram/cv-optimizer`, run:

```bash
git add README.md .gitignore requirements.txt
git commit -m "Add README, .gitignore and requirements"
git remote add origin https://github.com/BerkayBeratBayram/cv-optimizer.git
git branch -M main
git push -u origin main
```

If the remote is already set, skip the `git remote add` step.

## Next steps (optional)

- Add a simple example CV and job posting to `data/` so users can try the app instantly.
- Add unit tests for parsing and keyword extraction.
- Add an option to run without ChromaDB (in-memory embeddings + nearest-neighbor search) for easier setup.

---

If you want, I can push these changes to the GitHub repository for you (I will need your permission and remote credentials), or I can run the git commands locally here and you can push. Which do you prefer?
