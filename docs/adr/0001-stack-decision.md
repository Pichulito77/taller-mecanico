# 0001 — Stack Decision

Date: 2025-08-11

## Context
We need a productive, maintainable stack for a CRUD- and workflow-heavy workshop management system with RBAC, reporting, and transactional consistency. Development machines are Windows; we prefer minimizing native dependencies via Docker for the database.

## Decision
Primary: Django + PostgreSQL
Alternative: Laravel + MySQL

## Consequences
+ Fast time-to-market, strong admin, mature ORM.
+ Solid testing and security posture.
+ Prefer Docker for DB on Windows to avoid native driver/toolchain issues.
- Team should align on Python/Django conventions and pre-commit tooling.