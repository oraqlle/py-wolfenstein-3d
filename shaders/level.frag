#version 330 core

out vec4 frag_colour;

//in vec2 uv;
//flat in int tex_id;
//
//uniform sampler2DArray u_texture_array_0;

void main() {
    //vec3 tex_col = texture(u_texture_array_0, vec3(uv, tex_id)).rgb;

    //frag_colour = vec4(tex_col, 1.0);
    frag_colour = vec4(0.0, 1.0, 0.0, 1.0);
}
