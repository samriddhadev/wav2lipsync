import sys
import os
import torch
import subprocess

from wav2lip.install import setup
from wav2lip.easy_functions import (format_time,
                            get_input_length,
                            get_video_details,
                            show_video)
from model.config_model import Wav2LipConfig

import logging
logger = logging.getLogger(__name__)

if not torch.cuda.is_available():
  sys.exit('No GPU in runtime. Please go to the "Runtime" menu, "Change runtime type" and select "GPU".')

setup()

def run(video_path, audio_path, output_path, config: Wav2LipConfig):
    video_file = video_path
    vocal_file = audio_path

    # Extract configuration values from Pydantic model
    quality = config.OPTIONS.quality
    output_height = config.OPTIONS.output_height
    wav2lip_version = config.OPTIONS.wav2lip_version
    use_previous_tracking_data = config.OPTIONS.use_previous_tracking_data
    nosmooth = config.OPTIONS.nosmooth
    
    # Padding settings
    U = config.PADDING.u
    D = config.PADDING.d
    L = config.PADDING.l
    R = config.PADDING.r
    
    # Mask settings
    size = config.MASK.size
    feathering = config.MASK.feathering
    mouth_tracking = config.MASK.mouth_tracking
    debug_mask = config.MASK.debug_mask
    
    # Other settings
    batch_process = config.OTHER.batch_process
    output_suffix = config.OTHER.output_suffix
    include_settings_in_suffix = config.OTHER.include_settings_in_suffix
    preview_settings = config.OTHER.preview_settings
    frame_to_preview = config.OTHER.frame_to_preview

    working_directory = os.getcwd()

    if wav2lip_version == "Wav2Lip_GAN":
        checkpoint_path = os.path.join(working_directory, "checkpoints", "Wav2Lip_GAN.pth")
    else:
        checkpoint_path = os.path.join(working_directory, "checkpoints", "Wav2Lip.pth")

    if feathering == 3:
        feathering = 5
    if feathering == 2:
        feathering = 3

    resolution_scale = 1
    res_custom = False
    if output_height == "half resolution":
        resolution_scale = 2
    elif output_height == "full resolution":
        resolution_scale = 1
    else:
        res_custom = True
        resolution_scale = 3

    in_width, in_height, in_fps, in_length = get_video_details(video_file)
    out_height = round(in_height / resolution_scale)

    if res_custom:
        out_height = int(output_height)

    fps_for_static_image = 30

    frame_to_preview = max(frame_to_preview - 1, 0)

    if include_settings_in_suffix:
        if wav2lip_version == "Wav2Lip_GAN":
            output_suffix = f"{output_suffix}_GAN"
        output_suffix = f"{output_suffix}_{quality}"
        if output_height != "full resolution":
            output_suffix = f"{output_suffix}_{out_height}"
        if nosmooth:
            output_suffix = f"{output_suffix}_nosmooth1"
        else:
            output_suffix = f"{output_suffix}_nosmooth0"
        if U != 0 or D != 0 or L != 0 or R != 0:
            output_suffix = f"{output_suffix}_pads-"
            if U != 0:
                output_suffix = f"{output_suffix}U{U}"
            if D != 0:
                output_suffix = f"{output_suffix}D{D}"
            if L != 0:
                output_suffix = f"{output_suffix}L{L}"
            if R != 0:
                output_suffix = f"{output_suffix}R{R}"
        if quality != "fast":
            output_suffix = f"{output_suffix}_mask-S{size}F{feathering}"
            if mouth_tracking:
                output_suffix = f"{output_suffix}_mt"
            if debug_mask:
                output_suffix = f"{output_suffix}_debug"
    if preview_settings:
        output_suffix = f"{output_suffix}_preview"


    rescaleFactor = str(round(1 // resolution_scale))
    pad_up = str(round(U * resolution_scale))
    pad_down = str(round(D * resolution_scale))
    pad_left = str(round(L * resolution_scale))
    pad_right = str(round(R * resolution_scale))

    cmd = [
        sys.executable,
        "-m", "wav2lip.inference.py",
        "--face",
        video_file,
        "--audio",
        vocal_file,
        "--outfile",
        output_path,
        "--pads",
        str(pad_up),
        str(pad_down),
        str(pad_left),
        str(pad_right),
        "--checkpoint_path",
        checkpoint_path,
        "--out_height",
        str(out_height),
        "--fullres",
        str(resolution_scale),
        "--quality",
        quality,
        "--mask_dilation",
        str(size),
        "--mask_feathering",
        str(feathering),
        "--nosmooth",
        str(nosmooth),
        "--debug_mask",
        str(debug_mask),
        "--preview_settings",
        str(preview_settings),
        "--mouth_tracking",
        str(mouth_tracking),
    ]

    # Run the command
    subprocess.run(cmd)






