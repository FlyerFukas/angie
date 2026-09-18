# Angie

**A Turkish-speaking personal assistant that lives in Telegram.** Ask it what is
on your calendar, have it summarize your inbox, add a task, look up a phone
number, in plain Turkish, from your phone. It runs on your own machine as an
n8n workflow, with Claude as the reasoning engine.

[![License: PolyForm Noncommercial](https://img.shields.io/badge/License-PolyForm%20Noncommercial-orange.svg)](LICENSE)
[![Commercial use: license required](https://img.shields.io/badge/Commercial%20use-license%20required-critical.svg)](COMMERCIAL.md)
[![n8n](https://img.shields.io/badge/n8n-2.30.7-EA4B71?logo=n8n&logoColor=white)](https://n8n.io/)
[![Claude](https://img.shields.io/badge/Claude-Sonnet%205-D97757)](https://www.anthropic.com/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)](#setup)

> 🇹🇷 Türkçe sürüm: [README.tr.md](README.tr.md)
>
> **License:** free for personal and other noncommercial use. Business and
> commercial use requires a separate paid license → [COMMERCIAL.md](COMMERCIAL.md)

---

## What it does

Send a message to your own Telegram bot and Angie answers in Turkish, reaching
for a tool when the question needs real data:

| You write | Angie uses |
|---|---|
| bugün takvimimde ne var | Google Calendar |
| bugünkü maillerimi özetle | Gmail, promotional mail filtered out |
| görevlerim neler | task table |
| yarına rapor yazmayı ekle | task table, insert |
| rapor görevini tamamladım | task table, update |
| Mehmet'in numarası ne | contact table |

It remembers the last 15 messages, so follow-ups like *peki ya yarın* work.

## How it works

```
Telegram  ──►  cloudflared tunnel  ──►  n8n (localhost:5678)
                                          │
                                    identity lock
                                          │
                                     Claude agent
                        ┌─────────────┬───┴────┬─────────────┐
                     tasks        contacts  calendar       gmail
                  (n8n data tables)        (Google OAuth)
                                          │
Telegram  ◄────────────  reply, split into 4096-char chunks
```

Everything except the model call and the Google APIs stays on your machine.
Tasks and contacts live in n8n data tables: no external database, no Airtable
or Baserow account.

## Requirements

- Windows with Node.js 20+ and Python 3.10+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- An Anthropic API key
- A Google Cloud OAuth client, if you want calendar and mail

## Setup

```bash
git clone https://github.com/FlyerFukas/angie.git
cd angie
npm install n8n@2.30.7
```

Download the tunnel binary into `bin/`:

```powershell
Invoke-WebRequest https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe -OutFile bin\cloudflared.exe
```

Tell the generator who you are, then build the workflow:

```powershell
setx ANGIE_TAKVIM_ID "your.address@gmail.com"
py scripts\uret-angie.py
py scripts\uret-workflow.py
```

Start everything and open the editor at `http://localhost:5678`:

```
Angie-Baslat.cmd
```

In the n8n UI, add four credentials: Telegram API, Anthropic API, Google
Calendar OAuth2, Gmail OAuth2. For the Google ones, add this exact redirect URI
to your Google Cloud OAuth client:

```
http://localhost:5678/rest/oauth2-credential/callback
```

Then wire them up and publish:

```powershell
py scripts\baglantilari-kur.py
.\scripts\yayinla.ps1
```

Message your bot once. It replies with your Telegram ID. Lock the bot to it:

```powershell
py scripts\baglantilari-kur.py 123456789
.\scripts\yayinla.ps1
```

## What this project documents

Angie started as the n8n template
[Angie, Personal AI Assistant with Telegram Voice and Text](https://n8n.io/workflows/2462-angie-personal-ai-assistant-with-telegram-voice-and-text/),
but that template targets an older n8n and breaks in several places on 2.x. The
fixes, and the n8n behaviours behind them, are written down here because they
cost real hours to find:

1. **`n8n start --tunnel` is gone in 2.x.** The flag no longer exists, so
   Telegram webhooks need an external tunnel.
2. **Activation is now `publish:workflow` plus a restart.** Setting
   `workflow_entity.active = 1` alone does nothing.
3. **`import:workflow` deactivates a published workflow.** Always publish again
   after importing.
4. **Imported JSON needs an `id` field**, otherwise SQLite rejects it with a NOT
   NULL constraint error.
5. **Webhook registration lands 10-30 seconds after startup.** A `/healthz` 200
   does not mean the webhook path answers yet.
6. **CLI commands clash with a running n8n** over task broker port 5679. Give
   them `N8N_RUNNERS_BROKER_PORT=5680`.
7. **`N8N_EDITOR_BASE_URL` pins the OAuth callback.** Set it to localhost and a
   changing tunnel address no longer breaks Google sign-in.
8. **The Telegram node forces Markdown when `parse_mode` is unset.** In
   `GenericFunctions.js` it silently assigns `Markdown`, so a single underscore
   in a variable name makes Telegram reject the whole message with
   `can't parse entities`. Angie pins HTML and escapes the model output.
9. **The calendar field demands an email-shaped ID.** Google accepts `primary`;
   n8n's regex validation does not, and fails with
   `Calendar parameter's value is invalid`.
10. **`export:nodes` reports misleading versions** for versioned node types. The
    real maximum is in `nodeVersions` inside each node's compiled source.

Fixes carried over from the original template: the session key was hardcoded, so
every conversation shared one memory; the voice branch dropped the session ID;
replies longer than 4096 characters were rejected; a photo message crashed the
voice check.

## Project layout

```
Angie/
├── Angie-Baslat.cmd          start tunnel + n8n
├── Angie-Durdur.cmd          stop both
├── scripts/
│   ├── uret-angie.py         generates the workflow (edit this, not the JSON)
│   ├── baglantilari-kur.py   binds n8n credentials to nodes, sets identity lock
│   ├── angie-baslat.ps1      tunnel + n8n launcher
│   ├── yayinla.ps1           import, publish, restart
│   └── durum.py              prints current state
└── workflows/                generated output, not tracked by git
```

The workflow JSON is a build artifact. Change `scripts/uret-angie.py`, run it,
then run `yayinla.ps1`. Editing the JSON by hand gets overwritten.

## Limits

- Angie answers only while your machine is on and the tunnel is running.
- Cloudflare quick tunnels get a new address on every start. n8n re-registers
  the webhook automatically, so this is handled, but it is not meant for
  long-lived production use.
- Voice messages are not wired up in this version. The original template used
  OpenAI Whisper; since Angie runs on Claude, transcription would need a
  separate provider.
- Some corporate and campus networks block `api.telegram.org` outright. If
  activation fails with a certificate error, check the network before the code.

## Security

Credentials never touch this repository. See [SECURITY.md](SECURITY.md) for
where they live, what the tunnel exposes, and how the identity lock works.

## License

Angie is dual-licensed.

**Noncommercial use is free** under the
[PolyForm Noncommercial License 1.0.0](LICENSE): personal use, hobby projects,
study, research, educational institutions, government bodies and charities. No
permission needed, no notification. Just keep the license and the copyright
notice with the software if you pass it on.

**Commercial use requires a separate paid license.** Running Angie inside a
business, setting it up for a client, embedding it in a product or service, or
reselling it in any form needs written permission first. Terms, the available
license shapes and contact details are in [COMMERCIAL.md](COMMERCIAL.md).
Pricing is negotiable, discounts exist for small teams, and the architecture can
also be bought outright.

The repository being public does not make the software free to commercialize.
If you are unsure whether your case counts as commercial, ask. Answering is
free and quick.
