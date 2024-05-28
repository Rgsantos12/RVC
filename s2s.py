import argparse
import glob
import os
import sys
import shutil
import pandas as pd
from distutils import util
from gradio_client import Client


def str2bool(v):
    return bool(util.strtobool(v))


def initParams():
    parser = argparse.ArgumentParser(description=__doc__)
    # Voice arguments
    parser.add_argument(
        "--path_to_index",
        type=str,
        help="index voice path",
        default="logs/AUTO (WALL-E_Latin American Dub) - Weights.gg Model/auto_model.index",
        required=False,
    )
    parser.add_argument(
        "--is_male_voice",
        type=str2bool,
        nargs="?",
        const=True,
        default=True,
        required=False,
        help="whether the downloaded voice is male or not (low pitched/high pitched)",
    )
    # Audio configurations
    parser.add_argument(
        "-i",
        "--inp_dir",
        type=str,
        help="input directory path",
        default="processed_audios_by_uvr5/",
        required=False,
    )

    # You can add more choices for input format
    parser.add_argument(
        "--inp_format",
        type=str,
        help="input audio format",
        default="wav",
        required=False,
    )

    parser.add_argument(
        "-o",
        "--out_dir",
        type=str,
        help="output directory path",
        default="output_audios/AUTO",
        required=False,
    )
    args = parser.parse_args()
    return args


def convert_voice(voice_idx_path, audio_path, transpose):
    # Generate audio using voice conversion (speech-to-speech)
    result = client.predict(
        # float (numeric value between 0 and 2333) in 'Select Speaker/Singer ID:
        0,
        # str  in 'Enter the path of the audio file to be processed (default is the correct format example):'
        audio_path,
        # float  in 'Transpose (integer, number of semitones, raise by an octave: 12, lower by an octave: -12):'
        transpose,
        # str (filepath on your computer (or URL) of file) in 'F0 curve file (optional). One pitch per line.
        # Replaces the default F0 and pitch modulation:'
        # Cant pass "None"
        "./assets/sample_file.pdf",
        # str in 'Select the pitch extraction algorithm ('pm': faster extraction but lower-quality speech;
        # 'harvest': better bass but extremely slow; 'crepe': better quality but GPU intensive),
        # 'rmvpe': best quality, and little GPU requirement)'
        "rmvpe",
        # str  in 'Path to the feature index file. Leave blank to use the selected result from the dropdown:'
        "",
        # str in 'Auto-detect index path and select from the dropdown:'
        voice_idx_path,
        # float (numeric value between 0 and 1) in
        # 'Search feature ratio (controls accent strength, too high has artifacting):'
        0.75,
        # float (numeric value between 0 and 7) in
        # 'If >=3: apply median filtering to the harvested pitch results.
        # The value represents the filter radius and can reduce breathiness.'
        3,
        # float (numeric value between 0 and 48000) in
        # 'Resample the output audio in post-processing to the final sample rate. Set to 0 for no resampling:'
        0,
        # float (numeric value between 0 and 1) in 'Adjust the volume envelope scaling.
        # Closer to 0, the more it mimicks the volume of the original vocals.
        # Can help mask noise and make volume sound more natural when set relatively low.
        # Closer to 1 will be more of a consistently loud volume:'
        0.25,
        # float (numeric value between 0 and 0.5) in
        # 'Protect voiceless consonants and breath sounds to prevent artifacts such as tearing in electronic music.
        # Set to 0.5 to disable. Decrease the value to increase protection, but it may reduce indexing accuracy:'
        0.33,
        api_name="/infer_convert",
    )
    return result


if __name__ == "__main__":
    args = initParams()

    # Connect to the client
    client = Client("http://localhost:7865/")

    # Choose the voice you want to use
    use_voice = args.path_to_index

    # Create output folder
    out_dir = args.out_dir
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for audio_file in glob.glob(os.path.join(args.inp_dir, f"*.{args.inp_format}")):
        audio_name = os.path.basename(audio_file)
        audio_new_name = (
            f'fake_{audio_name.split("-")[0]}_rvc_'
            + os.path.basename(use_voice).split(".")[0]
            + "_audio.wav"
        )

        audio_flag = audio_name.split("_")[-1].split(".")[0]
        # Flag found (High Pitch)
        if audio_flag == "f":
            if args.is_male_voice:
                # F - M
                result = convert_voice(use_voice, audio_file, transpose=-12)
            else:
                # F - F
                result = convert_voice(use_voice, audio_file, transpose=0)
        # Flag not found (Low Pitch)
        else:
            if args.is_male_voice:
                # M - M
                result = convert_voice(use_voice, audio_file, transpose=0)
            else:
                # M - F
                result = convert_voice(use_voice, audio_file, transpose=12)

        # Move the converted audio to out_dir
        converted_audio_path = result[1]
        shutil.move(converted_audio_path, f"{out_dir}/{audio_new_name}")
        print(f"Converted {audio_name} using {os.path.basename(use_voice)}")
