import phonenumbers
from phone_extractor import format_phone, validate_phones

def test_format_phone():
    # Test cases
    test_cases = {
        "+1 833 545 9543": "+18335459543",  # USA
        "+212 661 370802": "+212661370802",  # Morocco
        "+33 612345678": "+33612345678",  # France
        "+4915234567890": "+4915234567890",  # Germany
        "invalid_number": None,
        "+1 415 555 2671": "+1415552671",  # USA
    }

    for input_number, expected_output in test_cases.items():
        parsed_number = phonenumbers.parse(input_number, None)  # Ensure correct parsing
        result = format_phone(parsed_number)
        assert result == expected_output, f"Expected {expected_output}, but got {result} for input {input_number}"

def test_validate_phones():
    # Test cases
    test_cases = {
        # Valid phone numbers
        ("+1 833 545 9543", "+212 661 370802", "+33 612345678"): {"+1 833 545 9543", "+212 661 370802", "+33 612345678"},
        # Invalid phone numbers
        ("invalid_number", "12345"): set(),
        # Mixed valid and invalid
        ("+1 415 555 2671", "invalid_number", "+4915234567890"): {"+1 415 555 2671", "+4915234567890"},
        # Edge case: empty list
        (): set(),
        # Edge case: list with None
        (None,): set(),
    }

    for phones, expected_output in test_cases.items():
        result = validate_phones(phones)
        assert result == expected_output, f"Expected {expected_output}, but got {result} for input {phones}"

if __name__ == "__main__":
    test_format_phone()
    test_validate_phones()
    print("All tests passed!")