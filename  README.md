# Marketplace Architecture (C4 + Service bootstrap)

## Goal
Design a marketplace architecture (no business logic), document decisions, provide a C4 Container diagram,
and bootstrap one service that runs in Docker and returns `200 OK` on `/health`.

---

## Requirements covered
- C4 Container diagram: `docs/c4/architecture.likec4`
- Domains and responsibilities documented
- Data ownership boundaries (DB-per-service; no shared DB)
- Sync/async interactions described
- One service implemented and runnable in Docker (`catalog-service`)
- Health-check endpoint `/health` returns `200 OK`

---

## Domains and responsibilities
1) **Identity & Access (Auth)**
   - user accounts, roles (buyer/seller), authentication
2) **Catalog**
   - products, categories, seller listings, product attributes
3) **Feed / Recommendations**
   - personalized feed generation based on user preferences and product signals
4) **Orders**
   - carts, orders, order statuses, lifecycle tracking
5) **Payments & Accounting**
   - payment records, invoices, ledger entries (stub in this homework)
6) **Notifications**
   - sending notifications on status changes (stub in this homework)

---

## Mapping domains to services
- **API Gateway / BFF**: single entry point; routing, auth middleware, simple aggregation
- **Auth Service**: Identity & Access
- **Catalog Service**: Catalog management
- **Feed Service**: Feed/Recommendations
- **Order Service**: Orders lifecycle
- **Payment Service**: Payments accounting
- **Notification Service**: Notifications delivery
- **Message Broker**: async events between services

Rationale: services are split by cohesive business domains to reduce coupling and allow independent evolution.

---

## Data ownership (no shared DB)
Each service owns its database and schema:
- Auth -> Auth DB
- Catalog -> Catalog DB
- Feed -> Feed DB
- Orders -> Order DB
- Payments -> Payment DB
- Notifications -> Notification DB

No other service writes to alien DB; interactions are via HTTP APIs or events.

---

## Interactions (sync vs async)
### Synchronous (HTTP)
- Gateway -> Auth/Catalog/Feed/Orders
- Orders -> Payments (payment initiation)

### Asynchronous (events)
- Orders publishes `OrderCreated`, `OrderStatusChanged`
- Payments publishes `PaymentSucceeded`, `PaymentFailed`
- Notifications consumes events and sends messages

---

## Architecture decisions (ADR)
- `docs/adr/01-razbienie.md` — decomposition + alternatives + trade-offs
- `docs/adr/02-dannye.md` — sync/async and DB-per-service

---

## C4 diagram (LikeC4)
Source: `docs/c4/architecture.likec4`

To preview, install VS Code extension **LikeC4** and open the preview from Command Palette.

---

## Run the service (Docker)

### Prerequisites
- Docker Desktop is installed and running

### Start
From the repository root:
```bash
docker compose up --build
```
### Health check
```bash
curl -i http://localhost:8000/health
```
Service will be available at: http://localhost:8000

Expected output:
- Status: `HTTP/1.1 200 OK`
- Body: `{"status":"ok"}`

### Stop
```bash
docker compose down
```