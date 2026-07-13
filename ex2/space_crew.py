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
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: str = datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember]
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validator_rules(self) -> 'SpaceMission':
        if not self.mission_id.startswith("M"):
            raise ValueError(" Mission ID must start with 'M'")
        is_true = False
        for element in self.crew:
            if (
                element.rank.value == "commander" or
                element.rank.value == "captain"
            ):
                is_true = True
            else:
                pass
        if is_true is True:
            pass
        else:
            raise ValueError(
                "Mission must have at least one Commander or Captain")

        number_crew = len(self.crew)
        i = 0
        if self.duration_days >= 365:
            for elements in self.crew:
                if elements.years_experience > 5:
                    i += 1
                else:
                    pass
        if i > (number_crew/2):
            pass
        else:
            raise ValueError("Long missions (> 365 days) need 50% "
                             "experienced crew (5+ years)")
        j = 0
        for elements in self.crew:
            if elements.is_active is True:
                j += 1
            else:
                pass
        if j == number_crew:
            pass
        else:
            print("All crew members must be active")
        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")
    try:
        member_one = CrewMember(
            member_id="one", name="Sarah Connor", rank=CrewRanks.commander,
            age=34, specialization="Mission Command", years_experience=6
        )

        member_two = CrewMember(
            member_id="two", name="John Smith", rank=CrewRanks.lieutenant,
            age=30, specialization="Navigation", years_experience=19
        )

        member_three = CrewMember(
            member_id="three", name="Alice Johnson", rank=CrewRanks.officer,
            age=28, specialization="Engineering", years_experience=43
        )
        crew_list = [member_one, member_two, member_three]
        print("Valid mission created:")
        mission = SpaceMission(
            mission_name="Mars Colony Establishment", mission_id="M2024_MARS",
            destination="Mars", duration_days=900, budget_millions=2500.0,
            crew=crew_list)
        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print(f"Crew size: {len(crew_list)}")
        print("Crew members:")
        print(f"-{member_one.name} ({CrewRanks.commander.value}) - "
              f"{member_one.specialization}")

        print(f"-{member_two.name} ({CrewRanks.lieutenant.value}) - "
              f"{member_two.specialization}")
        
        print(f"-{member_three.name} ({CrewRanks.officer.value}) - "
              f"{member_three.specialization}")
        print()
        print("=========================================")
        member_one = CrewMember(
            member_id="one", name="Sarah Connor", rank=CrewRanks.lieutenant,
            age=34, specialization="Mission Command", years_experience=6
        )

        member_two = CrewMember(
            member_id="two", name="John Smith", rank=CrewRanks.lieutenant,
            age=30, specialization="Navigation", years_experience=19
        )

        member_three = CrewMember(
            member_id="three", name="Alice Johnson", rank=CrewRanks.lieutenant,
            age=28, specialization="Engineering", years_experience=43
        )

        crew_list_two = [member_one, member_two, member_three]

        mission = SpaceMission(
            mission_name="Mars Colony Establishment", mission_id="M2024_MARS",
            destination="Mars", duration_days=900, budget_millions=2500.0,
            crew=crew_list_two)

    except ValidationError as e:
        print("Expected validation error:")
        for err in e.errors():
            print(err["msg"])


if __name__ == "__main__":
    main()
