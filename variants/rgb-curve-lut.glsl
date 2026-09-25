/* Per-channel 1D tone-curve lookup. The LUT stores the complete measured R,
 * G and B curves in a single 256x1 image. It is sampled in display-encoded
 * RGB space without linear-light conversion. */

#pragma parameter RGB_CURVE_STRENGTH "RGB Curve Strength" 1.00 0.00 1.00 0.01

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
uniform sampler2D RGBLUT;
uniform float RGB_CURVE_STRENGTH;

void main(void)
{
    vec3 source = texture2D(Texture, tex_coord).rgb;
    vec3 lut;
    lut.r = texture2D(RGBLUT, vec2((source.r * 255.0 + 0.5) / 256.0, 0.5)).r;
    lut.g = texture2D(RGBLUT, vec2((source.g * 255.0 + 0.5) / 256.0, 0.5)).g;
    lut.b = texture2D(RGBLUT, vec2((source.b * 255.0 + 0.5) / 256.0, 0.5)).b;
    gl_FragColor = vec4(mix(source, lut, RGB_CURVE_STRENGTH), 1.0);
}

#endif
