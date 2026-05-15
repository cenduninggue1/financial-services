# Claude for Office — Direct Cloud Setup

Admin tooling for configuring the Claude Office add-in to call your own cloud
(Vertex AI, Bedrock, or an LLM gateway) instead of Anthropic's API.

## Install

```bash
claude plugin marketplace add anthropics/financial-services-plugins
claude plugin install claude-for-msft-365-install@financial-services-plugins
```

Then inside the session: `/claude-for-msft-365-install:setup`

## Commands

| Command | What it does |
|---|---|
| `/claude-for-msft-365-install:setup` | Interactive wizard — provisions cloud resources, admin consent, writes manifest |
| `/claude-for-msft-365-install:manifest` | Generate the customized add-in manifest XML |
| `/claude-for-msft-365-install:consent` | Azure admin consent URL for the add-in's app registration |
| `/claude-for-msft-365-install:update-user-attrs` | Write per-user config via Microsoft Graph extension attributes |
| `/claude-for-msft-365-install:bootstrap` | Build the bootstrap endpoint — per-user MCP servers, skills, dynamic config |

## Notes (personal)

- I'm using this with **Bedrock** (us-east-1) — skipping the Vertex AI steps in the setup wizard.
- The `bootstrap` command is the most useful one for my setup; run it after any user config changes.
- TODO: figure out if `update-user-attrs` needs re-consent when adding new Graph scopes.
