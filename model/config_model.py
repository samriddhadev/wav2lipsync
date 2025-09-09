from pydantic import BaseModel, Field, validator
from typing import Literal, Union
from pathlib import Path


class PaddingConfig(BaseModel):
    """Padding configuration for video processing."""
    u: int = Field(default=0, description="Upper padding")
    d: int = Field(default=0, description="Down padding") 
    l: int = Field(default=0, description="Left padding")
    r: int = Field(default=0, description="Right padding")


class MaskConfig(BaseModel):
    """Mask configuration for video processing."""
    size: float = Field(default=2.5, ge=0, description="Mask size")
    feathering: int = Field(default=2, ge=0, description="Mask feathering level")
    mouth_tracking: bool = Field(default=False, description="Enable mouth tracking")
    debug_mask: bool = Field(default=False, description="Enable debug mask visualization")


class OtherConfig(BaseModel):
    """Other miscellaneous configuration options."""
    batch_process: bool = Field(default=False, description="Enable batch processing")
    output_suffix: str = Field(default="_Easy-Wav2Lip", description="Output file suffix")
    include_settings_in_suffix: bool = Field(default=False, description="Include settings in output filename")
    preview_settings: bool = Field(default=False, description="Enable preview settings")
    frame_to_preview: int = Field(default=100, ge=1, description="Frame number to preview")


class OptionsConfig(BaseModel):
    """Main options configuration."""
    video_file: str = Field(default="", description="Input video file path")
    vocal_file: str = Field(default="", description="Input audio file path")
    quality: Literal["Fast", "Improved", "Enhanced", "Experimental"] = Field(
        default="Enhanced", 
        description="Processing quality level"
    )
    output_height: Union[Literal["full resolution", "half resolution"], int] = Field(
        default="full resolution",
        description="Output video height - can be 'full resolution', 'half resolution', or pixel height"
    )
    wav2lip_version: Literal["Wav2Lip", "Wav2Lip_GAN"] = Field(
        default="Wav2Lip",
        description="Wav2Lip model version to use"
    )
    use_previous_tracking_data: bool = Field(
        default=True,
        description="Whether to use previous tracking data"
    )
    nosmooth: bool = Field(
        default=True,
        description="Disable smoothing"
    )
    preview_window: Literal["Full"] = Field(
        default="Full",
        description="Preview window mode"
    )

    @validator('video_file')
    def validate_video_file(cls, v):
        """Validate video file exists if provided."""
        if v and not Path(v).exists():
            raise ValueError(f"Video file does not exist: {v}")
        return v

    @validator('vocal_file')
    def validate_vocal_file(cls, v):
        """Validate audio file exists if provided."""
        if v and not Path(v).exists():
            raise ValueError(f"Audio file does not exist: {v}")
        return v

    @validator('output_height')
    def validate_output_height(cls, v):
        """Validate output height is either a valid string or positive integer."""
        if isinstance(v, str):
            if v not in ["full resolution", "half resolution"]:
                raise ValueError(f"Invalid output height string: {v}")
        elif isinstance(v, int):
            if v <= 0:
                raise ValueError("Output height must be positive")
        return v


class EasyWav2LipConfig(BaseModel):
    """Complete configuration model for Easy-Wav2Lip."""
    OPTIONS: OptionsConfig = Field(default_factory=OptionsConfig)
    PADDING: PaddingConfig = Field(default_factory=PaddingConfig)
    MASK: MaskConfig = Field(default_factory=MaskConfig)
    OTHER: OtherConfig = Field(default_factory=OtherConfig)