#ifdef GL_ES
precision highp float;
#endif

uniform float time;
uniform vec2 resolution;
uniform vec2 mouse;

float PI = acos(-1.0);

float pixelSize = 0.1;
float ps = 100.0 / pixelSize;

float briFilm(float l, float m) {
  return sin(6.0 * l - time) * sin(6.0 * m - time) + 1.0 /4.0;
//  return sin(6.0 * l) * sin(6.0 * m) + 1.0 /4.0;
}


void main(void) {
  vec2 p = (gl_FragCoord.xy * 2.0 - resolution) / min(resolution.x, resolution.y);
  
  p *= ps;
  vec2 id = floor(p);
  
  float x = id.x * 1.0 / ps;
  float y = id.y * 1.0 / ps;
  
  vec3 colorOut = vec3(briFilm(x, y));
  gl_FragColor = vec4(colorOut, 1.0);
}


