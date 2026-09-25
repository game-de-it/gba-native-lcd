/*
 * GBA reflective TFT response.
 *
 * The effect is deliberately shorter and weaker than the Game Gear STN
 * model. Falling transitions retain a finite trail while rising transitions
 * settle quickly. Feedback alpha stores the age of the falling transition.
 */

#pragma parameter GHOST_RISE "LCD Rise Speed" 0.81 0.50 1.00 0.01
#pragma parameter GHOST_FRAMES "LCD Ghost Frames" 6.0 1.0 12.0 1.0

#if defined(VERTEX)
attribute vec4 VertexCoord;
attribute vec4 TexCoord;
varying vec2 vTex;
uniform mat4 MVPMatrix;
void main(void) {
    gl_Position = MVPMatrix * VertexCoord;
    vTex = TexCoord.xy;
}
#elif defined(FRAGMENT)
#ifdef GL_ES
#ifdef GL_FRAGMENT_PRECISION_HIGH
precision highp float;
#else
precision mediump float;
#endif
#endif
varying vec2 vTex;
uniform sampler2D Texture;
uniform sampler2D FeedbackTexture;
uniform float GHOST_RISE;
uniform float GHOST_FRAMES;

void main(void) {
    vec3 current = texture2D(Texture, vTex).rgb;
    vec4 feedback = texture2D(FeedbackTexture, vTex);
    vec3 history = feedback.rgb;

    float frames = max(GHOST_FRAMES, 1.0);
    float previous_age = floor(feedback.a * frames + 0.5);
    vec3 delta = abs(history - current);
    float largest_delta = max(max(delta.r, delta.g), delta.b);
    float changed = step(2.0 / 255.0, largest_delta);
    float falling_delta = max(max(history.r - current.r,
                                  history.g - current.g),
                                  history.b - current.b);
    float falling = step(2.0 / 255.0, falling_delta) * changed;
    float next_age = min(previous_age + 1.0, frames) * falling;
    float remaining = max(frames - previous_age, 1.0);
    float next_remaining = max(frames - next_age, 0.0);
    float retention = (next_remaining * next_remaining) /
                      (remaining * remaining);
    float fall_speed = mix(1.0, 1.0 - retention, falling);
    vec3 rising = step(history, current);
    vec3 speed = mix(vec3(fall_speed), vec3(GHOST_RISE), rising);
    vec3 response = mix(history, current, speed);
    response = mix(current, response, changed);

    gl_FragColor = vec4(response, next_age / frames);
}
#endif
