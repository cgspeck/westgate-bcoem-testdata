#!/usr/bin/env python3
import config
from datadefs import ParticipantBrewerRecord
from db import create_entries, create_participant, participant_exists
from utils import generate_participant


participants: list[ParticipantBrewerRecord] = []

participant_count = 0
judge_count = 0
entry_count = 0

while True:
    new_participant = generate_participant()
    
    if participant_exists(new_participant):
        print(f"Oh no! User with same name or email already exists, skipping...")
        continue

    create_participant(new_participant)

    if len(new_participant.entries) > 0:
        create_entries(new_participant)

    participants.append(new_participant)
    participant_count += 1
    entry_count += len(new_participant.entries)
    if new_participant.is_judge:
        judge_count += 1

    # can we break out of loop yet?
    constraints_unsatisfied = False
    if judge_count < config.min_judges:
        constraints_unsatisfied = True
    if participant_count < config.min_participants:
        constraints_unsatisfied = True    
    if entry_count < config.min_entries:
        constraints_unsatisfied = True
    
    if not constraints_unsatisfied:
        break

    
print(f"Participants: {len(participants)}")
print(f"Judges: {judge_count}")
print(f"Entries: {entry_count}")