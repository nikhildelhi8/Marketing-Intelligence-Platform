# NOTES.md

Design decisions, deferred choices, and known edge cases — recorded per the
project's Definition of Done ("open decisions are documented, not resolved
prematurely").

---

## Phase 1 — `utils/`

### `utils/transforms.py`

#### `chunked` — eager vs. lazy validation of `size`
- **Decision:** `size <= 0` currently raises `ValueError` *lazily* — i.e. only
  once the generator is actually iterated (`for chunk in chunked(...)`), not
  at the moment `chunked(...)` is called.
- **Why this matters:** because `chunked` is a generator function, none of
  its body runs until iteration starts. A caller could call
  `chunks = chunked(data, 0)` and see no error at all — the `ValueError` only
  fires later, at the `for` loop, which can be far away from the actual
  mistake in the code and makes the stack trace less useful for debugging.
- **Deferred alternative:** split into a normal (non-generator) outer
  function that validates `size` immediately and raises eagerly, delegating
  the actual chunking logic to an inner generator (`_chunked_impl`). Not
  implemented yet — revisit if lazy validation ever causes a confusing bug
  in practice.

#### `flatten` — `isinstance` guard on nested items
- **Decision:** kept the runtime `isinstance(item, Iterable)` check even
  though the type hint (`Iterable[Iterable[T]]`) already promises every
  element of `nested` is itself iterable.
- **Why:** type hints are a *static* contract (checked by mypy, not
  enforced at runtime). Nothing stops a caller — especially one working
  with dynamically-loaded data (e.g. from JSON) — from passing in a mix of
  flat and nested items. The guard trades a small amount of runtime
  overhead for graceful degradation instead of a `TypeError` crash on
  `yield from item` when the contract is violated.
- **Status:** deliberate choice, not a default. Revisit if profiling ever
  shows this check matters for performance at scale.

### `utils/formatting.py`

#### `format_currency` — return value on `None`/empty-string input
- **Decision:** currently returns `"$0.00"` (with a `logger.warning`) when
  given `None` or `""`.
- **Open concern:** `"$0.00"` is visually indistinguishable from a genuine
  zero-dollar value in an exported report — a stakeholder reading a CSV
  can't tell "this campaign spent nothing" from "the data was broken and
  we silently substituted a fallback."
- **Alternatives under consideration:**
  1. Return `None` — but this changes the function's contract from
     `-> str` to `-> str | None`, pushing `None`-handling onto every
     caller (Phase 10 exporters, Phase 11 CLI display).
  2. Return an unmistakable sentinel string (e.g. `"N/A"`) — keeps the
     `-> str` contract simple for all callers, while making broken data
     visually obvious in reports.
- **Status:** not yet decided. Decide before Phase 10 (reporting) starts
  consuming this function, since that's where the choice actually has
  consequences.

#### `format_currency` — type hint vs. actual defensive behavior
- **Observation:** signature is `def format_currency(value: float) -> str`,
  but the function defensively checks for `None` and `""`, which the type
  hint says can never occur.
- **Status:** unresolved — either widen the signature to be honest
  (`value: float | str | None`) or drop the defensive check and trust the
  type contract. Related to the `flatten` guard decision above; same
  underlying question (trust static types vs. defend at runtime).

#### `safe_int` — strict vs. lenient parsing of decimal-looking strings
- **Question:** should `safe_int("12.5")` fail (current behavior — Python's
  `int()` cannot parse decimal strings directly) or succeed by truncating
  (`int(float("12.5")) == 12`)?
- **Status:** deferred. Decision depends on what the actual Kaggle CSV
  numeric columns look like (e.g. do integer-semantic fields like follower
  counts ever appear as `"1234.0"`?). To be resolved by inspecting the raw
  dataset before Phase 3 ingestion is built.

#### `safe_float` — silent `NaN` / `Infinity` parsing
- **Issue:** Python's `float()` accepts the strings `"nan"` and `"inf"`
  (case-insensitive) without raising — so `safe_float("NaN")` returns an
  actual floating-point `NaN` instead of failing loudly. If a CSV uses
  `"NaN"` as a missing-value placeholder (common in exported datasets),
  this `NaN` can silently propagate into downstream arithmetic (e.g.
  budget/ROI calculations), producing corrupted results with no error
  raised anywhere.
- **Status:** known issue, not fixed yet. This is the same failure mode
  Phase 9's blueprint explicitly warns about ("Silent NaN propagation")
  — it's just visible two phases earlier, at the ingestion boundary.
  Revisit when building `analytics/metrics.py`, or sooner if it causes a
  visible bug during Phase 3 ingestion testing.

#### `parse_percentage` — logging responsibility
- **Question:** `parse_percentage` delegates parsing to `safe_float`, which
  already logs a warning (with the raw failing value) on failure. Should
  `parse_percentage` also log its own warning on top of that?
- **Trade-off:** a second log line is redundant if it repeats the same
  information, but adds value if it records *calling context* (which
  higher-level function failed, not just which low-level parser) — useful
  when debugging from logs alone in production.
- **Status:** currently logs a second message on failure. Revisit whether
  the message should be enriched with context (e.g. which field/column was
  being parsed) rather than just restating that parsing failed.