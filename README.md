# BrewCart

Online coffee ordering.

- `api/`: Flask API (`/health`, `/menu`, `POST /quote`) with pricing rules in `pricing.py`
- `frontend/`: Express frontend

## Tests

```
cd api && pip install -r requirements-dev.txt && pytest && flake8
cd frontend && npm ci && npm test && npm run lint
```
