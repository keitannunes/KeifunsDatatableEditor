from typing import LiteralString

from src.tja2fumen.parsers import parse_tja, parse_fumen
from src.tja2fumen.converters import convert_tja_to_fumen, fix_dk_note_types_course
from src.tja2fumen.writers import write_fumen
from src.tja2fumen.constants import COURSE_IDS
from src.tja2fumen.classes import TJACourse, TJAMeasure, TJAData
from pydub import AudioSegment
import os, re
from src import encryption, nus3bank
import tempfile, shutil

def convert_and_write(tja_data: TJACourse,
                      course_name: str,
                      base_name: str,
                      single_course: bool,
                      temp_dir: str) -> list[str]:
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
    out_files = [f"{output_name}.bin", f"{output_name}_1.bin", f"{output_name}_2.bin"]
    for i in range(3):
        out_files[i] = os.path.join(temp_dir, out_files[i])
        write_fumen(out_files[i], fumen_data)

    return out_files

def normalize_fumen(sound_file: str, offset_ms: float, bpm: float) -> tuple[float, float]:
    """
    Normalizes the fumen by adding a measure before the song starts.
    If the offset is positive, it adds both the offset and a full measure.
    If the offset is negative and less than one measure long, it extends it to a full measure.

    Args:
        sound_file (str): The file path to the sound file.
        offset_ms (float): The song's offset in milliseconds.
        bpm (float): The beats per minute (BPM) of the song.

    Returns:
        float, float: 
            - The updated offset in milliseconds.
            - The difference between the original offset and the updated offset in milliseconds.
    """

    one_measure_ms = (60000.0 / bpm) * 4.0
    
    if offset_ms >= 0.0:
        # For positive offsets, add both the offset and a full measure
        length_to_add = offset_ms + one_measure_ms
        nus3bank.prepend_silent_to_audio(sound_file, int(length_to_add))
        return -one_measure_ms, length_to_add
    else:
        # For negative offsets
        offset_ms_pos = -offset_ms
        if offset_ms_pos <= one_measure_ms:
            # Offset is less than one measure, extend it to become one measure long
            length_to_add = one_measure_ms - offset_ms_pos
            nus3bank.prepend_silent_to_audio(sound_file, int(length_to_add))
            return -one_measure_ms, length_to_add
        else:
            # Offset is already longer than one measure, no change needed
            return offset_ms, 0.0



def convert_tja_to_fumen_files(song_id: str, tja_file: str, audio_file: str, preview_point_ms: float, start_blank_length_ms: float, out_path: str) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        fumen_out = os.path.join(out_path, 'fumen', song_id)
        sound_out = os.path.join(out_path, 'sound')

        if not os.path.exists(fumen_out):
            os.makedirs(fumen_out)
        if not os.path.exists(sound_out):
            os.makedirs(sound_out)

        parsed_tja = parse_tja(tja_file)

        temp_audio_path = nus3bank.convert_to_wav(audio_file, temp_dir)

        ## Normalize audio and add measure to all courses/branches
        offset_ms: float = parsed_tja.offset * 1000
        
        offset_ms, length_added = normalize_fumen(temp_audio_path, offset_ms, parsed_tja.bpm)

        preview_point_ms += length_added

        if start_blank_length_ms > 0:
            preview_point_ms += start_blank_length_ms
            nus3bank.prepend_silent_to_audio(temp_audio_path, int(start_blank_length_ms))
            offset_ms -= start_blank_length_ms

        offset_s = offset_ms / 1000
        parsed_tja.offset = offset_s

        # Convert parsed TJA courses and write each course to `.bin` files inside temp_dir
        print(parsed_tja.courses.keys())
        for course_name in parsed_tja.courses.keys():
            parsed_tja.courses[course_name].offset = offset_s
            convert_and_write(parsed_tja.courses[course_name], course_name, song_id,
                              single_course=len(parsed_tja.courses) == 1,
                              temp_dir=temp_dir)  # Use temp_dir for output

        # Encrypt TJAs from temp_dir
        for path, subdirs, files in os.walk(temp_dir):
            for name in files:
                if not re.match(rf'^{song_id}.*\.bin$', name):
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

        #Convert to nus3bank and export
        nus3bank.wav_to_idsp_to_nus3bank(temp_audio_path, os.path.join(sound_out, f'song_{song_id}.nus3bank'), int(preview_point_ms), song_id)

def get_offset_from_file(fumen_file: LiteralString | str | bytes ) -> float:
    with tempfile.TemporaryDirectory() as temp_dir:
        decrypted_file = os.path.join(temp_dir, 'decrypted.bin')
        encryption.save_file(
            file=fumen_file,  # type: ignore
            outdir=decrypted_file,
            encrypt=False,
            is_fumen=True
        )
        parsed = parse_fumen(decrypted_file)
        return parsed.measures[0].offset_start / 1000

def add_ura_to_song(song_id, tja_file, out_path) -> None:
    fumen_out_dir = os.path.join(out_path, 'fumen', song_id)
    fumen_in = os.path.join(fumen_out_dir, f'{song_id}_m.bin') #Out dir is also in dir for the fumen file in to get offset
    if not os.path.isfile(fumen_in):
        raise Exception(f'file {fumen_in} not found')

    offset_s = get_offset_from_file(fumen_in) * -1

    with tempfile.TemporaryDirectory() as temp_dir:
        parsed_tja = parse_tja(tja_file)
        offset_s -= 4 * 60 / parsed_tja.bpm
        parsed_tja.offset = offset_s
        course = 'Ura'
        parsed_tja.courses[course].offset = offset_s
        unencrypted_files = convert_and_write(parsed_tja.courses[course], course, song_id,
                          False,
                          temp_dir=temp_dir)  # Use temp_dir for output
        for in_path in unencrypted_files:
            if os.path.isfile(in_path):
                encryption.save_file(
                    file=in_path,  # type: ignore
                    outdir=os.path.join(fumen_out_dir, os.path.basename(in_path)),
                    encrypt=True,
                    is_fumen=True
                )