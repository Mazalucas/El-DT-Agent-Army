"""Test version information."""

import agents_army


def test_version():
    """Test that version is defined."""
    assert hasattr(agents_army, "__version__")
    assert agents_army.__version__ == "0.1.0"
