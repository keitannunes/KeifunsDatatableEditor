from tja2fumen.parsers import parse_tja
from tja2fumen.converters import convert_tja_to_fumen, fix_dk_note_types_course
from tja2fumen.writers import write_fumen
from tja2fumen.constants import COURSE_IDS
from tja2fumen.classes import TJACourse, TJAMeasure, TJAData
from pydub import AudioSegment
import os, re
from src import encryption, nus3bank
import tempfile

def convert_and_write(tja_data: TJACourse,
                      course_name: str,
                      base_name: str,
                      single_course: bool,
                      temp_dir: str) -> None:
    """Process the parsed data for a single TJA course."""
    fumen_data = convert_tja_to_fumen(tja_data)
    # Fix don/ka types
    fix_dk_note_types_course(fumen_data)
    # Add course ID (e.g., '_x', '_x_1', '_x_2') to the output file's base name
    output_name = base_name
    if single_course:
        pass  # Replicate tja2bin.exe behavior by excluding course ID
    else:
        split_name = course_name.split("P")  # e.g., 'OniP2' -> ['Oni', '2']
        output_name += f"_{COURSE_IDS[split_name[0]]}"

    # Write to the temp_dir instead of hardcoded 'temp' directory
    write_fumen(os.path.join(temp_dir, f"{output_name}.bin"), fumen_data)
    write_fumen(os.path.join(temp_dir, f"{output_name}_1.bin"), fumen_data)
    write_fumen(os.path.join(temp_dir, f"{output_name}_2.bin"), fumen_data)

def convert_tja_to_fumen_files(id: str, tja_file: str, sound_file: str, preview_point: int, start_offset: int, out_path: str) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        fumen_out = os.path.join(out_path, 'fumen', id)
        sound_out = os.path.join(out_path, 'sound')

        if not os.path.exists(fumen_out):
            os.makedirs(fumen_out)
        if not os.path.exists(sound_out):
            os.makedirs(sound_out)

        parsed_tja = parse_tja(tja_file)

        ## Normalize audio and add measure to all courses/branches
        one_measure_ms = (60000 / parsed_tja.bpm) * 4
        offset_ms = parsed_tja.offset * 1000
        preview_point += int(one_measure_ms - offset_ms + start_offset)
        normalized_audio = nus3bank.normalize_and_add_offset(sound_file, int(offset_ms), int(one_measure_ms), start_offset, temp_dir)
        #add empty measure
        for course in parsed_tja.courses.keys():
            for branch in parsed_tja.courses[course].branches.keys():
                if parsed_tja.courses[course].branches[branch] != []:
                    parsed_tja.courses[course].branches[branch].insert(0, TJAMeasure([],[],[TJAData(name='barline', value='0', pos=0)]))
                    first_real_measure = parsed_tja.courses[course].branches[branch][1]
                    has_barline = False
                    for e in first_real_measure.combined:
                        if e.name == 'barline':
                            has_barline = True
                            break
                    if not has_barline:
                        first_real_measure.combined.append(TJAData(name='barline', value='1', pos=0))
                    print(parsed_tja.courses[course].branches[branch][0])
                    print(parsed_tja.courses[course].branches[branch][1])


        parsed_tja.offset = min(start_offset / -1000.0, 0.0)

        # Convert parsed TJA courses and write each course to `.bin` files inside temp_dir
        for course_name in parsed_tja.courses.keys():
            if start_offset > 0: parsed_tja.courses[course_name].offset = min(start_offset / -1000.0, 0.0)
            convert_and_write(parsed_tja.courses[course_name], course_name, id,
                              single_course=len(parsed_tja.courses) == 1,
                              temp_dir=temp_dir)  # Use temp_dir for output

        # Encrypt TJAs from temp_dir
        for path, subdirs, files in os.walk(temp_dir):
            for name in files:
                if not re.match(rf'^{id}.*\.bin$', name):
                    continue
                in_path = os.path.join(path, name)
                out_path = os.path.join(fumen_out, name)
                if os.path.isfile(in_path):
                    encryption.save_file(
                        file=in_path,  # type: ignore
                        outdir=out_path,
                        encrypt=True,
                        is_fumen=True
                    )
                    os.remove(in_path)

        # ### Sound Stuff
        nus3bank.wav_to_idsp_to_nus3bank(normalized_audio, os.path.join(sound_out, f'song_{id}.nus3bank'), preview_point, id) 
        if os.path.exists(normalized_audio):
            os.remove(normalized_audio)

