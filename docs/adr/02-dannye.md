# ADR-02: Integration style and data ownership

## Status
Accepted

## Context
We must define:
- service-to-service interactions (sync vs async)
- boundaries of data ownership
- how to avoid shared databases and high coupling

## Decision
1) **DB per service**:
- Auth owns users/roles/profiles
- Catalog owns products/categories/listings
- Feed owns feed prefs and ranking cache
- Orders owns carts/orders/status history
- Payments owns payments/ledger
- Notifications owns templates/delivery logs

2) **Sync HTTP for request/response flows**:
- Gateway -> domain services (client requests)
- Order -> Payment (payment initiation) sync

3) **Async events for state changes and side effects**:
- Orders publish OrderCreated / OrderStatusChanged
- Payments publish PaymentSucceeded / PaymentFailed
- Notifications consumes events and sends messages

## Consequences (trade-offs)
Pros:
- Lower coupling: services do not “call each other in circles” to complete one action
- Notifications are decoupled and resilient to temporary failures
- DB-per-service enforces independent schema evolution

Cons:
- Eventual consistency: notifications may arrive slightly later
- Requires broker and basic event discipline (naming, versioning) in future

## Notes (implementation scope)
This homework does not implement business logic, databases, or broker runtime.
We document integration decisions and show them in the C4 diagram.