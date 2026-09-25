# Tuning notes

The first preset is intentionally conservative. It should remain readable on a
640-line handheld display and avoid the heavy darkening common in desktop LCD
shaders.

## Visual targets

1. Preserve the exact 4x mapping from 240 x 160 to 960 x 640.
2. Reproduce a strong vertical pixel boundary and a weaker horizontal boundary,
   as seen in the supplied macro photograph, without a CRT-style scanline.
3. Keep RGB subpixel separation restrained; the reference is dominated by dark
   aperture lines rather than rainbow fringing.
4. Reduce contrast and mix adjacent color channels to suggest the original LCD.
5. Add a small blue/cyan frontlight cast without hiding dark detail.

## Parameters to compare on hardware

- `LCD Color Response`: channel mixing and original-panel color character.
- `LCD Saturation`: lowers the vivid emulator output toward the photographed LCD.
- `LCD Contrast`: lower values flatten the image like a reflective LCD.
- `LCD Brightness`: compensates for luminance lost to the simulated aperture.
- `LCD Pixel Bleed`: spatial response softness; this is not temporal ghosting.
- `Vertical Pixel Grid`: the dominant dark vertical aperture boundary.
- `Horizontal Pixel Grid`: the finer horizontal aperture boundary.
- `RGB Subpixels`: colored stripe visibility inside each source pixel.
- `Frontlight Blue Cast`: subtle cool cast visible in the supplied GBA SP photos.
- `RGB Aperture Strength`: visibility of the stock panel's vertical R/G/B elements.
- `Pixel Column Gap`: dark fourth column between logical pixels at exact 4x output.

## Reflective-light model

The original GBA has no internal backlight. The shader therefore avoids an
emissive lamp curve. `Reflected Light Gradient` increases ambient reflection
from top to bottom, while `Upper Bezel Shadow` and `Bezel Shadow Depth` model
the shadow cast over a recessed, non-laminated panel by the upper shell edge.

Softness is not provided by linear filtering. The panel pass spreads chroma
through neighbouring source cells while preserving most centre luminance; the
final optics pass repeats the same principle over physical output pixels.

Temporal response should be considered only after this optical baseline has
been tested. It needs frame history and may introduce visible trails or extra
GPU cost.
