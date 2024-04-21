def assert_equal(expected_value, actual_value, error_message=None):
    if error_message is None:
        error_message = f'Assertion failed! Expected value is "{expected_value}" but actual value is "{actual_value}"'
    assert expected_value == actual_value, error_message


def execute_assertions_and_throw_errors(assertions):
    errors = []
    for assertion_func, assertion_message in assertions:
        try:
            assertion_func()
        except AssertionError as e:
            errors.append(f"{assertion_message}: {str(e)}")
    if errors:
        raise AssertionError("\n".join(errors))
