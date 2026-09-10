from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pydantic import ValidationError
from enum import Enum
from pydantic import model_validator


class Contact(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: Contact
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode='after')
    def validator_rules(self) -> 'AlienContact':
        if not self.contact_id.startswith("AC"):
            raise ValueError("The entered value must start with AC.")
        if self.contact_type == Contact.PHYSICAL and not self.is_verified:
            raise ValueError(
                "Physical contact reports must be verified")
        if self.contact_type == Contact.TELEPATHIC and self.witness_count < 3:
            raise ValueError("Telepathic contact requires at least 3 "
                             "witnesses")
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals (> 7.0) should include "
                             "received messages")
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("======================================")
    try:
        data = AlienContact(
                contact_id="AC_2024_001",
                timestamp=datetime.now(),
                location="Area 51, Nevada", contact_type=Contact.RADIO,
                signal_strength=8.5, duration_minutes=45,
                witness_count=5,
                message_received="Greetings from Zeta Reticuli")
        print("Valid contact report:")
        print(f"ID: {data.contact_id}")
        print(f"Type: {data.contact_type.value}")
        print(f"Location: {data.location}")
        print(f"Signal: {data.signal_strength}/10")
        print(f"Duration: {data.duration_minutes} minutes")
        print(f"Witnesses: {data.witness_count}")
        print(f"Message: {data.message_received}")
        print(data.timestamp)
        print()
        print("======================================")
        data = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            location="Area 51, Nevada", contact_type=Contact.TELEPATHIC,
            signal_strength=8.5, duration_minutes=45,
            witness_count=1, message_received="Greetings from Zeta Reticuli")
        print("Valid contact report:")
        print(f"ID: {data.contact_id}")
        print(f"Type: {data.contact_type}")
        print(f"Location: {data.location}")
        print(f"Signal: {data.signal_strength}")
        print(f"Duration: {data.duration_minutes}")
        print(f"Witnesses: {data.witness_count}")
        print(f"Duration: {data.duration_minutes}")
        print(f"Witnesses: {data.witness_count}")
        print(f"Message: {data.message_received}")
    except ValidationError as e:
        print("Expected validation error:")
        for err in e.errors():
            print(err["msg"])


if __name__ == "__main__":
    main()
