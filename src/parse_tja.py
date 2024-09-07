"""
Most of this code was adapted from https://github.com/WHMHammer/tja-tools and converted to Python.
The original repository does not specify a license. Usage of said code
is intended to fall under fair use for educational or non-commercial purposes.
If there are any concerns or issues regarding the usage of this code, please
contact @keifunky on discord.
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict
from math import ceil, floor
HEADER_GLOBAL = [
    'TITLE',
    'SUBTITLE',
    'BPM',
    'WAVE',
    'OFFSET',
    'DEMOSTART',
    'GENRE',
]

HEADER_COURSE = [
    'COURSE',
    'LEVEL',
    'BALLOON',
    'SCOREINIT',
    'SCOREDIFF',
    'TTROWBEAT',
]

COMMAND = [
    'START',
    'END',
    'GOGOSTART',
    'GOGOEND',
    'MEASURE',
    'SCROLL',
    'BPMCHANGE',
    'DELAY',
    'BRANCHSTART',
    'BRANCHEND',
    'SECTION',
    'N',
    'E',
    'M',
    'LEVELHOLD',
    'BMSCROLL',
    'HBSCROLL',
    'BARLINEOFF',
    'BARLINEON',
    'TTBREAK',
]

def parse_line(line):
    match = None
    
    # comment
    match = re.match(r'//.*', line)
    if match:
        line = line[:match.start()].strip()

    # header
    match = re.match(r'^([A-Z]+):(.+)', line, re.IGNORECASE)
    if match:
        name_upper = match.group(1).upper()
        value = match.group(2).strip()

        if name_upper in HEADER_GLOBAL:
            return {
                'type': 'header',
                'scope': 'global',
                'name': name_upper,
                'value': value
            }
        elif name_upper in HEADER_COURSE:
            return {
                'type': 'header',
                'scope': 'course',
                'name': name_upper,
                'value': value
            }
    
    # command
    match = re.match(r'^#([A-Z]+)(?:\s+(.+))?', line, re.IGNORECASE)
    if match:
        name_upper = match.group(1).upper()
        value = match.group(2) or ''

        if name_upper in COMMAND:
            return {
                'type': 'command',
                'name': name_upper,
                'value': value.strip()
            }
    
    # data
    match = re.match(r'^(([0-9]|A|B|C|F|G)*,?)$', line)
    if match:
        data = match.group(1)
        return {
            'type': 'data',
            'data': data
        }
    
    return {
        'type': 'unknown',
        'value': line
    }

def get_course(tja_headers, lines):
    headers = {
        'course': 'Oni',
        'level': 0,
        'balloon': [],
        'scoreInit': 100,
        'scoreDiff': 100,
        'ttRowBeat': 16
    }

    measures = []

    measure_dividend = 4
    measure_divisor = 4
    measure_properties = {}
    measure_data = ''
    measure_events = []
    current_branch = 'N'
    target_branch = 'N'
    flag_levelhold = False

    for line in lines:
        if line['type'] == 'header':
            if line['name'] == 'COURSE':
                headers['course'] = line['value']
            elif line['name'] == 'LEVEL':
                headers['level'] = int(line['value'])
            elif line['name'] == 'BALLOON':
                headers['balloon'] = [int(b) for b in re.split(r'[^0-9]', line['value']) if b]
            elif line['name'] == 'SCOREINIT':
                headers['scoreInit'] = int(line['value'])
            elif line['name'] == 'SCOREDIFF':
                headers['scoreDiff'] = int(line['value'])
            elif line['name'] == 'TTROWBEAT':
                headers['ttRowBeat'] = int(line['value'])
        
        elif line['type'] == 'command':
            if line['name'] == 'BRANCHSTART':
                if not flag_levelhold:
                    values = line['value'].split(',')
                    if values[0] == 'r':
                        if len(values) >= 3:
                            target_branch = 'M'
                        elif len(values) == 2:
                            target_branch = 'E'
                        else:
                            target_branch = 'N'
                    elif values[0] == 'p':
                        if len(values) >= 3 and float(values[2]) <= 100:
                            target_branch = 'M'
                        elif len(values) >= 2 and float(values[1]) <= 100:
                            target_branch = 'E'
                        else:
                            target_branch = 'N'
            
            elif line['name'] == 'BRANCHEND':
                current_branch = target_branch
            
            elif line['name'] in ('N', 'E', 'M'):
                current_branch = line['name']
            
            elif line['name'] in ('START', 'END'):
                current_branch = 'N'
                target_branch = 'N'
                flag_levelhold = False
            
            else:
                if current_branch != target_branch:
                    continue
                if line['name'] == 'MEASURE':
                    match_measure = re.match(r'(\d+)/(\d+)', line['value'])
                    if match_measure:
                        measure_dividend = int(match_measure.group(1))
                        measure_divisor = int(match_measure.group(2))
                
                elif line['name'] == 'GOGOSTART':
                    measure_events.append({
                        'name': 'gogoStart',
                        'position': len(measure_data)
                    })
                
                elif line['name'] == 'GOGOEND':
                    measure_events.append({
                        'name': 'gogoEnd',
                        'position': len(measure_data)
                    })
                
                elif line['name'] == 'SCROLL':
                    measure_events.append({
                        'name': 'scroll',
                        'position': len(measure_data),
                        'value': float(line['value'])
                    })
                
                elif line['name'] == 'BPMCHANGE':
                    measure_events.append({
                        'name': 'bpm',
                        'position': len(measure_data),
                        'value': float(line['value'])
                    })
                
                elif line['name'] == 'TTBREAK':
                    measure_properties['ttBreak'] = True
                
                elif line['name'] == 'LEVELHOLD':
                    flag_levelhold = True
        
        elif line['type'] == 'data' and current_branch == target_branch:
            data = line['data']
            if data.endswith(','):
                measure_data += data[:-1]
                measures.append({
                    'length': [measure_dividend, measure_divisor],
                    'properties': measure_properties,
                    'data': measure_data,
                    'events': measure_events
                })
                measure_data = ''
                measure_events = []
                measure_properties = {}
            else:
                measure_data += data

    if measures:
        first_bpm_event_found = any(evt['name'] == 'bpm' and evt['position'] == 0 for evt in measures[0]['events'])
        if not first_bpm_event_found:
            measures[0]['events'].insert(0, {
                'name': 'bpm',
                'position': 0,
                'value': tja_headers['bpm']
            })

    course = {
        'easy': 0,
        'normal': 1,
        'hard': 2,
        'oni': 3,
        'edit': 4,
        'ura': 4,
        '0': 0,
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4
    }.get(headers['course'].lower(), 0)

    if measure_data:
        measures.append({
            'length': [measure_dividend, measure_divisor],
            'properties': measure_properties,
            'data': measure_data,
            'events': measure_events
        })
    else:
        for event in measure_events:
            event['position'] = len(measures[-1]['data'])
            measures[-1]['events'].append(event)

    return {'course': course, 'headers': headers, 'measures': measures}

def parse_tja(tja):
    lines = [line.strip() for line in re.split(r'(\r\n|\r|\n)', tja) if line.strip()]

    headers = {
        'title': '',
        'subtitle': '',
        'bpm': 120,
        'wave': '',
        'offset': 0,
        'demoStart': 0,
        'genre': ''
    }

    courses = {}
    course_lines = []

    for line in lines:
        parsed = parse_line(line)

        if parsed['type'] == 'header' and parsed['scope'] == 'global':
            headers[parsed['name'].lower()] = parsed['value']

        elif parsed['type'] == 'header' and parsed['scope'] == 'course':
            if parsed['name'] == 'COURSE' and course_lines:
                course = get_course(headers, course_lines)
                courses[course['course']] = course
                course_lines = []

            course_lines.append(parsed)

        elif parsed['type'] in ('command', 'data'):
            course_lines.append(parsed)

    if course_lines:
        course = get_course(headers, course_lines)
        courses[course['course']] = course

    return {'headers': headers, 'courses': courses}

def pulse_to_time(events, objects):
    bpm = 120
    passed_beat = 0
    passed_time = 0
    eidx = 0
    oidx = 0

    times = []

    while oidx < len(objects):
        event = events[eidx] if eidx < len(events) else None
        obj_beat = objects[oidx]

        while event and event['beat'] <= obj_beat:
            if event['type'] == 'bpm':
                beat = event['beat'] - passed_beat
                time = 60 / bpm * beat

                passed_beat += beat
                passed_time += time
                bpm = float(event['value'])

            eidx += 1
            event = events[eidx] if eidx < len(events) else None

        beat = obj_beat - passed_beat
        time = 60 / bpm * beat
        times.append(passed_time + time)

        passed_beat += beat
        passed_time += time
        oidx += 1

    return times

def convert_to_timed(course):
    events = []
    notes = []
    beat = 0
    balloon = 0
    imo = False

    for measure in course['measures']:
        length = measure['length'][0] / measure['length'][1] * 4

        for event in measure['events']:
            e_beat = length / (len(measure['data']) or 1) * event['position']

            if event['name'] == 'bpm':
                events.append({
                    'type': 'bpm',
                    'value': event['value'],
                    'beat': beat + e_beat,
                })
            elif event['name'] == 'gogoStart':
                events.append({
                    'type': 'gogoStart',
                    'beat': beat + e_beat,
                })
            elif event['name'] == 'gogoEnd':
                events.append({
                    'type': 'gogoEnd',
                    'beat': beat + e_beat,
                })

        for d, ch in enumerate(measure['data']):
            n_beat = length / len(measure['data']) * d

            note = {'type': '', 'beat': beat + n_beat}

            if ch == '1':
                note['type'] = 'don'
            elif ch == '2':
                note['type'] = 'kat'
            elif ch == '3' or ch == 'A':
                note['type'] = 'donBig'
            elif ch == '4' or ch == 'B':
                note['type'] = 'katBig'
            elif ch == '5':
                note['type'] = 'renda'
            elif ch == '6':
                note['type'] = 'rendaBig'
            elif ch == '7':
                note['type'] = 'balloon'
                note['count'] = course['headers']['balloon'][balloon]
                balloon += 1
            elif ch == '8':
                note['type'] = 'end'
                if imo:
                    imo = False
            elif ch == '9':
                if not imo:
                    note['type'] = 'balloon'
                    note['count'] = course['headers']['balloon'][balloon]
                    balloon += 1
                    imo = True

            if note['type']:
                notes.append(note)

        beat += length

    # Assuming pulse_to_time is a pre-defined function
    times = pulse_to_time(events, [n['beat'] for n in notes])
    for idx, t in enumerate(times):
        notes[idx]['time'] = t

    return {'headers': course['headers'], 'events': events, 'notes': notes}

def get_statistics(course):
    # Initialize variables
    notes = [0, 0, 0, 0]
    rendas, balloons = [], []
    start, end, combo = 0, 0, 0
    renda_start = False
    balloon_start, balloon_count, balloon_gogo = False, 0, 0
    sc_cur_event_idx = 0
    sc_cur_event = course['events'][sc_cur_event_idx]
    sc_gogo = 0
    sc_notes = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    sc_balloon = [0, 0]
    sc_balloon_pop = [0, 0]
    sc_potential = 0

    type_note = ['don', 'kat', 'donBig', 'katBig']

    for i, note in enumerate(course['notes']):
        # Check and handle events
        if sc_cur_event and sc_cur_event['beat'] <= note['beat']:
            while sc_cur_event and sc_cur_event['beat'] <= note['beat']:
                if sc_cur_event['type'] == 'gogoStart':
                    sc_gogo = 1
                elif sc_cur_event['type'] == 'gogoEnd':
                    sc_gogo = 0

                sc_cur_event_idx += 1
                if sc_cur_event_idx < len(course['events']):
                    sc_cur_event = course['events'][sc_cur_event_idx]
                else:
                    sc_cur_event = None

        v1 = type_note.index(note['type']) if note['type'] in type_note else -1
        if v1 != -1:
            if i == 0:
                start = note['time']
            end = note['time']

            notes[v1] += 1
            combo += 1

            big = v1 in (2, 3)
            sc_range = (0 if combo < 10 else 1 if combo < 30 else 2 if combo < 50 else 3 if combo < 100 else 4)
            sc_notes[sc_gogo][sc_range] += 2 if big else 1

            note_score_base = (
                course['headers']['scoreInit'] +
                course['headers']['scoreDiff'] * (0 if combo < 10 else 1 if combo < 30 else 2 if combo < 50 else 4 if combo < 100 else 8)
            )

            note_score = (note_score_base // 10) * 10
            if sc_gogo:
                note_score = (note_score * 1.2 // 10) * 10
            if big:
                note_score *= 2

            sc_potential += note_score

            continue

        if note['type'] in ('renda', 'rendaBig'):
            renda_start = note['time']
            continue

        elif note['type'] == 'balloon':
            balloon_start = note['time']
            balloon_count = note['count']
            balloon_gogo = sc_gogo
            continue

        elif note['type'] == 'end':
            if renda_start:
                rendas.append(note['time'] - renda_start)
                renda_start = False
            elif balloon_start:
                balloon_length = note['time'] - balloon_start
                balloon_speed = balloon_count / balloon_length
                balloons.append([balloon_length, balloon_count])
                balloon_start = False

                if balloon_speed <= 60:
                    sc_balloon[balloon_gogo] += balloon_count - 1
                    sc_balloon_pop[balloon_gogo] += 1

    return {
        'totalCombo': combo,
        'notes': notes,
        'length': end - start,
        'rendas': rendas,
        'balloons': balloons,
        'score': {
            'score': sc_potential,
            'notes': sc_notes,
            'balloon': sc_balloon,
            'balloonPop': sc_balloon_pop,
        }
    }

@dataclass
class SongData:
    demo_start: float = 0.0
    title: str = ""
    sub: str = ""
    star: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    shinuti: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    shinuti_score: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    onpu_num: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    renda_time: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0, 0.0, 0.0])
    fuusen_total: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])

    

def parse_and_get_data(tja_file: str) -> SongData:
    """Takes in a tja fname and returns a parse_tja.SongData object"""
    ret = SongData()
    try:
        file = open(tja_file, encoding='shiftjis')
    except Exception:
        print('ShiftJIS encoding error, trying shift_jisx0213')
    try:
        file = open(tja_file, encoding='utf-8')
    except Exception:
        print('UTF-8 decode error, trying shift JIS')
    try:
        file = open(tja_file, encoding='shift_jisx0213')
    except Exception:
        print('ShiftJIS encoding error, trying shift_jis_2004')
    try:
        file = open(tja_file, encoding='shift_jis_2004')
    except Exception:
        print('ShiftJIS encoding error, trying latin-1')
    if not file: file = open(tja_file, encoding='latin-1')

    

    parsed = parse_tja(file.read())
    ret.demo_start = float(parsed['headers']['demostart'])
    ret.title = parsed['headers']['title']
    sub = parsed['headers']['subtitle']
    ret.sub = sub[2::] if sub.startswith('--') else sub 
    for i in parsed['courses'].keys():
        ret.star[i] = parsed['courses'][i]['headers']['level']
        stats = get_statistics(convert_to_timed(parsed['courses'][i]))
        ret.onpu_num[i] = stats['totalCombo']
        ret.fuusen_total[i] = sum(x[1] for x in stats['balloons'])
        ret.renda_time[i] = sum(stats['rendas'])

        #Most of the time this is correct, but you know namco is retarded and loves to overcomplicate shit
        ret.shinuti[i] = floor(100_000.0 / ret.onpu_num[i]) if ret.renda_time[i] < 0.5 else ceil(100_000.0 / ret.onpu_num[i]) * 10 
        ret.shinuti_score[i] = round(ret.shinuti[i] * ret.onpu_num[i] + 17.5 * ret.renda_time[i] * 100)
    file.close()
    return ret
        
    
if __name__ == '__main__':
    print(parse_and_get_data('C:\\Users\\knunes\\Downloads\\The Future of the Taiko Drum.tja'))
