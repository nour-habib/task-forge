"""
Shared constants for image generation.
IMAGE_MODEL is read from env; change .env to switch models.
"""

import os

# Image model from env (e.g. gpt-image-1, dall-e-2, dall-e-3)
IMAGE_MODEL = os.getenv("IMAGE_MODEL", "gpt-image-1")

# Image size. For sizes < 1024 use DALL-E 2 (512x512).
# DALL-E 2: 256x256, 512x512, 1024x1024
# DALL-E 3: 1024x1024, 1792x1024, 1024x1792
DALL_E_IMAGE_SIZE = "512x512"
