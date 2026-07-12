# projenin error mesajlarını düzlenle .error ekle
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pydantic import ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")
    try:
        data = SpaceStation(
            station_id="ISS001", name="International Space Station",
            crew_size=6, power_level=85.5, oxygen_level=92.3,
            last_maintenance="2026-07-11")

        print("Valid station created:")
        print(f"ID: {data.station_id}")
        print(f"Name: {data.name}")
        print(f"Crew: {data.crew_size}")
        print(f"Power: {data.power_level}")
        print(f"Oxygen: {data.oxygen_level}")
        if data.is_operational is True:
            print("Status: Operational")
        else:
            print("Status: Not Operational")
        print()
        print("========================================")
        data = SpaceStation(
            station_id="ISS001", name="International Space Station",
            crew_size=21, power_level=85.5, oxygen_level=92.3,
            last_maintenance="2026-07-11")
        print("Valid station created:")
        print(f"ID: {data.station_id}")
        print(f"Name: {data.name}")
        print(f"Crew: {data.crew_size}")
        print(f"Power: {data.power_level}")
        print(f"Oxygen: {data.oxygen_level}")
        if data.is_operational is True:
            print("Status: Operational")
        else:
            print("Status: Not Operational")
    except ValidationError as e:
        print("Expected validation error:")
        for err in e.errors():
            print(err["msg"])


if __name__ == "__main__":
    main()
