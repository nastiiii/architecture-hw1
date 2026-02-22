# ADR-01: Service decomposition for Marketplace

## Status
Accepted

## Context
We need to design a marketplace platform where:
- sellers manage product catalog
- customers browse personalized feed
- customers place orders
- payments are accounted
- notifications are sent on order status changes

Constraints:
- no business logic implementation at this stage
- at least one service must run in Docker and expose /health returning 200 OK
- architecture should be explainable and defendable

We also want to avoid “distributed monolith” patterns:
- shared database between services
- high coupling by content (services relying on each other to complete one atomic operation)

## Decision
Use a microservice-style decomposition aligned with domains (DDD-ish boundaries):
- API Gateway / BFF
- Auth Service
- Catalog Service
- Feed Service
- Order Service
- Payment Service
- Notification Service
- Message broker for async events

Each service owns its data (database-per-service).

## Consequences (trade-offs)
Pros:
- Clear bounded contexts and responsibilities
- Independent evolution of domains (catalog/feed/orders/payments/notifications)
- Reduced coupling via async events for status changes and notifications
- Enforced data ownership prevents shared-db coupling

Cons:
- More components to operate (broker, multiple services, multiple DBs)
- Eventual consistency for event-driven flows (notifications, some projections)
- More effort for observability and debugging across services (later)

## Alternatives considered
### Alternative A: Modular monolith
One deployable application with modules (auth/catalog/orders/payments/notifications).
Pros: simplest deployment, easy local development, fewer infra components.
Cons: scaling by teams harder, more merge/conflict pressure, weaker isolation, risk of “big ball of mud” over time.

### Alternative B: SOA with shared database
Multiple services but a shared database schema.
Pros: simpler data queries, fewer integration problems short-term.
Cons: violates data ownership, creates strong coupling through shared schema, services cannot evolve independently -> distributed monolith.

## Why chosen
Given multiple distinct domains and the course focus on service boundaries and data ownership,
microservice-style decomposition with DB-per-service best matches the goals and avoids shared-db coupling.