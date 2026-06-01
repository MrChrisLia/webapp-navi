# Hermes Security Insights (Beginner Setup)

This guide is for a brand-new machine where you only have:

- Burp Suite
- Docker Desktop

Goal: run Hermes in Docker, load the Burp extension, and start getting automatic app summaries + quests from your Burp traffic.

## 1) Clone the Repo (No GitHub Login)

From a fresh VM:

```bash
git clone https://github.com/MrChrisLia/webapp-navi.git
cd webapp-navi
```

Important:

- This only works without login if the repo is public.
- If the repo is private, `git clone` will require authentication.

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

## 3) Build the Burp Extension JAR

Important: the `.jar` is not stored in GitHub. You must build it after cloning.

### Option A (Recommended: Docker only, no Java/Gradle install)

```bash
docker run --rm \
  -v "$PWD":/work \
  -w /work/burp-extension \
  gradle:8.10-jdk17 \
  gradle clean jar
```

### Option B (If you already have Gradle + JDK installed)

```bash
cd burp-extension
gradle clean jar
cd ..
```

JAR output path:

`burp-extension/build/libs/hermes-burp-sync-0.1.0.jar`

## 4) Load the Burp Extension

In Burp:

1. Go to `Extensions` -> `Installed` -> `Add`
2. Extension type: `Java`
3. Select `hermes-burp-sync-0.1.0.jar`
4. Confirm it loads successfully

## 5) Configure Burp + Hermes Tab

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

## 6) Capture Traffic

In Burp, browse the target app using Burp’s browser (or your own browser through Burp proxy).

As new traffic appears in Burp Proxy history, Hermes auto-syncs request/response pairs to Docker backend.

Then use:

- `View App Summary` -> `Run`
- `Generate Quests` -> `Run`

You should see readable analysis in the insights panel.

## 7) Confirm Skills Loaded

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

## 8) Common Issues

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

### I cloned it but there is no `.jar`

This is expected. Build it using Step 3 Option A (Docker command), then load:

`burp-extension/build/libs/hermes-burp-sync-0.1.0.jar`

### Build error: `Could not find method java()` in `build.gradle`

This is caused by Gradle-version differences on some VMs.

Fix:

1. Pull latest repo changes:
   ```bash
   git pull
   ```
2. Rebuild with Docker-based Gradle (recommended):
   ```bash
   docker run --rm \
     -v "$PWD":/work \
     -w /work/burp-extension \
     gradle:8.10-jdk17 \
     gradle clean jar
   ```

### Build error: `records are not supported in -source 12`

Your VM is compiling with an old Java source level.

Fix:

1. Pull latest repo changes:
   ```bash
   git pull
   ```
2. Build with Docker Gradle + JDK 17:
   ```bash
   docker run --rm \
     -v "$PWD":/work \
     -w /work/burp-extension \
     gradle:8.10-jdk17 \
     gradle clean jar
   ```

### No results in summary

Usually one of:

1. No traffic captured yet
2. Wrong scope selected
3. Hosts excluded in domain filter

## 9) Add Your Own Skills

Drop `.md` skill files into:

- Host path: `hermes_api/skills`
- Container path: `/app/hermes_api/skills`

Skill format reference:

- `hermes_api/skills/README.md`

Reload skills without restart:

```bash
curl -sS 'http://localhost:8000/skills?refresh=true'
```

## 10) Useful Commands

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
