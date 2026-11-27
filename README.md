# BrewCart

[![CI](https://github.com/Aviral-Rohan/devops-project-06-github-actions-ci/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Aviral-Rohan/devops-project-06-github-actions-ci/actions/workflows/ci.yml)

Online coffee ordering.

- `api/`: Flask API (`/health`, `/menu`, `POST /quote`) with pricing rules in `pricing.py`
- `frontend/`: Express frontend

## How our CI works

Every pull request, and every push to `main`, runs [`.github/workflows/ci.yml`](.github/workflows/ci.yml) on GitHub-hosted Ubuntu runners:

| Job | Steps |
|---|---|
| API (Python 3.12) and API (Python 3.13) | install → `flake8` → `pytest` → upload JUnit report |
| Frontend (Node 22) | `npm ci` → `npm run lint` (eslint) → `npm test` (node --test) → upload JUnit report |

- The jobs run in parallel. The API job runs once per Python version (a matrix).
- pip and npm downloads are cached, keyed on `api/requirements*.txt` and `frontend/package-lock.json`.
- Test reports are attached to every run as artifacts, even when tests fail.
- `main` is protected: all three checks must pass before a pull request can be merged.

If a check fails, open the pull request → **Details** next to the red check → expand the step with ❌ and read its last lines.

## Run the checks locally

```
cd api && pip install -r requirements-dev.txt && flake8 && pytest
cd frontend && npm ci && npm run lint && npm test
```