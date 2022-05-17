import datetime
from os import environ
import random

import MySQLdb
from datadefs import ParticipantBrewerRecord

_dry_run = (environ.get('DRY_RUN', 'false') == 'true')

_db = None

if _db is None and not _dry_run:
    _db = MySQLdb.connect(
        database=environ["DB_DATABASE"],
        host=environ["DB_HOST"],
        password=environ["DB_PASSWORD"],
        port=int(environ["DB_PORT"]),
        user=environ["DB_USER"],
    )

def create_brew_judging_number() -> str:
    candidate = str(random.randint(100000, 999999))
    cur = _db.cursor()
    cur.execute("""
SELECT COUNT(*)
FROM brewing
WHERE brewJudgingNumber = %s;
    """, (candidate, ))
    exists = cur.fetchone()[0] > 0
    
    if exists:
        print(f"Judging number {candidate} already exists, trying again...")
        return create_brew_judging_number()

    return candidate
    

def create_entries(participant: ParticipantBrewerRecord):
    if _dry_run:
        return
    
    assert participant.user_account.user_id is not None
    cur = _db.cursor()
    entries = participant.entries
    
    for entry in entries:
        print(f"Creating entry '{entry.name}'")
        style = entry.style
        brew_info = None
        brew_judging_no = create_brew_judging_number()
        
        if style.brew_cat() == "21":
            brew_info = f"Required info for {entry.name}"
        cur.execute("""
    INSERT INTO brewing (
        brewName, brewStyle, brewCategory, brewCategorySort, brewSubCategory,
        brewInfo,
        brewBrewerFirstName, brewBrewerLastName, brewBrewerID,
        brewPaid,
        brewReceived,
        brewJudgingNumber,
        brewUpdated,
        brewConfirmed)
    VALUES (
        %s, %s, %s, %s, %s,
        %s,
        %s, %s, %s,
        %s,
        %s,
        %s,
        %s,
        %s
        )""", (
            entry.name, style.brew_style_name, style.brew_cat(), style.brew_cat_sort(), style.brew_style_num,
            brew_info,
            participant.first_name, participant.last_name, participant.user_account.user_id,
            1,
            1,
            brew_judging_no,
            datetime.datetime.now(),
            1
        ))

def create_participant(participant: ParticipantBrewerRecord):
    if _dry_run:
        return
    cur = _db.cursor()
    cur.execute("""
INSERT INTO users(user_name,password,userLevel,userCreated)
VALUES (%s, %s, %s, %s);
    """, (
        participant.user_account.user_name,
        "$2a$08$S.KNXq.yQL9uAOQ8zzUxtOL0dJ.srZRN.VDtVCOn7NzuntcPUW3oS",
        participant.user_account.user_level,
        datetime.datetime.now()
    ))
    
    cur.execute("SELECT LAST_INSERT_ID();")
    user_id = cur.fetchone()[0]
    
    print(f"Created user {participant.user_account.user_name} ({user_id})")
    participant.user_account.user_id = user_id
    # create brewer
    brewer_staff = 'Y' if participant.is_staff else 'N'
    brewer_steward = 'Y' if participant.is_steward else 'N'
    brewer_judge = 'Y' if participant.is_judge else 'N'
    brewer_judge_location = 'Y-1' if participant.is_judge else None
    brewer_steward_location = 'Y-1' if participant.is_steward else None
    brewer_judge_waiver = 'Y' if participant.is_judge else None
    brewer_judge_exp = '2' if participant.is_judge else None
    cur.execute("""
INSERT INTO brewer (
    uid, brewerFirstName, brewerLastName, 
    brewerAddress, brewerCity, brewerState, brewerZip, brewerCountry, brewerPhone1, 
    brewerClubs, brewerEmail, 
    brewerStaff, brewerSteward, 
    brewerJudge, brewerJudgeRank, brewerJudgeLocation, brewerJudgeExp,
    brewerStewardLocation, 
    brewerJudgeWaiver, 
    brewerDropOff
) VALUES (
    %s, %s, %s, 
    %s, %s, %s, %s, %s, %s,
    %s, %s,
    %s, %s,
    %s, %s, %s,%s,
    %s,
    %s,
    %s
    );""",
    (
        user_id, participant.first_name, participant.last_name,
        participant.street_address, participant.city, participant.state, participant.postcode, "Australia", participant.phone,
        participant.club, participant.email,
        brewer_staff, brewer_steward,
        brewer_judge, "Non-BJCP", brewer_judge_location,brewer_judge_exp,
        brewer_steward_location,
        brewer_judge_waiver,
        "1"
    ))
    # create staff record 
    cur.execute("""
    INSERT INTO staff (
        uid,staff_judge,staff_judge_bos,staff_steward,
        staff_organizer,staff_staff
    ) VALUES
	 (%s,0,0,0,0,0);
    """,
    (user_id,))

def participant_exists(participant: ParticipantBrewerRecord) -> bool:
    if _dry_run:
        return False

    cur = _db.cursor()
    cur.execute("SELECT COUNT(*) FROM users WHERE user_name = %s", (participant.user_account.user_name,))
    exists = cur.fetchone()[0] > 0
    
    if exists:
        return True
    
    cur.execute("SELECT COUNT(*) FROM brewer WHERE brewerFirstName = %s AND brewerLastName = %s", (participant.first_name, participant.last_name,))
    exists = cur.fetchone()[0] > 0
    
    return exists
