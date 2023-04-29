#version 300 es
precision highp float;

in vec3 vertexPosition;

void main(void){
    gl_Position = vec4(vertexPosition, 1.0);
}
