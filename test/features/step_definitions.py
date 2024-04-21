from pytest_bdd import when, then, parsers, scenarios

from test.api.data.builder.test_station_builder import build_test_station_payload
from test.conftest import Context
from test.utils.enum import CommandsEnum
from test.utils.helpers import assert_equal, execute_assertions_and_throw_errors

scenarios('test_stations.feature')


# defining these values here (or could be another place) and not pass it from the step layer allows us to easily
# update and adapt the tests in the future and not having to change in each step.
EXPECTED_VERSION_THRESHOLD = 1.6
INTERVAL_START, INTERVAL_END = 1, 60
EXPECTED_VALUE = 'OK'


@when(parsers.parse('a test request with command "getVersion" is sent to station ID {station_id}'))
def test_station_version_by_id(ctx: Context, station_id):
    # a logger is needed
    print(f'--- Testing station ID {station_id} with command: getVersion')

    data = build_test_station_payload(command=CommandsEnum.GET_VERSION.value)
    response = ctx.stations_client.test_station_id(ctx=ctx,
                                                   data=data,
                                                   station_id=station_id)
    ctx.add_response(response)


@when(parsers.parse('a test request with command "getInterval" is sent to station ID {station_id}'))
def test_station_interval_by_id(ctx: Context, station_id):
    print(f'--- Testing station ID {station_id} with command: getInterval')

    data = build_test_station_payload(command=CommandsEnum.GET_INTERVAL.value)
    response = ctx.stations_client.test_station_id(ctx=ctx,
                                                   data=data,
                                                   station_id=station_id)
    ctx.add_response(response)


@when(parsers.parse('a test request with command "setValues" and payload number {payload_number} is sent '
                    'to station ID {station_id}'))
def test_station_value_by_id(ctx: Context, payload_number, station_id):
    print(f'--- Testing station ID {station_id} with command setValues and payload number {payload_number}')
    data = build_test_station_payload(command=CommandsEnum.SET_VALUES.value,
                                      payload=payload_number)
    response = ctx.stations_client.test_station_id(ctx=ctx,
                                                   data=data,
                                                   station_id=station_id)
    ctx.add_response(response)
    ctx.set_shared_data('payload_number', payload_number)


@then(parsers.parse('response status code is {expected_response_code}'))
def verify_response_status_code(ctx: Context, expected_response_code):
    print(f'--- Asserting response status code is {expected_response_code}')
    response = ctx.get_last_response()
    assert_equal(int(expected_response_code), response.status_code)


@then('the tested station has compliant version')
def station_has_compliant_version(ctx: Context):
    response = ctx.get_last_response()

    print(f'--- Validating the station has compliant version higher than: {EXPECTED_VERSION_THRESHOLD}')
    _assert_compliant_version(version_threshold=EXPECTED_VERSION_THRESHOLD, response=response)


@then('the tested station has compliant interval')
def station_has_compliant_interval(ctx: Context):
    response = ctx.get_last_response()

    print(f'--- Validating the station has compliant interval between range: {INTERVAL_START} and {INTERVAL_END}')
    _assert_compliant_interval(interval_start=INTERVAL_START, interval_end=INTERVAL_END, response=response)


@then('the tested station is compliant for setting values')
def station_is_compliant_for_set_values(ctx: Context):
    print(f'--- Validating the station is compliant for command setValues with '
          f'payload number {ctx.get_shared_data("payload_number")}')

    response = ctx.get_last_response()
    _assert_compliant_set_values(expected_value=EXPECTED_VALUE, response=response)


def _assert_compliant_version(version_threshold, response):
    actual_version = response.json()['result']
    assert float(actual_version) > version_threshold, \
        f'Version is not correct! Expected version number to be higher than {version_threshold}, ' \
        f'but actual value is {actual_version}'


def _assert_compliant_interval(interval_start, interval_end, response):
    actual_interval = response.json()['result']
    assert interval_start <= int(actual_interval) <= interval_end, \
        f'Interval is not corrected! Expected value to be between {interval_start} and {interval_end}, but actual' \
        f'value is {actual_interval}'


def _assert_compliant_set_values(expected_value, response):
    actual_value = response.json()['result']
    assert_equal(expected_value=expected_value, actual_value=actual_value)


@when(parsers.parse('all test requests are sent to station ID {station_id}'))
def all_tests_requests_to_station_id(ctx: Context, station_id):
    test_station_version_by_id(ctx=ctx, station_id=station_id)
    ctx.set_shared_data('version_response', ctx.get_last_response())

    test_station_interval_by_id(ctx, station_id=station_id)
    ctx.set_shared_data('interval_response', ctx.get_last_response())

    test_station_value_by_id(ctx, payload_number=2, station_id=station_id)
    ctx.set_shared_data('values_response', ctx.get_last_response())


@then('the tested stations are compliant for all commands')
def tested_stations_are_compliant(ctx: Context):

    assertions = [
        (lambda: _assert_compliant_version(version_threshold=EXPECTED_VERSION_THRESHOLD,
                                           response=ctx.get_shared_data('version_response')),
         "Version is not compliant!"),
        (lambda: _assert_compliant_interval(interval_start=INTERVAL_START,
                                            interval_end=INTERVAL_END,
                                            response=ctx.get_shared_data('interval_response')),
         "Interval is not compliant!"),
        (lambda: _assert_compliant_set_values(expected_value=EXPECTED_VALUE,
                                              response=ctx.get_shared_data('values_response')),
         "Setting values is not compliant")
    ]
    execute_assertions_and_throw_errors(assertions)
