/* Achromatic 6x14 aperture: 2px lines on an 8x16 output-pixel grid. */

#pragma parameter VIRTUAL_E_STRENGTH "Black Stripe Strength" 1.00 0.00 1.00 0.05
#pragma parameter VIRTUAL_E_DIVIDER "Black Stripe Level" 0.00 0.00 0.50 0.01

#if defined(VERTEX)
attribute vec4 VertexCoord;
attribute vec4 TexCoord;
uniform mat4 MVPMatrix;
varying vec2 tex_coord;
void main(void) {
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
uniform float VIRTUAL_E_STRENGTH;
uniform float VIRTUAL_E_DIVIDER;

void main(void) {
    vec3 original = texture2D(Texture, tex_coord).rgb;
    float phaseX = mod(floor(gl_FragCoord.x), 8.0);
    float phaseY = mod(floor(gl_FragCoord.y), 16.0);
    bool divider = phaseX >= 6.0 || phaseY >= 14.0;
    float mask = divider ? VIRTUAL_E_DIVIDER : 1.0;

    vec3 striped = original * mask;
    gl_FragColor = vec4(
        clamp(mix(original, striped, VIRTUAL_E_STRENGTH), 0.0, 1.0),
        1.0
    );
}
#endif
