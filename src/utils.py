from collections import defaultdict
from copy import deepcopy
from typing import DefaultDict
from names import get_first_name, get_last_name
from unique_names_generator import get_random_name
from data import CLUBS, STREET_NAMES, STYLES, SUBURBS
import random
import config

from datadefs import Entry, ParticipantBrewerRecord, ParticipantUserAccount

def generate_entries(entry_count: int) -> list[Entry]:
    styles = deepcopy(STYLES)
    memo: list[Entry] = []
    excluded_style_groups: list[str] = []
    style_group_entry_count: DefaultDict[str, int] = defaultdict(lambda: 0)
    
    while len(memo) < entry_count:
        selected = random.choice(styles)
        
        if selected.brew_style_group in excluded_style_groups:
            print("selected excluded style group, trying again...")
            continue
        
        style_group_entry_count[selected.brew_style_group] += 1
        
        if style_group_entry_count[selected.brew_style_group] == config.max_entries_per_participant_per_group:
            excluded_style_groups.append(selected.brew_style_group)
        
        memo.append(Entry(
            name=f"{get_random_name()} {selected.brew_style_name.split(' [')[0]}",
            style=selected
        ))
    
    return memo
        

def generate_participant() -> ParticipantBrewerRecord:
    first_name = get_first_name()
    last_name = get_last_name()
    
    user_name = f"{first_name.lower()}.{last_name.lower()}@westgatebrewers.org"
    
    street_address = f"{random.randrange(1, 2000)} {random.choice(STREET_NAMES)}"
    club = random.choice(CLUBS)
    suburb = random.choice(SUBURBS)
    
    city = suburb.name
    postcode = suburb.postcode
    phone = f"0{str(random.randint(400000000, 499999999))}"
    email = user_name
    
    is_steward = random.uniform(0.0, 1.0) <= config.p_participant_is_steward
    is_judge = random.uniform(0.0, 1.0) <= config.p_participant_is_judge
    
    is_staff = is_judge or is_steward
    entries: list[Entry] = []    
    has_entries = random.uniform(0.0, 1.0) <= config.p_participant_has_entry
    
    if has_entries:
        entries = generate_entries(random.randint(1, config.max_entries_per_participant))
   
    return ParticipantBrewerRecord(
        user_account=ParticipantUserAccount(
            user_name=user_name
        ),
        first_name=first_name,
        last_name=last_name,
        street_address=street_address,
        club=club,
        city=city,
        postcode=postcode,
        phone=phone,
        email=email,
        is_staff=is_staff,
        is_steward=is_steward,
        is_judge=is_judge,
        entries=entries
    )