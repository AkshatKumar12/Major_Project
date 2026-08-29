# Work logs

Each teammate keeps a running log in `docs/logs/<name>.md`. Add an entry
at the end of every work session — takes under a minute.

## Format

```markdown
## YYYY-MM-DD
- Worked on: <file(s) or task>
- Blocked on: <anything, or "nothing">
- Next: <what you'll do next session>
- Time spent: <rough estimate>
```

## Rules

- One entry per session, even short ones. A 20-minute debugging session
  is still worth a line.
- Reference the log in your commit message when it matches, e.g.
  `git commit -m "dedup: content hash comparison (see docs/logs/akshat.md)"`
- Don't backfill. If you missed a day, just start again — an honest gap
  is more useful information than a padded log.
- Logs get checked weekly, not daily. This isn't surveillance, it's a
  paper trail — for your own memory as much as anyone else's.
