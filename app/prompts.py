PROMPTS = {
    "zootopia": {
        "positive": """
(masterpiece:1.4), (best quality:1.4), (ultra detailed:1.3), 8k uhd, sharp focus,
zootopia character, disney zootopia style, anthropomorphic animal character, furry character,
(expressive large eyes:1.3), detailed eye reflections, (glossy eyes:1.2), beautiful iris,
(soft fur texture:1.2), realistic fur details, fluffy fur, well-groomed fur,
3d rendered character, pixar rendering quality, disney animation aesthetic,
cartoon proportions, stylized anatomy, (vibrant saturated colors:1.2),
(cinematic lighting:1.3), soft studio lighting, rim lighting, ambient occlusion,
professional character design, clean geometry, smooth surfaces,
warm color palette, friendly expression, confident pose,
depth of field, bokeh background, professional photography lighting
""",
        "negative": """
(human:1.4), (realistic human:1.4), (real person:1.4), (human face:1.3), human skin,
photograph of person, photorealistic human, skin pores, wrinkles, human anatomy,
(gender change:1.5), (gender swap:1.5), (genderswap:1.5),
(deformed:1.3), (bad anatomy:1.3), (disfigured:1.3), (malformed:1.3),
(bad eyes:1.3), (cross-eyed:1.3), (extra eyes:1.3), (asymmetric eyes:1.3),
(bad hands:1.3), (extra fingers:1.3), (fused fingers:1.3), (missing fingers:1.3),
(bad proportions:1.2), (extra limbs:1.3), (missing limbs:1.2),
(facial hair:1.4), (beard:1.4), (mustache:1.4), stubble,
blurry, out of focus, low quality, low resolution, jpeg artifacts,
grainy, noisy, pixelated, compression artifacts,
ugly, distorted, mutation, mutated, extra heads, two heads,
watermark, text, signature, logo, copyright, artist name,
(dark:1.2), (gloomy:1.2), (horror:1.3), scary, creepy,
overexposed, underexposed, bad lighting, flat lighting,
duplicate, cloned, copied
"""
    },
    
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
    },
    
    "ghibli": {
        "positive": """
(masterpiece:1.4), (best quality:1.4), (ultra detailed:1.3), 8k, sharp focus,
studio ghibli style, ghibli anime, hayao miyazaki style, (ghibli aesthetic:1.3),
hand drawn art, traditional animation style, watercolor style,
soft painting, (painterly:1.2), artistic illustration,
(beautiful detailed eyes:1.2), gentle eyes, expressive eyes, warm gaze,
(soft shading:1.2), delicate shading, subtle gradients, natural shadows,
(warm lighting:1.3), golden hour lighting, soft sunlight, natural light,
nostalgic atmosphere, whimsical, peaceful, serene mood,
(detailed background:1.3), nature scenery, lush environment, 
beautiful landscape, detailed foliage, clouds, sky,
(vibrant but natural colors:1.2), earthy tones, harmonious palette,
soft colors, pastel colors, muted colors,
character focus, full body, environmental storytelling,
clean lineart, hand drawn lines, organic shapes,
dreamy atmosphere, magical realism, slice of life,
detailed clothing, flowing garments, natural fabrics,
wind effect, flowing hair, dynamic movement,
cinematic composition, rule of thirds, depth
""",
        "negative": """
(low quality:1.4), (worst quality:1.4), lowres, (bad quality:1.3),
(blurry:1.3), (out of focus:1.3), unfocused, soft focus,
(bad anatomy:1.3), (bad proportions:1.3), (deformed:1.3), (malformed:1.3),
(ugly:1.3), unattractive, gross,
(bad eyes:1.3), asymmetric eyes, cross-eyed, empty eyes,
(bad hands:1.4), (extra fingers:1.3), (fused fingers:1.3), (missing fingers:1.3),
poorly drawn hands, malformed hands,
extra limbs, missing limbs, mutation, mutated, disfigured,
(photorealistic:1.3), (realistic:1.3), (3d render:1.3), cgi,
photograph, photo, real life,
(modern anime style:1.2), (moe:1.2), (overly stylized:1.2),
sharp digital art, digital painting, cel shading,
grainy, noisy, pixelated, compression artifacts, jpeg artifacts,
(watermark:1.4), (text:1.3), (signature:1.3), (logo:1.3),
username, artist name, copyright,
(dark:1.3), (gloomy:1.2), horror, scary, creepy,
cyberpunk, sci-fi, futuristic, mechanical,
oversaturated, neon colors, artificial colors,
flat, 2d, simple shading,
cropped, cut off, out of frame,
duplicate, multiple views,
(sexual:1.4), (nsfw:1.4), inappropriate,
violence, blood, gore, weapons
"""
    }
}

SETTINGS = {
    "zootopia": {
        "steps": 30-40,
        "cfg_scale": 7-9,
        "sampler": "DPM++ 2M Karras atau Euler a",
        "clip_skip": 2,
        "lora_weight": 0.6-0.8,
        "controlnet_weight": 0.8-1.0,
        "gfpgan_visibility": 0.5-0.7,
        "denoising_strength": 0.4-0.6  
    },
    "anime": {
        "steps": 25-35,
        "cfg_scale": 7-11,
        "sampler": "DPM++ 2M Karras atau DPM++ SDE Karras",
        "clip_skip": 2,
        "lora_weight": 0.7-0.9,
        "controlnet_weight": 0.7-0.9,
        "gfpgan_visibility": 0.3-0.5,
        "denoising_strength": 0.35-0.55
    },
    "ghibli": {
        "steps": 30-45,
        "cfg_scale": 6-8,
        "sampler": "Euler a atau DPM++ 2M Karras",
        "clip_skip": 2,
        "lora_weight": 0.7-0.9,
        "controlnet_weight": 0.6-0.8,
        "gfpgan_visibility": 0.2-0.4, 
        "denoising_strength": 0.4-0.6
    }
}