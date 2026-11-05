from tools.phone_cleanser import clean_phone_rows


def test_normalizes_and_removes_row_number():
    result, count = clean_phone_rows("1. Nama 081234567890")
    assert result == "Nama 6281234567890"
    assert count == 1


def test_discards_leading_description_but_keeps_multiword_name():
    result, _ = clean_phone_rows("1. teks tambahan tidak penting - john doe salim 081312123434")
    assert result == "john doe salim 6281312123434"


def test_trailing_dash_preserves_name():
    result, _ = clean_phone_rows("1. john doe - 081312122323")
    assert result == "john doe 6281312122323"


def test_multiple_numbers_expand_to_rows():
    result, count = clean_phone_rows("Nama 081234567890 / 081345678901")
    assert result.splitlines() == ["Nama 6281234567890", "Nama 6281345678901"]
    assert count == 2


def test_reversed_order():
    result, _ = clean_phone_rows("6281234567890 Nama")
    assert result == "Nama 6281234567890"


def test_unusual_number_is_retained():
    result, _ = clean_phone_rows("Nama 123456789090")
    assert result == "Nama 123456789090"


def test_rows_without_numbers_are_dropped():
    result, count = clean_phone_rows("Nama\nJohn Doe - no number\nNama 081234567890")
    assert result == "Nama 6281234567890"
    assert count == 1
