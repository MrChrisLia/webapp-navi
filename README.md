# Hermes Security Insights (Local Setup)

This project is now **local-only** (no Docker).

It runs a local backend on `http://localhost:8000` and a Burp extension that syncs Proxy traffic into that backend.

## 1) Clone

```bash
git clone https://github.com/MrChrisLia/hermes-burpsuite-agent.git
cd hermes-burpsuite-agent
```

## 2) Install Prerequisites

You need:

- Python 3.10+
- Java 17+
- Gradle
- Burp Suite

Example (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip openjdk-17-jdk gradle
```

Verify:

```bash
python3 --version
java -version
gradle -v
```

## 3) Configure Environment

Create `.env` (or copy `.env.example`):

```bash
cp .env.example .env
```

### Default mode (no external model login)

Keep:

```bash
HERMES_PROVIDER=mock
```

### Use your authenticated Hermes Agent model runtime

`hermes proxy` is a command group in newer Hermes CLI versions, so running it by itself shows help text. Start the proxy with a subcommand:

```bash
hermes proxy start
```

Optional flags:

```bash
hermes proxy start --provider nous --host 127.0.0.1 --port 8645
```

Sanity-check readiness:

```bash
hermes proxy status
hermes proxy providers
```

Then set in `.env`:

```bash
HERMES_PROVIDER=hermes_agent
HERMES_BASE_URL=http://127.0.0.1:8645/v1
HERMES_MODEL=YOUR_MODEL_NAME
HERMES_API_KEY=
```

Use the exact host/port shown by `hermes proxy start` if you changed defaults.
If you authenticated through Hermes/Codex OAuth, leave `HERMES_API_KEY` blank.

## 4) Start Hermes Backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn hermes_api.main:app --host 0.0.0.0 --port 8000
```

Health check (new terminal):

```bash
curl -sS http://localhost:8000/health
```

For Hermes proxy mode, confirm the response shows:

- `"provider": "hermes_agent"`
- `"base_url": "http://127.0.0.1:8645/v1"` (or your custom proxy URL)
- `"model": "YOUR_MODEL_NAME"`

## 5) Build Burp Extension JAR

```bash
cd burp-extension
gradle clean jar
cd ..
```

JAR path:

`burp-extension/build/libs/hermes-burp-sync-0.1.0.jar`

## 6) Load Extension in Burp

1. Burp -> `Extensions` -> `Installed` -> `Add`
2. Type: `Java`
3. Select: `burp-extension/build/libs/hermes-burp-sync-0.1.0.jar`
4. Open extension tab: `Hermes Insights`

Set backend URL in extension:

`http://localhost:8000`

## 7) First Use

1. In extension scope menu, run `Create Scope`
2. Browse target through Burp Proxy
3. Run:
   - `View App Summary`
   - `Generate Quests`

## 8) Ask Hermes Questions In Burp (Chat Box)

The `Hermes Insights` tab now includes a `Hermes Chat` panel.

1. Keep the backend running (`http://localhost:8000` by default).
2. Load or create the correct scope in the extension.
3. Type a question in the chat input and press `Send` (or Enter).

Notes:

- Chat answers are scoped to the currently selected Hermes scope.
- For real model answers, use `HERMES_PROVIDER=hermes_agent` (or `openai_compatible`) and a working model/proxy config.
- If `HERMES_PROVIDER=mock`, chat still works but returns deterministic mock responses.

## 9) Skills (WSTG + Custom)

Check loaded skills:

```bash
curl -sS 'http://localhost:8000/skills?refresh=true'
```

Custom markdown skills location:

- `hermes_api/skills`

Format reference:

- `hermes_api/skills/README.md`

## 10) Troubleshooting

### No `.jar` after clone

Expected. Build it in `burp-extension` using:

```bash
gradle clean jar
```

### Build error: `records are not supported in -source 12`

Your build is using an old Java source level.

Fix:

1. Ensure Java 17+ is installed and active:
   ```bash
   java -version
   ```
2. Pull latest repo changes:
   ```bash
   git pull
   ```
3. Rebuild:
   ```bash
   cd burp-extension
   gradle clean jar
   ```

### Extension sync fails

Check:

1. Backend is running on `localhost:8000`
2. Health endpoint responds:
   ```bash
   curl http://localhost:8000/health
   ```
3. Extension `Hermes Backend` is exactly `http://localhost:8000`

### `hermes proxy` only prints usage/help

This is expected on newer CLI versions when no subcommand is supplied.

Use:

```bash
hermes proxy start
```

Not:

```bash
hermes proxy
```

### App summary is empty

Usually one of:

1. No Burp traffic captured yet
2. Wrong scope loaded
3. Relevant hosts excluded in domain filter

### Chat does not use your Hermes/OpenRouter model

Check backend config first:

```bash
curl -sS http://localhost:8000/health
```

If `provider` is `mock` or `model` is empty, your env was not loaded correctly.

Fix:

1. Ensure `.env` is in repo root.
2. Restart backend after editing `.env`.
3. Re-check `/health` values before testing chat in Burp.

### Chat returns `404 Not Found` on `/chat/completions`

This usually means one of these:

1. Wrong model name for the selected proxy provider.
2. Wrong provider selected when starting proxy.

Important: `hermes proxy start --provider nous` uses **Nous Portal** credentials/models, not your OpenRouter model picker.

Quick checks:

```bash
hermes proxy status
curl -sS http://127.0.0.1:8645/v1/models
```

Then set `HERMES_MODEL` to an ID returned by `/v1/models`.

If you want OpenRouter-specific models, do not use `--provider nous` unless that model is actually available there.
