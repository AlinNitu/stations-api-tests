from dataclasses import dataclass


@dataclass
class StationDto:
    command: str
    payload: int | str | None
