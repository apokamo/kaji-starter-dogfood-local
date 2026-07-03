"""``greet`` の Small テスト: 正常系（整形・トリム）と異常系（空・空白のみ）を覆う。"""

import pytest

from starter_app import greet


@pytest.mark.small
def test_greet_returns_personalized_message() -> None:
    assert greet("Alice") == "Hello, Alice!"


@pytest.mark.small
def test_greet_trims_surrounding_whitespace() -> None:
    assert greet("  Bob  ") == "Hello, Bob!"


@pytest.mark.small
def test_greet_empty_string_raises_value_error() -> None:
    with pytest.raises(ValueError):
        greet("")


@pytest.mark.small
def test_greet_whitespace_only_raises_value_error() -> None:
    with pytest.raises(ValueError):
        greet("   ")
