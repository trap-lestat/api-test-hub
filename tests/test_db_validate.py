from __future__ import annotations

import sqlite3
import textwrap

from api_test_hub.config import load_config
from api_test_hub.core import run_case
from api_test_hub.utils import start_mock_server, stop_mock_server


def test_validate_db_sqlite(tmp_path) -> None:
    db_path = tmp_path / "demo.db"
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("create table users (id integer primary key, name text)")
        conn.execute("insert into users (id, name) values (1, 'admin')")
        conn.commit()
    finally:
        conn.close()

    base_url, server = start_mock_server()
    try:
        config_text = textwrap.dedent(
            f"""
            version: 1
            name: demo
            base_url: {base_url}
            db:
              default:
                type: sqlite
                path: {db_path}
            cases:
              - name: db_check
                method: GET
                path: /hello
                validate_db:
                  - name: user_count
                    datasource: default
                    sql: "select count(1) from users"
                    extract:
                      db_user_count: value
                    assert:
                      - eq: [body.value, 1]
            """
        ).strip()

        config = load_config_text(tmp_path, config_text)
        context = {}
        run_case(
            config.base_url,
            config.cases[0],
            variables=config.variables,
            context=context,
            auth=config.auth,
            dbs=config.db,
        )
    finally:
        stop_mock_server(server)


def load_config_text(tmp_path, content):
    path = tmp_path / "demo.yaml"
    path.write_text(content, encoding="utf-8")
    return load_config(path)
