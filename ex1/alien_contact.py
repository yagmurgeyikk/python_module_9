from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pydantic import ValidationError
from enum import Enum
from pydantic import model_validator


class Contact(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: Contact
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(max_length=500)
    is_verified: bool = False
    try:
        @model_validator(mode='after')
        def validator_rules(self) -> 'AlienContact':
            if not self.contact_id.startswith("AC"):
                raise ValidationError("The entered value must start with AC.")
            if not self.contact_type == Contact.physical and not self.is_verified:
                raise ValidationError("Physical contact reports must be verified")
            if not self.contact_type == Contact.telepathic and self.witness_count < 3:
                raise ValidationError("Telepathic contact requires at least 3 "
                                      "witnesses")
            if self.signal_strength > 7.0 and not self.message_received:
                raise ValidationError("Strong signals (> 7.0) should include "
                                      "received messages")
    except ValidationError as e:
        print("Expected validation error:")
        print(e)
