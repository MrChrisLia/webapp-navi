# Hermes Security Insights (Beginner Setup)

This guide is for a brand-new machine where you only have:

- Burp Suite
- Docker Desktop

Goal: run Hermes in Docker, load the Burp extension, and start getting automatic app summaries + quests from your Burp traffic.

## 1) Get the Project Files

Use either option:

1. `git clone` the repo (if Git is installed), or
2. Download ZIP from GitHub and extract it.

Open a terminal in the project root (the folder containing `docker-compose.yml`).

## 2) Start Hermes with Docker

Run:

```bash
docker compose up -d --build
```

Verify backend is healthy:

```bash
curl -sS http://localhost:8000/health
```

Expected: JSON with `"status":"ok"`.

## 3) Load the Burp Extension

Extension JAR path:

`burp-extension/build/libs/hermes-burp-sync-0.1.0.jar`

In Burp:

1. Go to `Extensions` -> `Installed` -> `Add`
2. Extension type: `Java`
3. Select `hermes-burp-sync-0.1.0.jar`
4. Confirm it loads successfully

## 4) Configure Burp + Hermes Tab

Open the extension tab in Burp (`Hermes Insights`).

Set:

- `Hermes Backend`: `http://localhost:8000`
- Leave `Auto Sync Running` checked
- Scope is menu-driven:
  - `Load Scope`
  - `Save Scope As...`
  - `Create Scope`
  - `Delete Scope`

Recommended first step:

1. Choose `Create Scope` -> `Run`
2. Enter a scope name like `My First Test`

## 5) Capture Traffic

In Burp, browse the target app using Burp’s browser (or your own browser through Burp proxy).

As new traffic appears in Burp Proxy history, Hermes auto-syncs request/response pairs to Docker backend.

Then use:

- `View App Summary` -> `Run`
- `Generate Quests` -> `Run`

You should see readable analysis in the insights panel.

## 6) Confirm Skills Loaded

Hermes includes WSTG + markdown skills and applies them per scope output.

Check loaded skills:

```bash
curl -sS 'http://localhost:8000/skills?refresh=true'
```

Check current scope summary includes skills:

```bash
curl -sS 'http://localhost:8000/app-summary/My%20First%20Test'
```

Look for:

- `wstg_recommended_skills`
- `wstg_recommended_skill_details`

## 7) Common Issues

### Backend won’t start on port 8000

Another app is using `8000`. Find/stop it, or remap compose port.

### Burp browser shows no internet / proxy issues

Usually a local port conflict (often `8080`).
If another app uses `8080`, change Burp proxy listener and browser proxy to a free port (for example `8081`), and keep them aligned.

### Extension says sync failed

Check:

1. Docker backend is running: `docker compose ps`
2. Health endpoint works: `curl http://localhost:8000/health`
3. `Hermes Backend` field in Burp is exactly `http://localhost:8000`

### No results in summary

Usually one of:

1. No traffic captured yet
2. Wrong scope selected
3. Hosts excluded in domain filter

## 8) Add Your Own Skills

Drop `.md` skill files into:

- Host path: `hermes_api/skills`
- Container path: `/app/hermes_api/skills`

Skill format reference:

- `hermes_api/skills/README.md`

Reload skills without restart:

```bash
curl -sS 'http://localhost:8000/skills?refresh=true'
```

## 9) Useful Commands

Start:

```bash
docker compose up -d --build
```

Stop:

```bash
docker compose down
```

Logs:

```bash
docker compose logs -f hermes
```

Open shell in container:

```bash
docker compose exec hermes sh
```
