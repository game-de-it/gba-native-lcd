/*
 * GBA reflective LCD, pass 2: exact 4x4 logical-cell matrix for a 960x640
 * target. B/G/R transmission differences are intentionally subtle. The
 * fourth column and row form the opaque matrix boundary for each GBA dot.
 */

#pragma parameter MATRIX_FACE "Cell Transmission" 1.00 0.80 1.35 0.01
#pragma parameter MATRIX_GAP "Opaque Matrix" 0.66 0.40 1.00 0.01
#pragma parameter SUBPIXEL_STRENGTH "BGR Filter Strength" 0.22 0.00 0.70 0.01
#pragma parameter TOP_EDGE_LIGHT "Top Edge Light" 0.10 0.00 1.00 0.01
#pragma parameter SHADOW_START_LIGHT "Light at 30px" 0.30 0.10 1.00 0.01
#pragma parameter BOTTOM_LIGHT "Bottom Reflected Light" 1.80 1.00 2.00 0.01
#pragma parameter TOP_BAND_PX "Top Shadow Band Pixels" 30.0 0.0 100.0 1.0
#pragma parameter SHADOW_END_PX "Shadow Gradient End Pixels" 180.0 80.0 320.0 1.0
#pragma parameter SIDE_EDGE_LIGHT "Side Edge Light" 0.40 0.10 1.00 0.01
#pragma parameter SIDE_WIDTH_PX "Side Shadow Width Pixels" 30.0 0.0 120.0 1.0
#pragma parameter SENSOR_LIGHT_ENABLE "Sensor Edge Shadows" 1.00 0.00 1.00 1.00
#pragma parameter SENSOR_MAX_EDGE_SHADOW "Maximum Edge Shadow Reach" 180.0 30.0 600.0 1.0
#pragma parameter SENSOR_RAISE_CURVE "Raise Shadow Response" 1.00 0.40 3.00 0.05
#pragma parameter SENSOR_DEADZONE "Motion Deadzone" 0.00 0.00 0.50 0.01
#pragma parameter SENSOR_EDGE_DARKNESS "Moving Shadow Root" 0.25 0.05 0.60 0.01
#pragma parameter SENSOR_STRETCHED_DARKNESS "Stretched Shadow Root" 0.10 0.02 0.40 0.01
#pragma parameter SENSOR_FAR_LIGHT "Light Beyond Shadow" 1.00 1.00 2.50 0.05
#pragma parameter BAND_LIGHT "Soft Reflection Band Light" 1.80 1.00 2.00 0.05
#pragma parameter BAND_WIDTH "Band Horizontal Half Width" 0.46 0.20 0.49 0.01
#pragma parameter BAND_HEIGHT "Band Vertical Spread" 0.168 0.050 0.350 0.001
#pragma parameter BAND_TRAVEL "Band Motion Range" 0.30 0.00 0.40 0.01
#pragma parameter INNER_BAND_LIGHT "Inner Reflection Band Light" 1.65 1.00 2.00 0.05
#pragma parameter INNER_BAND_WIDTH "Inner Band Core Half Width" 0.16 0.05 0.35 0.01
#pragma parameter INNER_BAND_HEIGHT "Inner Band Core Half Height" 0.04 0.01 0.15 0.01
#pragma parameter INNER_BAND_FADE_WIDTH "Inner Band Fade Half Width" 0.38 0.15 0.46 0.01
#pragma parameter INNER_BAND_FADE_HEIGHT "Inner Band Fade Half Height" 0.14 0.05 0.30 0.01

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
uniform vec2 InputSize;
uniform vec2 OutputSize;
uniform float MATRIX_FACE;
uniform float MATRIX_GAP;
uniform float SUBPIXEL_STRENGTH;
uniform float TOP_EDGE_LIGHT;
uniform float SHADOW_START_LIGHT;
uniform float BOTTOM_LIGHT;
uniform float TOP_BAND_PX;
uniform float SHADOW_END_PX;
uniform float SIDE_EDGE_LIGHT;
uniform float SIDE_WIDTH_PX;
uniform float SENSOR_LIGHT_ENABLE;
uniform float SENSOR_MAX_EDGE_SHADOW;
uniform float SENSOR_RAISE_CURVE;
uniform float SENSOR_DEADZONE;
uniform float SENSOR_EDGE_DARKNESS;
uniform float SENSOR_STRETCHED_DARKNESS;
uniform float SENSOR_FAR_LIGHT;
uniform float BAND_LIGHT;
uniform float BAND_WIDTH;
uniform float BAND_HEIGHT;
uniform float BAND_TRAVEL;
uniform float INNER_BAND_LIGHT;
uniform float INNER_BAND_WIDTH;
uniform float INNER_BAND_HEIGHT;
uniform float INNER_BAND_FADE_WIDTH;
uniform float INNER_BAND_FADE_HEIGHT;
uniform vec3 Accelerometer;

float motion_axis(float value)
{
    float magnitude = clamp((abs(value) - SENSOR_DEADZONE) /
                            max(1.0 - SENSOR_DEADZONE, 0.01), 0.0, 1.0);
    return sign(value) * pow(magnitude, SENSOR_RAISE_CURVE);
}

float edge_shadow(float distance, float reach)
{
    // When an edge tilts toward the light, both the shadow width and its
    // opacity fade away. At the neutral 30px reach (or beyond), the bezel
    // root uses the full moving-shadow darkness.
    float shadow_strength = clamp(reach / max(SIDE_WIDTH_PX, 1.0), 0.0, 1.0);
    float extension = clamp((reach - SIDE_WIDTH_PX) /
                            max(SENSOR_MAX_EDGE_SHADOW - SIDE_WIDTH_PX, 1.0),
                            0.0, 1.0);
    float extended_root = mix(SENSOR_EDGE_DARKNESS,
                              SENSOR_STRETCHED_DARKNESS, extension);
    float root_light = mix(1.0, extended_root, shadow_strength);
    float edge_t = smoothstep(0.0, max(reach, 1.0), distance);
    return mix(root_light, 1.0, edge_t);
}

void main(void)
{
    vec3 colour = texture2D(Texture, tex_coord).rgb;
    vec2 phase = fract(tex_coord * TextureSize);

    float blue = 1.0 - step(0.25, phase.x);
    float green = step(0.25, phase.x) - step(0.50, phase.x);
    float red = step(0.50, phase.x) - step(0.75, phase.x);
    float boundary = max(step(0.75, phase.x), step(0.75, phase.y));

    // Each element still transmits every channel. This is a colour-filter
    // bias, not three isolated emissive lamps.
    vec3 bgr_filter =
        blue  * vec3(0.90, 0.94, 1.16) +
        green * vec3(0.92, 1.12, 0.92) +
        red   * vec3(1.16, 0.93, 0.90);
    bgr_filter = mix(vec3(1.0), bgr_filter, SUBPIXEL_STRENGTH);

    float matrix = mix(MATRIX_FACE, 1.0 - MATRIX_GAP, boundary);
    // RetroArch may allocate a power-of-two backing texture larger than the
    // active image. TexCoord then stops below 1.0 on the right/bottom edges.
    // Convert it to active-image coordinates before placing physical-panel
    // lighting in output pixels.
    vec2 content_uv = clamp(tex_coord * TextureSize / InputSize, 0.0, 1.0);
    float down = content_uv.y;
    // Three explicit regions tuned for the 960x640 KONKR panel:
    // rows 0-29 rise from 0.25 to 0.50; rows 30-179 recover from 0.50 to
    // normal light; rows 180-639 gain reflected light toward 1.80.
    // TextureSize is the 240x160 input and remains correct for the logical
    // cell phase above. Lighting boundaries, however, are specified in the
    // 960x640 output panel's physical pixels and must use OutputSize.
    float row = floor(down * OutputSize.y);
    float top_t = clamp(row / max(TOP_BAND_PX - 1.0, 1.0), 0.0, 1.0);
    float shadow_t = clamp((row - TOP_BAND_PX) /
                           max(SHADOW_END_PX - TOP_BAND_PX - 1.0, 1.0),
                           0.0, 1.0);
    float lower_t = clamp((row - SHADOW_END_PX) /
                          max(OutputSize.y - SHADOW_END_PX - 1.0, 1.0),
                          0.0, 1.0);
    float top_gradient = mix(TOP_EDGE_LIGHT, SHADOW_START_LIGHT, top_t);
    float shadow_gradient = mix(SHADOW_START_LIGHT, 1.0, shadow_t);
    float lower_reflection = mix(1.0, BOTTOM_LIGHT, lower_t);
    float static_ambient = row < TOP_BAND_PX
        ? top_gradient
        : (row < SHADOW_END_PX ? shadow_gradient : lower_reflection);

    // A face-up device has the same shadow profile on all four edges. Tilting
    // the panel makes the bezel shadow on the raised edge reach farther into
    // the LCD. The light source is fixed above the centre of the screen, so
    // pitch affects top/bottom and roll affects left/right independently.
    float sensor_available = step(0.05, length(Accelerometer));
    float tilt_x = motion_axis(clamp(Accelerometer.x, -1.0, 1.0));
    float tilt_y = motion_axis(clamp(Accelerometer.y, -1.0, 1.0));

    float top_reach = mix(SIDE_WIDTH_PX, SENSOR_MAX_EDGE_SHADOW,
                          max(tilt_y, 0.0)) * (1.0 - max(-tilt_y, 0.0));
    float bottom_reach = mix(SIDE_WIDTH_PX, SENSOR_MAX_EDGE_SHADOW,
                             max(-tilt_y, 0.0)) * (1.0 - max(tilt_y, 0.0));
    float left_reach = mix(SIDE_WIDTH_PX, SENSOR_MAX_EDGE_SHADOW,
                           max(-tilt_x, 0.0)) * (1.0 - max(tilt_x, 0.0));
    float right_reach = mix(SIDE_WIDTH_PX, SENSOR_MAX_EDGE_SHADOW,
                            max(tilt_x, 0.0)) * (1.0 - max(-tilt_x, 0.0));

    float column = floor(content_uv.x * OutputSize.x);
    float bottom_distance = OutputSize.y - 1.0 - row;
    float right_distance = OutputSize.x - 1.0 - column;
    float sensor_edges = edge_shadow(row, top_reach) *
                         edge_shadow(bottom_distance, bottom_reach) *
                         edge_shadow(column, left_reach) *
                         edge_shadow(right_distance, right_reach);

    // The end of an extended bezel shadow is neutral light (1.0). Beyond
    // that boundary, the panel increasingly faces the overhead source and
    // may exceed neutral brightness toward the opposite edge. Combine both
    // axes before applying the gain so diagonal tilt cannot multiply it twice.
    float top_light = max(tilt_y, 0.0) *
        smoothstep(top_reach, max(OutputSize.y - 1.0, top_reach + 1.0), row);
    float bottom_light = max(-tilt_y, 0.0) *
        smoothstep(bottom_reach, max(OutputSize.y - 1.0,
                                     bottom_reach + 1.0), bottom_distance);
    float left_light = max(-tilt_x, 0.0) *
        smoothstep(left_reach, max(OutputSize.x - 1.0, left_reach + 1.0), column);
    float right_light = max(tilt_x, 0.0) *
        smoothstep(right_reach, max(OutputSize.x - 1.0,
                                    right_reach + 1.0), right_distance);
    float far_light_amount = sqrt(clamp(max(top_light, bottom_light) +
                                        max(left_light, right_light),
                                        0.0, 1.0));
    float sensor_far_light = mix(1.0, SENSOR_FAR_LIGHT, far_light_amount);
    float sensor_ambient = sensor_edges * lower_reflection * sensor_far_light;
    float use_sensor = SENSOR_LIGHT_ENABLE * sensor_available;
    float ambient = mix(static_ambient, sensor_ambient, use_sensor);

    // A broad Gaussian reflection has no rectangular boundary and therefore
    // merges into the existing panel light. It rests at screen centre and
    // moves toward the illuminated side as the opposite bezel shadow grows.
    vec2 band_center = vec2(0.5) +
        vec2(-tilt_x, tilt_y) * BAND_TRAVEL * use_sensor;
    float band_x_distance = abs(content_uv.x - band_center.x);
    float band_horizontal = 1.0 - smoothstep(
        max(BAND_WIDTH - 0.08, 0.0), BAND_WIDTH, band_x_distance);
    float band_y_delta = (content_uv.y - band_center.y) /
        max(BAND_HEIGHT, 0.01);
    float band_vertical = exp(-0.5 * band_y_delta * band_y_delta);
    float band_amount = band_horizontal * band_vertical;
    float outer_band_gain = mix(1.0, BAND_LIGHT, band_amount);

    // A smaller, independent reflection sits inside the broad band. Blend
    // toward its absolute light level instead of multiplying both bands.
    float inner_band_horizontal = 1.0 - smoothstep(
        INNER_BAND_WIDTH, max(INNER_BAND_FADE_WIDTH,
                              INNER_BAND_WIDTH + 0.001),
        band_x_distance);
    float inner_band_y_distance = abs(content_uv.y - band_center.y);
    float inner_band_vertical = 1.0 - smoothstep(
        INNER_BAND_HEIGHT, max(INNER_BAND_FADE_HEIGHT,
                               INNER_BAND_HEIGHT + 0.001),
        inner_band_y_distance);
    float inner_band_amount = inner_band_horizontal * inner_band_vertical;
    float band_gain = mix(outer_band_gain, INNER_BAND_LIGHT,
                          inner_band_amount);
    ambient *= band_gain;

    float edge_distance = min(column, OutputSize.x - 1.0 - column);
    float side_t = smoothstep(0.0, max(SIDE_WIDTH_PX, 1.0), edge_distance);
    float side_light = mix(SIDE_EDGE_LIGHT, 1.0, side_t);
    ambient *= mix(side_light, 1.0, use_sensor);

    gl_FragColor = vec4(clamp(colour * bgr_filter * matrix * ambient,
                              0.0, 1.0), 1.0);
}

#endif
