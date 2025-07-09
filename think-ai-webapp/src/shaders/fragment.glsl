precision mediump float;

uniform vec3 u_light_position;
uniform vec3 u_view_position;
uniform vec3 u_diffuse_color;
uniform vec3 u_specular_color;
uniform vec3 u_emissive_color;
uniform float u_shininess;
uniform float u_transparency;
uniform float u_consciousness_factor;

varying vec3 v_position;
varying vec3 v_normal;
varying vec2 v_texcoord;

void main() {
    vec3 normal = normalize(v_normal);
    vec3 light_dir = normalize(u_light_position - v_position);
    vec3 view_dir = normalize(u_view_position - v_position);
    vec3 reflect_dir = reflect(-light_dir, normal);
    
    // Diffuse lighting
    float diff = max(dot(normal, light_dir), 0.0);
    vec3 diffuse = diff * u_diffuse_color;
    
    // Specular lighting
    float spec = pow(max(dot(view_dir, reflect_dir), 0.0), u_shininess);
    vec3 specular = spec * u_specular_color;
    
    // Consciousness glow effect
    vec3 consciousness_glow = u_emissive_color * u_consciousness_factor;
    
    // Final color
    vec3 result = diffuse + specular + consciousness_glow;
    gl_FragColor = vec4(result, u_transparency);
}
