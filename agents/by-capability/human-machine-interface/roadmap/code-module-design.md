# Code Module Design: A Guide-Spec Checker for Chat (Design Note, No Code)

> **Status:** proposed design note. It describes a module that does not exist and that this repository will not contain. Written 2026-10-20. No code, no results, no measured claims.

This note is for the repository owner and for whoever builds the later code. It says what a separate code module would read, where it would run, what it must never do, and which test conversations it must pass.

**Research:** 0 web searches. Everything below comes from files in this repository: the Guide spec blocks in `goals/*/failures/*.md`, [conversation-event-schema-v0.1.md](specs/conversation-event-schema-v0.1.md), [failure-taxonomy-v1.md](specs/failure-taxonomy-v1.md), and `tests/README.md`.

## 1. Purpose in one paragraph

Each pattern page ends with a **Guide spec** block, labeled "fixed format for later code; derived from this page, no invented thresholds". The module would load those blocks, look at a conversation, and report which pattern, if any, a draft reply or a finished turn may be showing, and which move from the page's Moves table applies. The pattern page stays the source of truth. The module only reads it.

## 2. What the module reads

### 2.1 The Guide spec (one per pattern page)

At the time of writing, 61 pages under `goals/` carry one Guide spec block (61 `pattern_id:` lines, 61 `status: proposed` lines). Each is a fenced `yaml` block under the heading line "**Guide spec**". There is no wire format beyond that block.

### 2.2 The conversation event schema

[Conversation event schema v0.1](specs/conversation-event-schema-v0.1.md) describes one turn as one event. Its groups are: core fields (`conversation_id`, `turn_index`, `timestamp`, `channel`, `speaker`, `event_type`, `text`, `text_redaction`), chat bot-turn fields (`bot.*`), user-turn labels (`user_label.*`), context fields, request/stream/error fields, handoff/verification/action/payment fields, and session-end fields. Chat fields are specified. Voice and web fields are PLANNED only; the module must not detect or report them.

### 2.3 Pattern IDs

A Pattern ID is the pattern file name without `.md` (taxonomy v1). The module treats an ID as valid only if it appears in the taxonomy.

## 3. The Guide spec format as it is actually used

Fields found in all 61 blocks, in the order the pages write them:

| Field | What the pages put there |
|---|---|
| `pattern_id` | The page's file name without `.md`. All 61 match their file names. |
| `runs` | Where the check runs: `pre_send` (45), `conversation` (14), `post_turn` (2). |
| `reads` | A bracketed list of dotted field names the check needs. |
| `trigger` | One plain sentence, for example "a handoff or channel switch is about to be sent". No thresholds. |
| `moves` | A bracketed list of move names from the page's Moves table. |
| `choices` | Menu options for `offer_choices`, or `none`, or `[]`. |
| `on_miss` | What to do when the check fails: `rewrite` (48), `handoff` (8), `log` (4), `ask` (1). |
| `metric` | The page's primary metric, as a phrase. |
| `counter_metric` | The metric that catches over-correcting. |
| `status` | `proposed` on every page. |

Move names in use: `hand_off`, `lead_with_answer`, `offer_choices`, `admit_uncertainty`, `ask_clarifying_question`, `ask_one_question` (one page).

### 3.1 Inconsistencies between pages

The module needs a tolerant reader, or the pages need a cleanup pass by the owner. Found by grep:

1. **`reads` names do not match the event schema.** Pages use their own prefixes: `session.` (44 uses), `reply.` (24), `user_turn.` (20), `turn.` (17), `state.` (14), `draft_reply.` (14), plus `bot_draft.`, `bot_turn.`, `bot_reply.`, `user_message.`, `refusal_event.`, `handoff_event.`, `job.`, `limit_event.` and others. The schema uses `bot.*`, `user_label.*`, `request.*`, `handoff.*` and so on. Several `session.*` names (for example `session.advances_declined`, `session.stalled_turns`) are not schema fields. A mapping from page names to schema names does not exist yet.
2. **Several names for the draft reply.** `draft_reply`, `bot_draft`, `bot_turn`, `bot_reply` and `reply` all appear for what looks like the same thing. I did not verify that they mean the same thing on every page.
3. **`choices` has four spellings.** A quoted list (`["Windows", "Mac", ...]`), `none`, `[]`, and one unquoted comma list ("back, change an answer, start over, something else (free text always open)"). Some carry a trailing `#` comment.
4. **Trailing `#` comments on some lines.** 16 `moves:` lines end with "# short names for the moves in the table". One `choices:` line says "# example only, built from the readings each turn". One says "# no menu: state the correction; free text stays open". Two say "# no offer_choices move on this page".
5. **`on_miss` values are not defined anywhere I read.** `rewrite`, `handoff`, `log`, `ask` are used, but no page or spec defines them. The module's behavior for each is an open question (section 7).
6. **`runs: conversation` has no stated unit.** It appears to mean the check looks at several turns, not one draft. The pages do not say whether it runs every turn or on events.
7. **`runs: post_turn`** appears on two pages: `missing-the-obvious-intent` and `silent-failure-and-timeout`.
8. **Voice pages carry the same format.** `repair-failure` and `order-mix-ups-at-the-speaker` are `runs: conversation`, but the schema marks their voice fields PLANNED. The module must skip any `reads` item that needs a PLANNED field.
9. **Free-text metrics.** `metric` and `counter_metric` are phrases, not computed identifiers.

## 4. Where checks run

| `runs` value | Meaning, as the pages use it | Example |
|---|---|---|
| `pre_send` | The check looks at a reply that is about to be sent, and can change it. | `answer-and-go-conversation`: "a non-final bot reply is about to be sent with an answer but no forward move" |
| `post_turn` | The check looks after a turn finished, so it cannot change that reply. | `silent-failure-and-timeout` (reads `request.end_reason`, `stream.finish_reason`) |
| `conversation` | The check looks across the conversation, not one reply. | `complex-or-emotional-discussion-forced-into-chat` (reads `session.turns_without_progress`) |

Because `post_turn` and `conversation` checks cannot rewrite a reply already sent, their `on_miss` can only be a logged flag, an `ask` or a `handoff` on the next turn. The pages do not say this explicitly; I am inferring it from the names, and it is listed in section 7.

## 5. What the module never does

- **No code in this repository.** This repo holds pages, specs and tests only. The module lives in a separate repository the owner creates.
- **No auto-send.** The module returns a verdict and, at most, a proposed rewrite or a move name. It never sends a message to a user, a customer, or a person on staff. A person or the host application decides whether to send.
- **No storing personal data.** It keeps no raw message text beyond the request. The schema has `text_redaction` (`none`, `partial`, `full`) and `user_ref` ("never a raw name or email"). The module should require redacted text by default and persist only IDs, labels and verdicts. The schema does not say how to redact, and the module should not claim to.
- **No claims of measured results.** No accuracy, recall, savings or "tested" statements. Signals and thresholds on the pages are uncalibrated.
- **Guide specs stay `proposed`.** The module never changes a `status` line, and never edits a pattern page. Any change to a spec goes through a pull request to this repository.
- **No invented thresholds.** It uses only what a spec's `trigger` and the page's signals say. If a page gives no number, the module takes it as configuration from the implementer.
- **No voice or web detection.** Those fields are PLANNED in the schema.
- **No sensitive data collection.** It must not ask users for the values that `sensitive-data-collected-in-chat` warns about.

## 6. Test conversations it must pass

The module is checked against the repository's own tests, in `tests/<pattern-id>.md`. Each file follows `tests/README.md`: a rubric, numbered scenarios, and a Results table that says "Not yet run" until someone runs it. 30 test files exist for 61 pages, so 31 specs have no test file. This note records no results.

Eight chat-first files to start with, one per kind of check:

| Pattern ID | Test file | `runs` | Why this one |
|---|---|---|---|
| `answer-buried` | `tests/answer-buried.md` | `pre_send` | Simplest draft-reply check |
| `guessing-instead-of-asking` | `tests/guessing-instead-of-asking.md` | `pre_send` | The only `on_miss: ask` page |
| `scam-victim-not-interrupted` | `tests/scam-victim-not-interrupted.md` | `pre_send` | Reads `payment.*` fields; high stakes |
| `cold-transfer` | `tests/cold-transfer.md` | `pre_send` | Reads `handoff_event.packet` and `handoff_event.transcript_url` |
| `talk-to-a-human-ignored-or-looped` | `tests/talk-to-a-human-ignored-or-looped.md` | `conversation` | Multi-turn check |
| `dead-end-i-don-t-understand-replies` | `tests/dead-end-i-don-t-understand-replies.md` | `conversation` | Matches the schema's worked example (fallback twice, then a request for a person) |
| `corrections-not-applied` | `tests/corrections-not-applied.md` | `conversation` | Slot state across turns |
| `silent-failure-and-timeout` | `tests/silent-failure-and-timeout.md` | `post_turn` | Only way to exercise `post_turn` with request and stream events |

`repair-failure` and `order-mix-ups-at-the-speaker` also have test files, but they are voice patterns and stay out of the first set.

**Pass condition for the module:** on each scenario, the module's verdict agrees with the file's pass/fail rubric line, including the scenarios where the right behavior is "nothing special" (`tests/README.md` requires at least two per file). A person must run this and record it; the module's authors must not write the result in advance.

## 7. Open questions for the owner

1. Which repository, language and license? The schema's license line reads "owner to choose".
2. Should the 61 pages be normalized first (section 3.1 items 1 to 4), or should the module carry a mapping table from page names to schema names? Who owns that table?
3. What does each `on_miss` value do: `rewrite`, `handoff`, `log`, `ask`? Is `handoff` a proposed message, or a call into the host's transfer system?
4. Is `conversation` evaluated every turn or on events (for example `session_end`)? Is `post_turn` always after the reply was sent?
5. Who supplies the labels (`user_label.*`, `bot.*` labels): a rule, a classifier, a judge or a human? The schema leaves this open and their accuracy is unmeasured.
6. Where do thresholds come from when a page gives none? Per-deployment configuration?
7. Should the module handle the 31 pages without test files, or wait until those have tests?
8. Redaction: does the module trust the host to redact, or must it refuse unredacted `text`?
9. Which move wins when several specs fire on the same draft reply?

Code repo created by the owner on 2026-10-24: [sarkars/gort](https://github.com/sarkars/gort) (public, empty, no license yet). The product name is GORT; see [gort-plan.md](gort-plan.md). Question 1 is answered except the license.
