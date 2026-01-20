from __future__ import annotations

import sqlite3
import textwrap

from api_test_hub.config import load_config
from api_test_hub.core import run_case
from api_test_hub.utils import start_mock_server, stop_mock_server


def test_validate_db_result_compares_with_response(tmp_path) -> None:
    db_path = tmp_path / "demo.db"
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("create table users (id integer primary key, name text)")
        conn.execute("insert into users (id, name) values (1, 'admin')")
        conn.execute("insert into users (id, name) values (2, 'demo')")
        conn.execute("insert into users (id, name) values (3, 'lei')")
        conn.execute("insert into users (id, name) values (4, 'tom')")
        conn.execute("insert into users (id, name) values (5, 'sam')")
        conn.execute("insert into users (id, name) values (6, 'kate')")
        conn.execute("insert into users (id, name) values (7, 'admin')")
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
              - name: db_compare
                method: GET
                path: /hello
                validate_db:
                  - name: user_count
                    datasource: default
                    sql: "select count(1) from users"
                    extract:
                      db_user_count: value
                validate:
                  - eq: [body.user.id, "${{db_user_count}}"]
            """
        ).strip()

        config_path = tmp_path / "demo.yaml"
        config_path.write_text(config_text, encoding="utf-8")

        config = load_config(config_path)
        context = {}
        run_case(
            config.base_url,
            config.cases[0],
            variables=config.variables,
            context=context,
            auth=config.auth,
            dbs=config.db,
        )

        assert context["db_user_count"] == 7
    finally:
        stop_mock_server(server)
