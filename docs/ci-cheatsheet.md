# GitHub Actions cheat sheet (Project 06)

Everything used in this project, with what each part does.

## Workflow file anatomy

| Key | What it does |
|---|---|
| `name: CI` | Name shown in the Actions tab and the badge |
| `on: pull_request` | Run on every pull request (opened, new commits, reopened) |
| `on: push: branches: [main]` | Run on every push to `main`, including merges |
| `permissions: contents: read` | The run's `GITHUB_TOKEN` can only read the repo |
| `concurrency: group: ci-${{ github.ref }}` | Runs on the same branch share a group... |
| `cancel-in-progress: true` | ...and a new run cancels the older one |
| `jobs.<id>.name` | Display name; this is the **check name** branch protection requires |
| `runs-on: ubuntu-latest` | A fresh GitHub-hosted Linux VM for each job |
| `strategy.matrix.python-version: ["3.12", "3.13"]` | One job per value, run in parallel |
| `strategy.fail-fast: false` | One matrix job failing doesn't cancel the others |
| `${{ matrix.python-version }}` | Expression: the current matrix value |
| `defaults.run.working-directory: api` | Every `run:` step starts in `api/` |
| `steps[].uses: owner/action@vN` | Use a published action, pinned to a major version |
| `steps[].with:` | Inputs for that action |
| `steps[].run:` | Shell commands; `|` for several lines |
| `steps[].if: always()` | Run this step even if an earlier one failed |
| `needs: [job]` | Make a job wait for another (not needed here: jobs run in parallel) |

YAML rules: 2-space indents, no tabs. `- item` is a list entry, `key: value` is a map. Quote versions (`"3.12"`, not `3.12`, or `3.10` becomes `3.1`).

## Actions used

| Action | Inputs used | Purpose |
|---|---|---|
| `actions/checkout@v5` | none | Clone the repo onto the runner |
| `actions/setup-python@v6` | `python-version`, `cache: pip`, `cache-dependency-path: api/requirements*.txt` | Install Python; save and restore the pip cache keyed on the requirements files |
| `actions/setup-node@v5` | `node-version: 22`, `cache: npm`, `cache-dependency-path: frontend/package-lock.json` | Same for Node and npm |
| `actions/upload-artifact@v6` | `name`, `path` | Attach files (test reports) to the run. v6 runs on Node 24; v5 gave Node 20 deprecation warnings |

## Test reports

```bash
pytest -v --junitxml=reports/junit-python-3.12.xml
node --test --test-reporter=spec --test-reporter-destination=stdout \
            --test-reporter=junit --test-reporter-destination=reports/junit-frontend.xml
```

Two reporters on `node --test`: readable output in the log, and JUnit XML in a file.

## Where to find things on GitHub

| What | Where |
|---|---|
| All runs | **Actions** tab |
| A run's summary, annotations and artifacts | Actions → the run → **Summary** |
| A failing log line | PR → **Details** next to the red check → expand the ❌ step |
| Re-run | The run → **Re-run all jobs** |
| Required checks | Settings → Branches → edit the `main` rule → **Require status checks to pass** → search each job name |
| Badge URL | `https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg?branch=main` |

## Reading the cache in the log

| Log line (in **Set up Python** / **Set up Node**) | Meaning |
|---|---|
| `pip cache is not found` | Cache miss: packages are downloaded |
| `Cache restored successfully` / `Cache restored from key: setup-python-Linux-...` | Cache hit |
| Post step `Cache saved with key: ...` | The cache was written at the end of a miss run |

## Branch protection used

- Require a pull request before merging
- Require status checks to pass: `API (Python 3.12)`, `API (Python 3.13)`, `Frontend (Node 22)`
- Require branches to be up to date before merging
- Do not allow bypassing the above settings
- **Require approvals: off.** On a one-person repo you can't approve your own PR, so it would block every merge

## Local commands

```bash
nvm install 22 && nvm use 22                      # same Node as CI
cd api && pip install -r requirements-dev.txt && flake8 && pytest
cd frontend && npm ci && npm run lint && npm test
git branch -d <merged-branch> && git fetch --prune  # tidy up after merging
```
