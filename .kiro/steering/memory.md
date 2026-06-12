# Project Memory - Faceless Football Content

This file maintains context and key decisions across Kiro sessions. Update it manually after important conversations.

## Current Project State
- **Project**: Faceless Football Content Production
- **Focus**: Raúl Jiménez video content pipeline
- **Status**: Active development

## Key Decisions & Learnings
1. **Skills installed**: 19 global skills from taste-skill and ECC (content-engine, video-editing, etc.)
2. **Hardware limitations**: 2015 Intel MacBook (8GB RAM) → local LLMs not feasible
3. **Primary tools**: Kiro/Claude for main work, Ollama for basic local tasks (if needed)
4. **Git workflow**: `gtc` alias for quick commits (timestamped), `gcp` for version-numbered commits

## Workflow Patterns
- Video footage → indexing → clipping → captioning → publishing
- Using Python scripts in `raul-jimenez-project/scripts/`
- Content strategy focused on World Cup/player narratives

## Recent Conversations
- Installed global skills (~/.kiro/skills/)
- Discussed local LLM limitations on current hardware
- Explored free remote LLM options (Groq, Together AI)
- Set up git aliases (`gtc`, `gcp`)

## Next Actions
1. Develop video content pipeline
2. Create more project-specific steering files
3. Consider free API services for programmatic LLM access

## Reference Commands
- `gtc` = git add, commit with timestamp, push
- `gcp` = git add, commit with version number, push to main
- `ollama run phi3:3.8b-mini-instruct-q4_K_M` = run local Phi-3 model

---
*Last updated: 2026-06-12*

To update: Add new learnings under appropriate sections, remove outdated info.