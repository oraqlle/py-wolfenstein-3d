#version 330 core

layout (location = 0) in vec3 in_position;
layout (location = 1) in int in_tex_id;
layout (location = 2) in int face_id;
layout (location = 3) in int ao_id;
layout (location = 4) in int flip_id;

uniform mat4 m_proj;
uniform mat4 m_view;

flat out int tex_id;
out vec2 uv;
out float shading;

const float ao_values[4] = float[4](0.3, 0.4, 0.6, 1.0);

const float face_shading[6] = float[6](
    1.0, 0.95,  // flats
    0.9, 0.85,  // front, back
    0.8, 0.75   // left, right
);

const vec2 uv_coords[4] = vec2[4](
    vec2(0, 0), vec2(0, 1),
    vec2(1, 0), vec2(1, 1)
);

const int uv_indices[24] = int[24](
    1, 0, 2, 1, 2, 3,  // tex coords indices of verts for even face
    3, 0, 2, 3, 1, 0,  // " odd face
    3, 1, 0, 3, 0, 2,  // " even flipped face
    1, 2, 3, 1, 0, 2   // " odd flipped face
);

void main() {
    tex_id = in_tex_id;

    int uv_index = gl_VertexID % 6 + ((face_id & 1) + flip_id * 2) * 6;
    uv = uv_coords[uv_indices[uv_index]];

    shading = face_shading[face_id] * ao_values[ao_id];

    gl_Position = m_proj * m_view * vec4(in_position, 1.0);
}
