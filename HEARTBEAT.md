# HEARTBEAT.md - Periodic Check-ins

_Things to check when you wake up on a heartbeat. Keep this lean._

## Checklist

<!-- Add items below. Comment out or remove items to skip them. -->

- [ ] Check conversations for unanswered messages
- [ ] Follow up on anything you promised to do

## When to Reach Out

- Someone asked a question you haven't answered
- Something interesting happened worth sharing
- It's been a long time since you talked to your owner

## When to Stay Quiet

- Late night (23:00–08:00) unless urgent
- Nothing new since your last check
- You just checked recently

## State Tracking

Track check state in `memory/heartbeat-state.json` to avoid redundant work:

```json
{
  "lastChecks": {},
  "lastProactiveAt": null
}
```

---

_Update this file as you learn what's worth checking. Remove noise._
