# Support Resolution Agent: Business Goals, Failure Definitions, and Test List

A chat agent that resolves common customer issues (order status, account questions, plan changes) using the company's systems, and hands off to a person when it should.

> **Read this first.** These are design starting points to adapt with your own business owners, not benchmarks or advice. No target numbers are given because none can be set without your baseline.

## Scope (a starting point)

**The agent does:**
- Answer questions about the customer's own account, orders, and plan using live records
- Perform small, reversible actions within set limits (update an address, resend a receipt)
- Hand off to a person with a summary when it cannot or should not continue

**The agent does not:**
- Decide refunds or credits above its limit (see the refunds and billing-disputes agent)
- Give legal, medical, or financial advice
- Change account ownership or security settings without verification

## Business goals

| # | Goal | Success means | Owner |
|---|---|---|---|
| G1 | Resolve the issue in the first conversation | The customer's problem is fixed, and the customer confirms it or does not come back about the same issue. | Head of support or support operations |
| G2 | Use the right account and the right facts | Every statement about the customer's account, plan, or order comes from their own current records, and every policy statement from the current policy. | Support operations plus the owner of the knowledge base |
| G3 | Hand off to a person at the right moment, with context | The customer reaches a person when the situation needs one, and the person does not have to ask again for what the customer already said. | Head of support, with the team that staffs the human queue |
| G4 | Keep the customer's effort low | The customer states their problem once, always knows the next step, and is not sent in circles. | Support experience owner |

## Goal definitions

For every goal: how to measure it, how to find your baseline, what counts as a failure and how severe it is, and when the agent hands over to a person. Baseline method for all goals: Take a sample of conversations or cases the way a person handled them over a period you choose (one vendor's guidance uses 90 days as an example) and compute the same measure. A statement like "it takes too long" is not a baseline.

### G1. Resolve the issue in the first conversation

| Field | Definition |
|---|---|
| How to measure | Confirmed-resolution rate: conversations ending in an explicit confirmation or no repeat contact on the same issue within a window you set, divided by all conversations. Track it next to containment (conversations that did not reach a person), and report the gap. |
| A failure is | The agent says the issue is solved when it is not, closes on a polite message, or the customer returns with the same issue. |
| Severity | Critical: a false "done" on something with money or deadlines. High: repeat contact on the same issue. Medium: a correct fix that took far longer than a person would. |
| Hand over to a person when | The customer asks for a person; two attempts have failed; the issue touches money, safety, or an account change the agent cannot make. |

**Failures to test for this goal (from the library):**
- [False Completion Claim](../../by-use-case/customer-service/goals/conversation-resolution/failures/false-completion-claim.md): Agent says done when action was not completed
- [Premature Ticket Closure from Politeness-Cue Misread as Resolution Confirmation](../../by-use-case/support-services/goals/issue-resolution/failures/premature-ticket-closure-from-politeness-cue-misread-as-resolution-confirmation.md): Agent Closes a Support Ticket as Resolved Because the Customer's Reply Contains a Polite Closing Phrase ("Thanks," "OK," "Got it"), Without…
- [Repeat Contact Loop](../../by-use-case/support-services/goals/issue-resolution/failures/repeat-contact-loop.md): Agent Resolves Each Support Contact From a Customer in Isolation, Failing to Recognize That the Same Underlying Issue Has Been "Resolved"…
- [Deflection of Unresolved Issues](../../by-use-case/support-services/goals/self-service-deflection/failures/deflection-of-unresolved-issues.md): Self-Service Agent Marks a Conversation as "Deflected" (Resolved Without Human Agent) Based on the Customer Not Replying, Rather Than the…
- [Canned Response Context Mismatch](../../by-use-case/support-services/goals/issue-resolution/failures/canned-response-context-mismatch.md): Agent Selects a Templated/Canned Response That Matches Surface Keywords but Misses the Customer's Actual Situation

### G2. Use the right account and the right facts

| Field | Definition |
|---|---|
| How to measure | Sampled review: share of replies whose account and policy facts match the system of record at the time. Count wrong-account and wrong-plan answers separately. |
| A failure is | The agent answers for the wrong product or account, quotes an outdated article, or states a policy with confidence it does not have. |
| Severity | Critical: another customer's data or the wrong account acted on. High: a wrong policy or price stated as fact. Medium: an outdated help article suggested. |
| Hand over to a person when | Records conflict or are missing; the retrieved answer is low-confidence; the customer disputes the stated fact. |

**Failures to test for this goal (from the library):**
- [Agent Infers Product Line from Recently-Mentioned Topic Instead of Entitlement Record](../../by-use-case/support-services/goals/ticket-routing/failures/agent-infers-product-line-from-recently-mentioned-topic-instead-of-entitlement-record.md): Ticket-Routing Agent Determines Which Product Line a Ticket Belongs to Based on Whatever Product Name Was Most Recently Mentioned in the…
- [Knowledge Base Staleness in Support Chatbots](../../by-use-case/support-services/goals/issue-resolution/failures/knowledgebase-staleness.md): Support Agent Uses Outdated Knowledge Base; Gives Customers Incorrect or Outdated Information
- [Embedding Retrieval Surfaces Deprecated Help Article in Deflection Suggestion](../../by-use-case/support-services/goals/self-service-deflection/failures/embedding-retrieval-surfaces-deprecated-help-article-in-deflection-suggestion.md): A Self-Service Deflection Agent's RAG Step, Used to Suggest a Help Article to Resolve a Customer's Question Without Human Involvement,…
- [Low Retrieval-Confidence Presented as a Confident Answer Without Escalation Disclaimer](../../by-use-case/support-services/goals/self-service-deflection/failures/low-retrieval-confidence-presented-as-confident-answer-without-escalation-disclaimer.md): Self-Service Deflection Agent Generates a Fluent, Assertive Answer From a Weakly-Matched Retrieved Article, Instead of Hedging or Routing…
- [Embedding Retrieval Selects Similar but Wrong Canned Response](../../by-use-case/customer-service/goals/conversation-resolution/failures/embedding-retrieval-selects-similar-but-wrong-canned-response.md): A Support Agent That Selects a Canned Response or Macro From a Library Via Semantic/Embedding Similarity to the Customer's Message, Rather…

### G3. Hand off to a person at the right moment, with context

| Field | Definition |
|---|---|
| How to measure | Escalation precision and recall against labelled conversations; share of handed-off cases where the agent repeated a question the bot had already asked. |
| A failure is | The agent loops instead of escalating, escalates too early, misses an angry or urgent customer, or drops what it had learned in the handoff. |
| Severity | Critical: a customer in distress or with a time-critical issue is not escalated. High: a customer is stuck in a loop. Medium: a needless handoff. |
| Hand over to a person when | This goal defines the triggers: the customer's request, repeated failure, stakes, and sentiment. |

**Failures to test for this goal (from the library):**
- [Poor Escalation](../../by-use-case/customer-service/goals/conversation-resolution/failures/poor-escalation.md): Agent fails to hand off to a human at the right time
- [Escalation Too Early](../../by-use-case/customer-service/goals/conversation-resolution/failures/escalation-too-early.md): Agent gives up despite solvable request
- [Chatbot Loop Without Human Escalation Path](../../by-use-case/support-services/goals/self-service-deflection/failures/chatbot-loop-without-human-escalation-path.md): Self-Service Deflection Agent Keeps Offering the Same or Similar Automated Suggestions Without Recognizing the Customer Needs Human…
- [Sentiment Misclassification Delays Escalation](../../by-use-case/support-services/goals/sentiment-escalation/failures/sentiment-misclassification-delays-escalation.md): Agent's Sentiment Classifier Mislabels Controlled, Formally-Worded but Highly Escalated Customer Language as Neutral, Delaying Human…
- [Multi-Agent Handoff Drops Prior Attempted Fix Between Bot and Human Agent](../../by-use-case/support-services/goals/issue-resolution/failures/multi-agent-handoff-drops-prior-attempted-fix-between-bot-and-human-agent.md): A Bot-Tier Support Agent's Chat Transcript With a Customer Shows the Customer Already Tried Two Specific Troubleshooting Steps Without…

### G4. Keep the customer's effort low

| Field | Definition |
|---|---|
| How to measure | Customer-effort proxies from logs: repeated questions per conversation, turns to resolution, loops (the same suggestion twice), and a short effort survey. |
| A failure is | The agent re-asks known information, repeats itself, apologizes without acting, or sends the customer through circular help pages. |
| Severity | High: a loop with no exit. Medium: repeated questions or an unclear next step. |
| Hand over to a person when | A loop or the same question is detected twice. |

**Failures to test for this goal (from the library):**
- [Repeated Question Loop](../../by-use-case/customer-service/goals/conversation-resolution/failures/repeated-question-loop.md): Agent asks for information already provided
- [Unclear Next Step](../../by-use-case/customer-service/goals/conversation-resolution/failures/unclear-next-step.md): User does not know what happens next
- [Over-Apology Loop](../../by-use-case/customer-service/goals/conversation-resolution/failures/over-apology-loop.md): Agent apologizes repeatedly without solving
- [Circular FAQ Redirect Loop](../../by-use-case/support-services/goals/self-service-deflection/failures/circular-faq-redirect-loop.md): Self-Service Deflection Agent Routes a Customer Through a Closed Loop of FAQ Articles That Each Point Back to One Another, Never Reaching a…
- [Tone Mismatch](../../by-use-case/customer-service/goals/conversation-resolution/failures/tone-mismatch.md): Agent sounds rude, robotic, too casual, or too formal

## Operations concerns for this agent

| Area | Why it matters here | Patterns |
|---|---|---|
| [Tool Reliability](../../cross-cutting/operations/goals/tool-reliability/) | The agent acts through order, account, and ticket systems; silent tool failures turn into false "done" answers | 19 |
| [Tool Access Scope Limits](../../cross-cutting/operations/goals/tool-access-scope-limits/) | The agent must see only the signed-in customer's records | 16 |
| [Memory Management](../../cross-cutting/operations/goals/memory-management/) | The conversation spans many turns and sometimes sessions | 22 |
| [Context Lifecycle](../../cross-cutting/operations/goals/context-lifecycle/) | Long chats push early facts and rules out of the window | 6 |
| [State Tracking](../../cross-cutting/operations/goals/state-tracking/) | The agent must know what it already did and asked | 9 |
| [Agent Handoffs Delegation](../../cross-cutting/operations/goals/agent-handoffs-delegation/) | Context must survive bot-to-human and bot-to-bot transfers | 10 |
| [Human Oversight Reliability](../../cross-cutting/operations/goals/human-oversight-reliability/) | Escalation and approval paths must work when staff are busy or away | 8 |
| [Real Time Performance](../../cross-cutting/operations/goals/real-time-performance/) | Slow replies make customers repeat or leave | 12 |
| [Traceability](../../cross-cutting/operations/goals/traceability/) | Disputes need a record of what the agent said and did | 8 |

## Security and governance to check

- [Agent Trust](../../cross-cutting/security/goals/agent-trust/) (security)
- [Data Loss Prevention](../../cross-cutting/security/goals/data-loss-prevention/) (security)
- [Runtime Security](../../cross-cutting/security/goals/runtime-security/) (security)
- [Governance](../../cross-cutting/governance/goals/governance/) (governance)
- [Output Accuracy](../../cross-cutting/accuracy/goals/output-accuracy/) (accuracy)

## Decisions your business owner must make

- What counts as "resolved", and how long without a repeat contact confirms it
- Which actions the agent may take, and the dollar or risk limit for each
- The triggers that always go to a person
- Which systems of record the agent trusts when records conflict

## Related

- [All agents by business goal](../)
