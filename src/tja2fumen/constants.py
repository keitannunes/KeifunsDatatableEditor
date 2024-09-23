"""
Constant song properties of TJA and fumen files.
"""

# Names for branches in diverge songs
BRANCH_NAMES = ("normal", "professional", "master")

# Types of notes that can be found in TJA files
TJA_NOTE_TYPES = {
    '0': 'Blank',
    '1': 'Don',                 # ドン
    'n': 'Don',                 # ドン
    '#SENOTECHANGE 1': 'Don',   # ドン
    'd': 'Don2',                # ド
    '#SENOTECHANGE 2': 'Don2',  # ド
    'o': 'Don3',                # コ
    '#SENOTECHANGE 3': 'Don3',  # コ
    '2': 'Ka',                  # カッ
    't': 'Ka',                  # カッ
    '#SENOTECHANGE 4': 'Ka',    # カッ
    'k': 'Ka2',                 # カ
    '#SENOTECHANGE 5': 'Ka2',   # カ
    '3': 'DON',                 # ドン(大)
    '4': 'KA',                  # カッ(大)
    '5': 'Drumroll',            # 連打―っ!!
    '6': 'DRUMROLL',            # 連打(大)―っ!!
    '7': 'Balloon',             # ふうせん
    '8': 'EndDRB',
    '9': 'Kusudama',            # くすだま
    'A': 'DON2',                # ドン(手)
    'B': 'KA2',                 # カッ(手)
    'C': 'Blank',               # bombs
    'D': 'Drumroll',            # fuse roll
    'E': 'DON2',                # red + green single hit
    'F': 'Ka',                  # ADLib (hidden note)
    'G': 'KA2',                 # red + green double hit
    'H': 'DRUMROLL',            # double roll
    'I': 'Drumroll',            # green roll
}

# Types of notes that can be found in fumen files
FUMEN_NOTE_TYPES = {
    0x1: "Don",         # ドン
    0x2: "Don2",        # ド
    0x3: "Don3",        # コ
    0x4: "Ka",          # カッ
    0x5: "Ka2",         # カ
    0x6: "Drumroll",    # 連打―っ!!
    0x7: "DON",         # ドン(大)
    0x8: "KA",          # カッ(大)
    0x9: "DRUMROLL",    # 連打(大)―っ!!
    0xa: "Balloon",     # ふうせん
    0xb: "DON2",        # ドン(手)
    0xc: "Kusudama",    # くすだま
    0xd: "KA2",         # カッ(手)
    0xe: "Unknown1",    # ? (Present in some Wii1 songs)
    0xf: "Unknown2",    # ? (Present in some PS4 songs)
    0x10: "Unknown3",   # ? (Present in some Wii1 songs)
    0x11: "Unknown4",   # ? (Present in some Wii1 songs)
    0x12: "Unknown5",   # ? (Present in some Wii4 songs)
    0x13: "Unknown6",   # ? (Present in some Wii1 songs)
    0x14: "Unknown7",   # ? (Present in some PS4 songs)
    0x15: "Unknown8",   # ? (Present in some Wii1 songs)
    0x16: "Unknown9",   # ? (Present in some Wii1 songs)
    0x17: "Unknown10",  # ? (Present in some Wii4 songs)
    0x18: "Unknown11",  # ? (Present in some PS4 songs)
    0x19: "Unknown12",  # ? (Present in some PS4 songs)
    0x22: "Unknown13",  # ? (Present in some Wii1 songs)
    0x62: "Drumroll2"   # ?
}

# Invert the dict to go from note type to fumen byte values
FUMEN_TYPE_NOTES = {v: k for k, v in FUMEN_NOTE_TYPES.items()}

# Normalize the various fumen course names into 1 name per difficulty
NORMALIZE_COURSE = {
    '0': 'Easy',
    'Easy': 'Easy',
    '1': 'Normal',
    'Normal': 'Normal',
    '2': 'Hard',
    'Hard': 'Hard',
    '3': 'Oni',
    'Oni': 'Oni',
    '4': 'Ura',
    'Ura': 'Ura',
    'Edit': 'Ura'
}

# Fetch the 5 valid course names from NORMALIZE_COURSE's values
COURSE_NAMES = list(set(NORMALIZE_COURSE.values()))

# All combinations of difficulty and single/multiplayer type
TJA_COURSE_NAMES = []
for difficulty in COURSE_NAMES:
    for player in ['', 'P1', 'P2']:
        TJA_COURSE_NAMES.append(difficulty+player)

# Map course difficulty to filename IDs (e.g. Oni -> `song_m.bin`)
COURSE_IDS = {
    'Easy': 'e',
    'Normal': 'n',
    'Hard': 'h',
    'Oni': 'm',
    'Ura': 'x',
}

TIMING_WINDOWS = {
    #            "GOOD" timing      "OK" timing       "BAD" timing
    'Easy':   (041.7083358764648, 108.441665649414, 125.125000000000),
    'Normal': (041.7083358764648, 108.441665649414, 125.125000000000),
    'Hard':   (025.0250015258789, 075.075004577637, 108.441665649414),
    'Oni':    (025.0250015258789, 075.075004577637, 108.441665649414)
}