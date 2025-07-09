attribute vec3 position;
attribute vec3 normal;
attribute vec2 texcoord;

uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform mat4 u_normal_matrix;

varying vec3 v_position;
varying vec3 v_normal;
varying vec2 v_texcoord;

void main() {
    vec4 world_pos = u_model * vec4(position, 1.0);
    v_position = world_pos.xyz;
    v_normal = normalize((u_normal_matrix * vec4(normal, 0.0)).xyz);
    v_texcoord = texcoord;
    
    gl_Position = u_projection * u_view * world_pos;
}
