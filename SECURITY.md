# Security Policy

## API keys are never stored in this repository

Angie reads every credential from n8n's own encrypted database on your machine.
Nothing is hardcoded, and no key ever reaches a file in this repo.

| Credential | Where it lives |
|---|---|
| Telegram bot token | n8n credential store (`~/.n8n/database.sqlite`, encrypted) |
| Anthropic API key | n8n credential store |
| Google OAuth client ID + secret | n8n credential store |
| Google access + refresh tokens | n8n credential store |

The encryption key sits in `~/.n8n/config` and is tied to your machine. Both
that folder and `node_modules/` are excluded by `.gitignore`.

The generated workflow files (`workflows/*.json`) are also excluded, because
they embed your Telegram user ID, your calendar address, and n8n credential
references. The generator script `scripts/uret-angie.py` is what ships instead,
and it reads personal values from environment variables:

```
setx ANGIE_TAKVIM_ID   "your.address@gmail.com"
setx ANGIE_TELEGRAM_ID "123456789"
```

If you fork this project you use **your own** bot, **your own** API keys and
**your own** quota.

## The tunnel exposes your whole n8n instance

Telegram delivers messages over a webhook, so n8n has to be reachable from the
internet. The setup here uses a Cloudflare quick tunnel, and that tunnel
forwards **every** path, not just the webhook, including the n8n sign-in page.

Practical consequences:

- Use a strong n8n password and enable MFA from the n8n user settings.
- The tunnel address changes on every start and is not published anywhere, but
  treat it as public: quick tunnel URLs are not a secret.
- For anything long-lived, put n8n behind a reverse proxy that only forwards
  `/webhook/*`, or host it on a server with proper access control.
- Stop the tunnel when you are not using it (`Angie-Durdur.cmd`).

## Only one Telegram account can talk to the bot

A bot token is effectively a password: anyone holding it can message your bot.
Angie therefore checks the sender against `izinli_id` and silently ignores
everyone else. Leave that value empty on first run and the bot replies with your
own Telegram ID so you can lock it down.

If a token leaks, revoke it through BotFather with `/revoke` and create a new
one. The old token stops working immediately.

## Your data stays on your machine

Tasks, contacts and conversation memory live in n8n data tables inside
`~/.n8n/database.sqlite`. Nothing is uploaded anywhere except the model requests
Angie makes on your behalf:

- Message text goes to Anthropic for the reply.
- Calendar and Gmail queries go to Google under the OAuth scopes you granted.

Grant the narrowest Google scopes you can live with, and remember that Gmail
access means the model can read message contents you ask it to summarize.

## Reporting a vulnerability

Open an issue describing the problem. Please do not include real tokens, real
message contents, or your tunnel address in the report.
