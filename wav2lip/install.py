version = 'v8.3'

import os
import shutil
import subprocess
import warnings

from wav2lip.enhance import load_sr
from wav2lip.easy_functions import load_model, load_predictor

warnings.filterwarnings("ignore", category=UserWarning, module="torchvision.transforms.functional_tensor")

model = None

# Move and replace a file to the basicsr location
def move_and_replace_file_to_basicsr(source, file_name):
    basicsr_location = os.path.join(os.getcwd(), '.venv', 'lib', 'python3.12', 'site-packages', 'basicsr', 'data')
    if basicsr_location:
        destination = os.path.join(basicsr_location, file_name)
        # Move and replace the file
        shutil.copyfile(source, destination)
        print(f'File replaced at {destination}')
    else:
        print('Could not find basicsr location.')

def setup():
    working_directory = os.getcwd()
    file_name = "degradations.py"  # Replace with your file name
    file_to_replace = os.path.join(working_directory, "wav2lip", file_name)  # Replace with your file name
    move_and_replace_file_to_basicsr(file_to_replace, file_name)
    global model
    model = load_model(os.path.join(working_directory, "wav2lip", "checkpoints", "Wav2Lip_GAN.pth"))
    model = load_model(os.path.join(working_directory, "wav2lip", "checkpoints", "Wav2Lip.pth"))
    load_predictor()

    with open("installed.txt", "w") as f:
        f.write(version)
    print("Installation complete!")
