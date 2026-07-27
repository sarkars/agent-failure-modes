# What Are the Most Common System Integration Failures in AI Agents?

**System integration fails when agents cannot interoperate with upstream or downstream services, when integration contracts drift and break silently, when schema changes in dependencies cause parsing or processing failures, or when agents lack observability into cross-system communication.** System integration is foundational in production agents because no agent operates in isolation — agents call APIs, databases, message queues, and other services, and failures in those systems or in the integration contracts between systems cascade into agent failures. The patterns documented here are still being collected; this goal area awaits additional empirical data from production integration-failure incidents.

## Key Takeaways

- System integration is often treated as an infrastructure concern rather than an agent-design concern, but agent behavior depends directly on the reliability and correctness of system integrations.
- Patterns in this goal area are under active collection; teams deploying agents that depend on external systems should prioritize integration testing and contract validation before production launch.
- Common integration failures include API schema changes, message format incompatibility, timeout configuration mismatch, and missing error handling for specific service failures.
- Integration strategy depends on system topology: synchronous agents calling REST APIs need different error handling than asynchronous agents consuming message queues, which differ from agents reading from databases.

## Scope

This goal encompasses the full integration lifecycle — discovering and validating integration contracts, handling service-specific errors, recovering from integration failures, and observing cross-system communication for debugging.

## When System Integration Matters

- An agent depends on external services (REST APIs, message queues, databases), where service failures or API changes break agent functionality.
- An agent is part of a larger system where it calls downstream services and other services call the agent, creating bidirectional coupling that introduces complexity.
- Multiple teams own different parts of the system and can change integration contracts independently, creating the risk of silent API drift that breaks production without clear error messages.

## Cross-Pattern Insight

System integration failures are often invisible in testing because test environments typically mock external services or use test instances with stable APIs. A production agent might call an external API that works fine for 99.9% of requests but has edge cases or version-specific behaviors that test mocks never encountered. When integration contracts drift (API adds a new required field, message schema changes), production deployments break in ways that weren't caught by integration tests. The mitigation that recurs across integration patterns is the same architectural move — make integration contracts explicit and testable: use API contracts (OpenAPI specs, protocol buffers, or JSON schema) as the source of truth for both client and server, validate contracts at deployment time rather than discovering mismatches at runtime, test with real or realistic service instances (not just mocks), and add specific error handling for each failure mode that service can produce (timeouts, 5xx errors, specific error codes) rather than generic error handling that masks problems.

## Frequently Asked Questions

### How do you handle version drift when external APIs evolve?
Version drift occurs when an external service adds fields, changes behavior, or deprecates endpoints without advance notice. Use API contracts (OpenAPI, schema definitions) that are owned by the service team and published alongside the API itself. Before deploying an agent that calls an API, validate that the agent's assumptions about the API (request format, response schema, error codes) match the published contract. Use the contract as the source of truth for both documentation and code generation.

### What is the difference between a service timeout and a service failure?
A timeout means the service didn't respond within the configured window (network latency, service overload, or actual failure). A service failure means the service responded with an error code (5xx, 429, etc.). Both require specific handling: timeouts often benefit from retry (network hiccup), while 5xx errors may benefit from fallback or circuit breaking. Don't treat all failures the same — different error types need different recovery strategies.

### Can integration contracts be validated without mocking?
Yes, but it requires discipline and test infrastructure: maintain staging or test instances of dependencies that match production APIs, run integration tests against real or realistic service instances regularly (not just once at deployment), and alert when contracts change. Mocks are useful for unit testing agents in isolation, but production integration requires testing with realistic services.

## Patterns

This goal area is currently under active pattern collection. As empirical data from production system-integration failures becomes available, documented patterns will be added here.

## Related Goals

- [Tool Integration Limits](../tool-integration-limits/) — integration failures when tools are applied without respecting their constraints
- [Tool Error Handling](../tool-error-handling/) — error handling strategies for tool and service failures
- [Observability Monitoring](../observability-monitoring/) — integration failures are invisible without cross-service tracing and error monitoring
- [Logging and Tracing](../logging-and-tracing/) — integration events should be logged for debugging and incident response
