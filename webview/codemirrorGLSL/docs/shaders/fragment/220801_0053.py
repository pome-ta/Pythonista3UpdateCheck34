#version 300 es
precision highp float;

uniform float time;
uniform vec2 resolution;
uniform vec2 mouse;

out vec4 fragmentColor;

const vec3 camPos = vec3(0.0, 0.0, 3.0);
const vec3 camDir = vec3(0.0, 0.0, -1.0);
const vec3 camUp = vec3(0.0, 1.0, 0.0);

const vec3 lightDir = vec3(-0.57, 0.57, 0.57);

float distFuncTorus(vec3 p) {
  vec2 t = vec2(0.75, 0.25);
  vec2 r = vec2(length(p.xy) - t.x, p.z);
  // vec2 r = vec2(length(p.xz) - t.x, p.y);
  return length(r) - t.y;
}

float distFuncFloor(vec3 p) {
  return dot(p, vec3(0.0, 1.0, 0.0)) + 1.0;
}

float distFunc(vec3 p) {
  float d1 = distFuncTorus(p);
  float d2 = distFuncFloor(p);
  return min(d1, d2);
}

vec3 genNormal(vec3 p) {
  float d = 0.0001;
  return normalize(vec3(
    distFunc(p + vec3(d, 0.0, 0.0)) - distFunc(p + vec3(-d, 0.0, 0.0)),
    distFunc(p + vec3(0.0, d, 0.0)) - distFunc(p + vec3(0.0, -d, 0.0)),
    distFunc(p + vec3(0.0, 0.0, d)) - distFunc(p + vec3(0.0, 0.0, -d))
  ));
}


void main() {
  vec2 p = (gl_FragCoord.xy * 2.0 - resolution) / min(resolution.x, resolution.y);

  vec3 camSide = cross(camDir, camUp);
  float targetDepth = 1.0;
  vec3 ray = normalize(camSide * p.x + camUp * p.y + camDir * targetDepth);

  /* marching loop */
  float tmp, dist;
  tmp = 0.0;
  vec3 disPos = camPos;
  for (int i = 0; i < 512; i++) {
    dist = distFunc(disPos);
    tmp += dist;
    disPos = camPos + tmp * ray;
  }

  /* hit check */
  vec3 color = vec3(0.0);
  if (abs(dist) < 0.001) {
    vec3 normal = genNormal(disPos);
    float diff = clamp(dot(lightDir, normal), 0.1, 1.0);
    color = vec3(1.0, 1.0, 1.0) * diff;
  } 

  fragmentColor = vec4(color, 1.0);
}
