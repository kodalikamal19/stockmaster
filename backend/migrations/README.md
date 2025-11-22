# Database Migrations

This directory contains Alembic database migrations.

## Initialize migrations (first time only)

```bash
flask db init
```

## Create a new migration

```bash
flask db migrate -m "Description of changes"
```

## Apply migrations

```bash
flask db upgrade
```

## Rollback migration

```bash
flask db downgrade
```

