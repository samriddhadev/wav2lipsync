from pydantic import BaseModel, Field
from typing import Literal, Union, Optional


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
    quality: Literal["Fast", "Improved", "Enhanced", "Experimental"] = Field(
        default="Improved", 
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


class Wav2LipConfig(BaseModel):
    """Complete configuration model for Wav2Lip processing."""
    OPTIONS: OptionsConfig = Field(default_factory=OptionsConfig)
    PADDING: PaddingConfig = Field(default_factory=PaddingConfig)
    MASK: MaskConfig = Field(default_factory=MaskConfig)
    OTHER: OtherConfig = Field(default_factory=OtherConfig)

    class Config:
        """Pydantic model configuration."""
        validate_assignment = True
        extra = "allow"  # Allow extra fields for flexibility

    def get_quality_description(self) -> str:
        """Get description for the selected quality setting."""
        descriptions = {
            "Fast": "Wav2Lip only",
            "Improved": "Wav2Lip with a feathered mask around the mouth to remove the square around the face",
            "Enhanced": "Wav2Lip + mask + GFPGAN upscaling done on the face",
            "Experimental": "Test version of applying gfpgan - see release notes"
        }
        return descriptions.get(self.OPTIONS.quality, "Unknown quality setting")

    def get_resolution_scale(self) -> int:
        """Get resolution scale factor based on output_height setting."""
        if self.OPTIONS.output_height == "half resolution":
            return 2
        elif self.OPTIONS.output_height == "full resolution":
            return 1
        else:
            return 3  # custom resolution

    def is_custom_resolution(self) -> bool:
        """Check if using custom resolution."""
        return isinstance(self.OPTIONS.output_height, int)
