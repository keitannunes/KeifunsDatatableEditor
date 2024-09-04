from tja2fumen.parsers import parse_tja
from tja2fumen.converters import convert_tja_to_fumen, fix_dk_note_types_course
from tja2fumen.writers import write_fumen
from tja2fumen.constants import COURSE_IDS
from tja2fumen.classes import TJACourse
from pydub import AudioSegment
import os, re
from src import encryption, nus3bank

def convert_and_write(tja_data: TJACourse,
                      course_name: str,
                      base_name: str,
                      single_course: bool = False) -> None:
    """Process the parsed data for a single TJA course."""
    fumen_data = convert_tja_to_fumen(tja_data)
    # fix don/ka types
    fix_dk_note_types_course(fumen_data)
    # Add course ID (e.g. '_x', '_x_1', '_x_2') to the output file's base name
    output_name = base_name
    if single_course:
        pass  # Replicate tja2bin.exe behavior by excluding course ID
    else:
        split_name = course_name.split("P")  # e.g. 'OniP2' -> ['Oni', '2']
        output_name += f"_{COURSE_IDS[split_name[0]]}"

    write_fumen(f"temp/{output_name}.bin", fumen_data)
    write_fumen(f"temp/{output_name}_1.bin", fumen_data)
    write_fumen(f"temp/{output_name}_2.bin", fumen_data)

def convert_tja_to_fumen_files(id: str, tja_file: str, sound_file: str, preview_point: float, start_point: float, out_path: str) -> None:
    # Write tja files
    if not os.path.exists('temp'):
        os.makedirs('temp')
    fumen_out = os.path.join(out_path, 'fumen', id)
    sound_out = os.path.join(out_path, 'sound')
    if not os.path.exists(fumen_out):
        os.makedirs(fumen_out)
    if not os.path.exists(sound_out):
        os.makedirs(sound_out)
    
    
    parsed_tja = parse_tja(tja_file)
    # Convert parsed TJA courses and write each course to `.bin` files
    for course_name, course in parsed_tja.courses.items():
        convert_and_write(course, course_name, id,
                            single_course=len(parsed_tja.courses) == 1)
    
    #Encrypt TJAs
    for path, subdirs, files in os.walk('temp'):
        for name in files:
            if not re.match(rf'^{id}.*\.bin$', name):
                continue
            in_path = os.path.join(path, name)
            out_path = os.path.join(fumen_out, name)
            if os.path.isfile(in_path):
                encryption.save_file(
                    file=in_path, #type: ignore
                    outdir=out_path,
                    encrypt=True,
                    is_fumen=True
                )
                os.remove(in_path)

    ### Sound Stuff
    nus3bank.ogg_or_wav_to_idsp_to_nus3bank(sound_file, os.path.join(sound_out, f'song_{id}.nus3bank'), preview_point, id)
    

        
