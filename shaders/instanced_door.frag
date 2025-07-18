#version 330 core

out vec4 frag_colour;

in vec2 uv;
flat in int tex_id;

uniform sampler2DArray u_texture_array_0;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

void main() {
    vec3 tex_col = texture(u_texture_array_0, vec3(uv, tex_id)).rgb;
    tex_col = pow(tex_col, gamma);

    // fog ie. distance shadows
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w;
    tex_col = mix(tex_col, vec3(0.05), (1.0 - exp2(-0.015 * fog_dist * fog_dist)));

    tex_col = pow(tex_col, inv_gamma);
    frag_colour = vec4(tex_col, 1.0);
}
