from dataclasses import asdict

from test.api.data.dto.test_station_dto import StationDto


def build_test_station_payload(command=None, payload=None):
    # value from param OR fall back to a default value
    command = command or 'setValue'
    payload = payload or None

    full_payload = StationDto(command=command,
                              payload=payload)
    return asdict(full_payload)
