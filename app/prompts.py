PROMPTS = {
    "anime": {
        "positive": """
(masterpiece:1.4), (best quality:1.4), (ultra detailed:1.3), 8k, sharp focus,
anime style, high quality anime, modern anime aesthetic, (detailed anime art:1.3),
beautiful anime character, bishojo style, (expressive anime eyes:1.3),
(detailed eyes:1.2), sparkling eyes, vibrant iris, detailed pupils, eye highlights,
(smooth anime shading:1.2), cell shading, soft shadows, gradient shading,
clean lineart, (detailed line work:1.2), smooth lines, precise outlines,
(vibrant colors:1.2), saturated colors, vivid palette, colorful,
beautiful face, symmetrical face, detailed facial features,
(detailed hair:1.2), flowing hair, hair highlights, hair strands,
detailed clothing, intricate outfit, fashion design,
professional illustration, digital art, official art style,
(cinematic lighting:1.2), dramatic lighting, soft lighting, ambient light,
depth of field, bokeh, detailed background,
dynamic pose, confident expression, character focus
""",
        "negative": """
(low quality:1.4), (worst quality:1.4), (bad quality:1.3), lowres,
(blurry:1.3), (out of focus:1.3), unfocused, motion blur,
(bad anatomy:1.3), (bad proportions:1.3), (deformed:1.3), (disfigured:1.3),
(ugly:1.3), (gross:1.2), unattractive,
(bad face:1.3), (bad eyes:1.3), asymmetric eyes, cross-eyed, (dead eyes:1.2),
(bad hands:1.4), (extra fingers:1.3), (fused fingers:1.3), (missing fingers:1.3),
(poorly drawn hands:1.3), malformed hands, mutated hands,
extra limbs, missing limbs, extra arms, extra legs,
(mutation:1.3), (mutated:1.3), malformed, distorted,
grainy, noisy, pixelated, jpeg artifacts, compression artifacts,
(watermark:1.4), (text:1.3), (signature:1.3), (logo:1.3), artist name,
username, copyright notice, patreon username,
duplicate, cloned, multiple views, collage,
(3d:1.2), (realistic:1.2), (photorealistic:1.2), photograph,
(monochrome:1.2), greyscale, black and white,
(dark:1.2), too dark, underexposed, overexposed,
flat colors, washed out colors, desaturated,
simple background, plain background, white background (unless intended),
cropped, cut off, (out of frame:1.2)
"""
    }
}

SETTINGS = {
    "anime": {
        "steps": 28,
        "strength": 0.4,
        "lora_scale": 0.75,
        "guidance_scale": 7.5
    }
}
