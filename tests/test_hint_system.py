from number_guessing_game import HintSystem


def test_generate_hint():
    target_number = 24
    hint = HintSystem.generate_hint(target_number)

    # Test that hint is a string and ends with a period
    assert isinstance(hint, str)
    assert hint.endswith(".")

    # Test possible hint variations
    valid_hints = [
        "The number is divisible by",
        "The number is even",
        "The number's digits sum to 6"
    ]

    # Check if hint starts with one of the valid hint types
    assert any(hint.startswith(valid_start) for valid_start in valid_hints)


def test_generate_hint_odd_number():
    target_number = 25
    hint = HintSystem.generate_hint(target_number)

    if "even" in hint or "odd" in hint:
        assert "odd" in hint


def test_generate_hint_digit_sum():
    target_number = 123
    hint = HintSystem.generate_hint(target_number)

    if "digits sum" in hint:
        assert "6" in hint  # 1 + 2 + 3 = 6
