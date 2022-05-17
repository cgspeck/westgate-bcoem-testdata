from __future__ import annotations
from dataclasses import dataclass, field
import typing

@dataclass
class Entry:
    name: str
    style: Style

@dataclass
class ParticipantUserAccount:
    user_name: str # email address
    user_level: str = "2"
    user_id: typing.Optional[int] = field(default=None)

@dataclass
class ParticipantBrewerRecord:
    user_account: ParticipantUserAccount
    first_name: str
    last_name: str
    
    street_address: str
    city: str
    postcode: str
    
    phone: str
    club: str
    email: str
    
    is_staff: bool
    is_steward: bool
    is_judge: bool

    entries: list[Entry]

    state: str = "VIC"
    country: str = "Australia"
    
    def generate_staff_record(self):
        pass

@dataclass
class Style:
    id: str
    brew_style_name: str
    brew_style_group: str
    brew_style_num: str
    
    def brew_cat(self):
        return str(int(self.brew_style_group))
    
    def brew_cat_sort(self):
        return f"{int(self.brew_style_group):02}"

@dataclass
class Suburb:
    name: str
    postcode: str
