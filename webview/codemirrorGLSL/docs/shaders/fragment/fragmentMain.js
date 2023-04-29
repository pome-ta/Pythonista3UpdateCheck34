#version 300 es
precision highp float;

/* よくあるやつ */

uniform float time;
uniform vec2 resolution;
uniform vec2 mouse;

out vec4 fragmentColor;



void main() {
  //vec2 p = (gl_FragCoord.xy * 2.0 - resolution) / min(resolution.x, resolution.y);
  vec2 uv = gl_FragCoord.xy / resolution.xy;

  vec3 outColor = vec3(uv, abs(sin(time)));
  fragmentColor = vec4(outColor, 1.0);
}

