/* Final cover-layer crosstalk. Defaults intentionally stay at 1-4%. */

#pragma parameter OPTICS_CHROMA "Cover Colour Crosstalk" 0.04 0.0 0.20 0.01
#pragma parameter OPTICS_LUMA "Cover Luma Crosstalk" 0.02 0.0 0.12 0.005

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
uniform vec2 TextureSize;
uniform float OPTICS_CHROMA;
uniform float OPTICS_LUMA;

void main(void) {
    vec2 px = 1.0 / TextureSize;
    vec3 centre = texture2D(Texture, tex_coord).rgb;
    vec3 neighbours =
        texture2D(Texture, tex_coord + vec2(-px.x, 0.0)).rgb +
        texture2D(Texture, tex_coord + vec2( px.x, 0.0)).rgb +
        texture2D(Texture, tex_coord + vec2(0.0, -px.y)).rgb +
        texture2D(Texture, tex_coord + vec2(0.0,  px.y)).rgb;
    vec3 spread = neighbours * 0.25;
    const vec3 LUMA = vec3(0.299, 0.587, 0.114);
    float yc = dot(centre, LUMA);
    float ys = dot(spread, LUMA);
    vec3 cc = centre - vec3(yc);
    vec3 cs = spread - vec3(ys);
    gl_FragColor = vec4(clamp(
        vec3(mix(yc, ys, OPTICS_LUMA)) + mix(cc, cs, OPTICS_CHROMA),
        0.0, 1.0), 1.0);
}
#endif
