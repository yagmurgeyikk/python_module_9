from pydantic import BaseModel, Field
from datetime import datetime
from pydantic import ValidationError
from enum import Enum
from pydantic import model_validator


class CrewRanks(Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: CrewRanks
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(ge=5, le=15)
    mission_name: str = Field(ge=3, le=100)
    destination: str = Field(ge=3, le=50)
    launch_date: str = datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember]
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validator_rules(self) -> 'SpaceMission':
        if not self.mission_id.startswith("M"):
            raise ValueError(" Mission ID must start with 'M'")
        for element in self.crew:
            if (
                element.rank.value == "commander" or
                element.rank.value == "captain"
            ):
                pass
            else:
                raise ValueError("Must have at least one Commander or Captain")

        number_crew = len(self.crew)
        i = 0
        for _ in range(number_crew):
            if self.duration_days > 365:
                if self.years_experience > 5:
                    i += 1
                else:
                    pass
        if i > (number_crew/2):
            pass
        else:
            raise ValueError("Long missions (> 365 days) need 50% "
                             "experienced crew (5+ years)")
        j = 0
        for elements in range(number_crew):
            if elements.is_active is True:
                j += 1
            else:
                pass
        if i == number_crew:
            pass
        else:
            print("All crew members must be active")
