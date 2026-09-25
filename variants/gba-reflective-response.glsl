/*
 * GBA reflective LCD, pass 1: source-cell response.
 *
 * The original TFT does not behave like a soft-focus lens. Only four percent
 * of the source-cell colour is shared with its direct neighbours. Reflective
 * tone response is handled separately: black has a small ambient floor and
 * bright colours reflect proportionally more of the incident light.
 */

#pragma parameter SRC_BLEND "Neighbour Cell Blend" 0.04 0.00 0.12 0.005
#pragma parameter BLACK_FLOOR "Reflected Black Floor" 0.12 0.00 0.22 0.005
#pragma parameter WHITE_LEVEL "Reflected White Ceiling" 0.78 0.60 1.00 0.01
#pragma parameter HIGHLIGHT_REFLECT "Highlight Reflectance" 0.01 0.00 0.20 0.005
#pragma parameter PANEL_COOL_V2 "Reflective Panel Cool Cast" 0.09 0.00 0.20 0.005
#pragma parameter PANEL_SAT_V2 "Reflective Panel Saturation" 0.52 0.30 1.10 0.01
#pragma parameter PANEL_GAMMA_V2 "Reflective Panel Gamma" 0.90 0.50 1.50 0.01
#pragma parameter HUE_CORRECTION "Original LCD Hue Response" 1.00 0.00 1.00 0.05
#pragma parameter ORANGE_R "Orange Red Transmission" 0.87 0.00 1.20 0.01
#pragma parameter ORANGE_G "Orange Green Transmission" 0.40 0.00 1.20 0.01
#pragma parameter ORANGE_B "Orange Blue Transmission" 0.60 0.00 1.20 0.01
#pragma parameter RED_R "Red Red Transmission" 0.275 0.00 1.20 0.005
#pragma parameter RED_G "Red Green Transmission" 0.29 0.00 1.20 0.01
#pragma parameter RED_B "Red Blue Transmission" 0.28 0.00 1.20 0.01
#pragma parameter GREEN_R "Green Red Transmission" 0.82 0.00 1.20 0.01
#pragma parameter GREEN_G "Green Green Transmission" 0.78 0.00 1.20 0.01
#pragma parameter GREEN_B "Green Blue Transmission" 0.61 0.00 1.20 0.01

#if defined(VERTEX)

attribute vec4 VertexCoord;
attribute vec4 TexCoord;
uniform mat4 MVPMatrix;
varying vec2 tex_coord;

void main(void)
{
    gl_Position = MVPMatrix * VertexCoord;
    tex_coord = TexCoord.xy;
}

#elif defined(FRAGMENT)

#ifdef GL_ES
#ifdef GL_FRAGMENT_PRECISION_HIGH
precision highp float;
#else
precision mediump float;
#endif
#endif

varying vec2 tex_coord;
uniform sampler2D Texture;
uniform vec2 TextureSize;
uniform float SRC_BLEND;
uniform float BLACK_FLOOR;
uniform float WHITE_LEVEL;
uniform float HIGHLIGHT_REFLECT;
uniform float PANEL_COOL_V2;
uniform float PANEL_SAT_V2;
uniform float PANEL_GAMMA_V2;
uniform float HUE_CORRECTION;
uniform float ORANGE_R;
uniform float ORANGE_G;
uniform float ORANGE_B;
uniform float RED_R;
uniform float RED_G;
uniform float RED_B;
uniform float GREEN_R;
uniform float GREEN_G;
uniform float GREEN_B;

const vec3 LUMA = vec3(0.299, 0.587, 0.114);

void main(void)
{
    vec2 texel = 1.0 / TextureSize;
    vec3 centre = texture2D(Texture, tex_coord).rgb;
    vec3 neighbours =
        texture2D(Texture, tex_coord + vec2(-texel.x, 0.0)).rgb +
        texture2D(Texture, tex_coord + vec2( texel.x, 0.0)).rgb +
        texture2D(Texture, tex_coord + vec2(0.0, -texel.y)).rgb +
        texture2D(Texture, tex_coord + vec2(0.0,  texel.y)).rgb;
    vec3 colour = centre * (1.0 - SRC_BLEND) + neighbours * (SRC_BLEND * 0.25);
    vec3 source_colour = colour;

    float y = dot(colour, LUMA);
    colour = mix(vec3(y), colour, PANEL_SAT_V2);

    // Reflected black is dark grey rather than emissive zero. The smooth
    // highlight term raises pale colours without turning the panel into a
    // backlit display.
    // Compress the available reflective range at both ends. Unlike an IPS,
    // the unlit panel never reaches display black or emissive white.
    colour = pow(max(colour, vec3(0.0)), vec3(PANEL_GAMMA_V2));
    colour = vec3(BLACK_FLOOR) + colour * (WHITE_LEVEL - BLACK_FLOOR);
    colour += vec3(HIGHLIGHT_REFLECT * smoothstep(0.58, 1.0, y) * (1.0 - y));
    colour *= vec3(1.0 - PANEL_COOL_V2 * 0.72,
                   1.0 - PANEL_COOL_V2 * 0.28,
                   1.0 + PANEL_COOL_V2);

    float red = source_colour.r;
    float green = source_colour.g;
    float blue = source_colour.b;
    float orange_mask =
        smoothstep(0.65, 0.90, red) *
        smoothstep(0.35, 0.62, green) *
        (1.0 - smoothstep(0.18, 0.38, blue)) *
        smoothstep(0.10, 0.35, red - green);
    float red_mask =
        smoothstep(0.65, 0.90, red) *
        (1.0 - smoothstep(0.18, 0.42, green)) *
        smoothstep(0.30, 0.65, red - green) *
        smoothstep(0.25, 0.60, red - blue);
    float green_mask =
        smoothstep(0.30, 0.62, green) *
        smoothstep(0.06, 0.28, green - red) *
        smoothstep(0.04, 0.26, green - blue);

    vec3 correction = vec3(1.0);
    correction = mix(correction, vec3(ORANGE_R, ORANGE_G, ORANGE_B),
                     orange_mask * HUE_CORRECTION);
    correction = mix(correction, vec3(RED_R, RED_G, RED_B),
                     red_mask * HUE_CORRECTION);
    correction = mix(correction, vec3(GREEN_R, GREEN_G, GREEN_B),
                     green_mask * HUE_CORRECTION);
    colour *= correction;

    gl_FragColor = vec4(clamp(colour, 0.0, 1.0), 1.0);
}

#endif
