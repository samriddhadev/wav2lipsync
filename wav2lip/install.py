version = 'v8.3'

import os
import shutil
import subprocess
import warnings

from enhance import load_sr
from easy_functions import load_model, load_predictor

warnings.filterwarnings("ignore", category=UserWarning, module="torchvision.transforms.functional_tensor")

model = None

# Get the location of the basicsr package
def get_basicsr_location():
    result = subprocess.run(['pip', 'show', 'basicsr'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'Location: ' in line:
            return line.split('Location: ')[1]
    return None

# Move and replace a file to the basicsr location
def move_and_replace_file_to_basicsr(file_name):
    basicsr_location = get_basicsr_location()
    if basicsr_location:
        destination = os.path.join(basicsr_location, file_name)
        # Move and replace the file
        shutil.copyfile(file_name, destination)
        print(f'File replaced at {destination}')
    else:
        print('Could not find basicsr location.')

def setup():
    file_to_replace = 'degradations.py'  # Replace with your file name
    move_and_replace_file_to_basicsr(file_to_replace)
    working_directory = os.getcwd()
    global model
    model = load_model(os.path.join(working_directory, "wav2lip", "checkpoints", "Wav2Lip_GAN.pth"))
    model = load_model(os.path.join(working_directory, "wav2lip", "checkpoints", "Wav2Lip.pth"))
    load_predictor()

    with open("installed.txt", "w") as f:
        f.write(version)
    print("Installation complete!")
