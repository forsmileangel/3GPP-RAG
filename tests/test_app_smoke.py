"""Smoke test: app/streamlit_app.py must import without executing the UI.

Under `streamlit run` the script runs as __main__ and calls main(); under
`import app.streamlit_app` (here) the module name differs, so main() does NOT
fire — which only holds if no `st.*` side effect sits at module top level.
Skips until streamlit is installed.
"""

from __future__ import annotations

import pytest

pytest.importorskip("streamlit")


def test_streamlit_app_imports_without_running_ui():
    import app.streamlit_app as appmod

    assert callable(appmod.main)
    assert callable(appmod.get_engine)


def test_streamlit_app_runs_headless_no_exception():
    """Execute the script headless via Streamlit's own test runner. main() runs
    but returns early (no button pressed), so no DB/LLM is touched — this proves
    the page/sidebar/widget setup has no runtime error, beyond import-safety."""
    from pathlib import Path

    from streamlit.testing.v1 import AppTest

    app_path = Path(__file__).resolve().parent.parent / "app" / "streamlit_app.py"
    at = AppTest.from_file(str(app_path)).run(timeout=30)
    assert not at.exception
    assert at.title[0].value == "3GPP 規格查詢 (MVP)"
