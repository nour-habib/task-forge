"""
Shared constants for DALL-E image generation.
Change these in one place to affect all builder agents.
"""

# DALL-E image size. For sizes < 1024 use DALL-E 2 (512x512).
# DALL-E 2: 256x256, 512x512, 1024x1024
# DALL-E 3: 1024x1024, 1792x1024, 1024x1792
DALL_E_IMAGE_SIZE = "512x512"
DALL_E_MODEL = "dall-e-2"  # Required for 512x512; use "dall-e-3" for 1024x1024+
