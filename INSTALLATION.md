# Installation

This skill follows the [Agent Skills](https://agentskills.io) open standard: the same `SKILL.md` file is read natively by Claude Code, Cursor, Gemini CLI, and Google Antigravity, each scanning its own skills directory.
Pick the destination path(s) below for whichever tool(s) you use — the skill's content is identical everywhere, only the install location differs.

For every tool, the same three install methods apply, just with a different destination path:

- Plain clone, globally for all projects (personal/global path below).
- Project-local clone, inside a specific repo (project path below).
- As a git submodule, if the host project wants version pinning and to track updates via `git submodule update` (same project path, via `git submodule add` instead of `git clone`).

## Claude Code

Project:

```
git clone https://github.com/CFDEMproject/cfdem-assistant .claude/skills/cfdem-assistant
```

Personal (all projects):

```
git clone https://github.com/CFDEMproject/cfdem-assistant ~/.claude/skills/cfdem-assistant
```

Claude Code auto-discovers `SKILL.md` from either location — no further configuration needed.

## Cursor

Project:

```
git clone https://github.com/CFDEMproject/cfdem-assistant .agents/skills/cfdem-assistant
```

Personal (all projects):

```
git clone https://github.com/CFDEMproject/cfdem-assistant ~/.agents/skills/cfdem-assistant
```

Cursor also reads `.claude/skills/` directly, so a Claude Code install (above) is picked up by Cursor automatically — no separate install needed if you've already installed it for Claude Code in the same project.

## Gemini CLI

Project:

```
git clone https://github.com/CFDEMproject/cfdem-assistant .agents/skills/cfdem-assistant
```

Personal (all projects):

```
git clone https://github.com/CFDEMproject/cfdem-assistant ~/.agents/skills/cfdem-assistant
```

Gemini CLI also accepts `.gemini/skills/cfdem-assistant` (project) or `~/.gemini/skills/cfdem-assistant` (personal) instead, but `.agents/skills/` takes precedence if both are present.

## Google Antigravity

Project:

```
git clone https://github.com/CFDEMproject/cfdem-assistant .agents/skills/cfdem-assistant
```

Personal (all projects):

```
git clone https://github.com/CFDEMproject/cfdem-assistant ~/.gemini/config/skills/cfdem-assistant
```

Antigravity's personal/global path is the one outlier here — it doesn't match Cursor's or Gemini CLI's `~/.agents/skills/`.

## Other Agent Skills-compatible tools

Any other tool implementing the same open standard (e.g. Codex CLI, GitHub Copilot) can be pointed at this repo the same way — check that tool's own documentation for its skills directory, then clone or submodule this repo into it.

## Using alongside Aspherix Assistant

For a coupled CFD-DEM case, install both this skill and [Aspherix Assistant](https://github.com/CFDEMproject/aspherix-assistant) the same way, side by side (e.g. `.claude/skills/cfdem-assistant` and `.claude/skills/aspherix-assistant`) — each tool's skill discovery picks up both automatically, no extra configuration needed to use them together.
