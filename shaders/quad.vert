#version 330 core

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 in_uv;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

out vec3 colour;

void main() {
    colour = vec3(0, 1, 0);
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}
