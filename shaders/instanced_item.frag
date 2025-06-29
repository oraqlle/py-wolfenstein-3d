#version 330 core

out vec4 frag_colour;

in vec2 uv;
flat in int tex_id;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

uniform sampler2DArray u_texture_array_0;

void main() {
    vec4 tex_col = texture(u_texture_array_0, vec3(uv, tex_id));

    if (tex_col.a <= 0.1) discard;

    vec3 col = pow(tex_col.rgb, gamma);

    // fog ie. distance shadows
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w;
    col = mix(col, vec3(0.05), (1.0 - exp2(-0.015 * fog_dist * fog_dist)));

    col = pow(col, inv_gamma);
    frag_colour = vec4(col, tex_col.a);
}
