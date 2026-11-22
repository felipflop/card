# Docs

How this card got designed, not just what it ended up as.

| Where | What's in it |
|---|---|
| [first-principles.md](first-principles.md) | What physics and the requirements force, with numbers: the LC tank, the energy and thickness budgets, the optics. Every decision traces back here. |
| [decisions/](decisions/) | One short record per design decision: the context, what I picked, and what it costs me. Numbered, never rewritten once accepted. |
| [log/](log/) | A dated build log. What I did that day, what I measured, what surprised me. |
| [research/](research/) | Notes from datasheets and papers that fed the decisions: sourcing, LED colours, solar, feature ideas. |
| [explorations/](explorations/) | Interactive pages I built to compare options before committing. Open them in a browser. |
| [media/](media/) | Schematic renders for the README, rebuilt by `make docs`. |

The flow is: first principles set the limits, research finds parts that fit them, that turns into a decision record, the decision gets built, and the build log says what happened when it met reality. When a later decision replaces an earlier one, the old record gets marked superseded and links to the new one.
