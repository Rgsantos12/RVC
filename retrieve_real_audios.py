import glob
import os
import sys
import shutil
import pandas as pd

if __name__ == "__main__":
                        ## Copy files to a folder to use in UVR5 ##
    tsv_path = r"C:\Users\Utilizador\OneDrive - Universidade do Algarve\synthetic-speech-detection-dataset\fake\data\transcript.tsv"
    df_data = pd.read_csv(tsv_path, sep='\t', encoding="UTF-8")
    # inp_dir = r"C:\Users\Utilizador\OneDrive - Universidade do Algarve\synthetic-speech-detection-dataset\real"
    # out_dir = r"C:\Users\Utilizador\OneDrive\Documentos\Retrieval-based-Voice-Conversion-WebUI\selected_audios"
    # for i, (aud, text_stream) in enumerate(zip(df_data["audio"], df_data["sentence"]), start=1):
    #     inp_file = os.path.join(inp_dir, aud)
    #     dst_file = os.path.join(out_dir, f"{i}-{aud}")
    #     shutil.copyfile(src=inp_file, dst=dst_file)

                            ## Rename after going through UVR5 ##
    # inp_dir = r"C:\Users\Utilizador\OneDrive\Documentos\Retrieval-based-Voice-Conversion-WebUI\UVR5_audios"
    # out_dir = r"C:\Users\Utilizador\OneDrive\Documentos\Retrieval-based-Voice-Conversion-WebUI\selected_preprocessed_audios (UVR5)"
    # for audio_file in os.listdir(inp_dir):
    #     if audio_file not in os.listdir(out_dir):
    #         inp_file = os.path.join(inp_dir, audio_file)
    #         out_base_file = audio_file.split("_")
    #         out_base_file.pop(0)
    #         out_base_file = '_'.join([str(elem) for elem in out_base_file])
    #         dst_file = os.path.join(out_dir, out_base_file)
    #         shutil.copyfile(src=inp_file, dst=dst_file)

			        ## Rename to a final name to then preprocess the audios ##
    # inp_dir = r"C:\Users\Utilizador\OneDrive - Universidade do Algarve\synthetic-speech-detection-dataset\fake"
    # for audio_file in glob.glob(os.path.join(inp_dir, "*.wav")):
    #     inp_file = os.path.join(inp_dir, audio_file)
    #     string_name = os.path.basename(audio_file).split("_")
    #     file_name = f"{string_name[1]}_{string_name[2]}_"
    #     string_name.pop(1)
    #     string_name.pop(1)
    #     file_name = file_name + "_".join(string_name)
    #     os.rename(inp_file, os.path.join(inp_dir, file_name))