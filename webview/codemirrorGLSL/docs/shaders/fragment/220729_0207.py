#version 300 es

/* タイムストップと、画面操作 */
precision highp float;

uniform float time;
uniform vec2 resolution;
uniform vec2 mouse;

out vec4 fragmentColor;

void main(void) {
  vec2 m = vec2(mouse.x * 2.0 - 1.0, -mouse.y * 2.0 + 1.0);
  vec2 p = (gl_FragCoord.xy * 2.0 - resolution) / min(resolution.x, resolution.y);
  float t = sin(length(m - p) * 30.0 + time * 5.0);
  fragmentColor = vec4(vec3(t), 1.0);
}
