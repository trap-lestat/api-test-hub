from __future__ import annotations

import sqlite3
from typing import Any, Dict, List, Tuple

from api_test_hub.core.assertions import AssertionErrorDetail, assert_response
from api_test_hub.core.request import ResponseData


class DatabaseError(ValueError):
    pass


def run_db_checks(
    databases: Dict[str, Any],
    checks: List[Dict[str, Any]],
    context: Dict[str, Any] | None = None,
) -> None:
    for check in checks:
        check = dict(check)
        datasource = str(check.get("datasource", "default"))
        if datasource not in databases:
            raise DatabaseError(f"Unknown datasource: {datasource}")

        sql = check.get("sql")
        if not sql:
            raise DatabaseError("validate_db requires sql")

        rows = _execute_sql(databases[datasource], str(sql))
        value = rows[0][0] if rows else None

        extract = check.get("extract") or {}
        if context is not None and isinstance(extract, dict):
            for key, field in extract.items():
                if field == "value":
                    context[key] = value
                elif field == "rows":
                    context[key] = rows
        check.pop("extract", None)

        rules = check.get("assert") or []
        if rules:
            response = ResponseData(
                url=f"db://{datasource}",
                method="QUERY",
                status_code=0,
                headers={},
                text="",
                json={"value": value, "rows": rows},
            )
            assert_response(response, rules)


def _execute_sql(config: Dict[str, Any], sql: str) -> List[Tuple[Any, ...]]:
    db_type = str(config.get("type", "sqlite")).lower()
    if db_type == "sqlite":
        return _execute_sqlite(config, sql)
    if db_type == "mysql":
        return _execute_mysql(config, sql)
    if db_type in {"postgres", "postgresql"}:
        return _execute_postgres(config, sql)

    raise DatabaseError(f"Unsupported db type: {db_type}")


def _execute_sqlite(config: Dict[str, Any], sql: str) -> List[Tuple[Any, ...]]:
    path = config.get("path")
    if not path:
        raise DatabaseError("sqlite requires path")
    conn = sqlite3.connect(path)
    try:
        cur = conn.execute(sql)
        return cur.fetchall()
    finally:
        conn.close()


def _execute_mysql(config: Dict[str, Any], sql: str) -> List[Tuple[Any, ...]]:
    try:
        import pymysql
    except Exception as exc:
        raise DatabaseError("pymysql is required for mysql") from exc

    conn = pymysql.connect(
        host=config.get("host"),
        port=int(config.get("port", 3306)),
        user=config.get("user"),
        password=config.get("password"),
        database=config.get("database"),
    )
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()
    finally:
        conn.close()


def _execute_postgres(config: Dict[str, Any], sql: str) -> List[Tuple[Any, ...]]:
    try:
        import psycopg2
    except Exception as exc:
        raise DatabaseError("psycopg2 is required for postgres") from exc

    conn = psycopg2.connect(
        host=config.get("host"),
        port=int(config.get("port", 5432)),
        user=config.get("user"),
        password=config.get("password"),
        dbname=config.get("database"),
    )
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()
    finally:
        conn.close()
