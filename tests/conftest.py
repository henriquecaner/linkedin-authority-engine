import pathlib
import pytest

@pytest.fixture
def plugin_dir():
    return pathlib.Path(__file__).resolve().parent.parent / "linkedin-authority-engine"
