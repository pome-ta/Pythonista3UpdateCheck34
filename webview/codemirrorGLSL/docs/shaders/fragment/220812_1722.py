#version 300 es
precision highp float;

uniform float time;
uniform vec2 resolution;
uniform vec2 mouse;

out vec4 fragmentColor;

const vec3 camPos = vec3(0.0, 4.0, 7.0);
const vec3 camDir = vec3(0.0, -0.707, -0.707);
const vec3 camUp = vec3(0.0, 0.707, -0.707);

const vec3 lightDir = vec3(-0.57, 0.57, 0.57);

float distFuncTorus(vec3 p) {
  p.xz -= mouse * 2.0 - 1.0;
  vec2 t = vec2(3.0, 1.0);
  vec2 r = vec2(length(p.xz) - t.x, p.y);
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

float genShadow(vec3 ro, vec3 rd) {
  float h = 0.0;
  float c = 0.001;
  float r = 1.0;
  float shadowCoef = 0.5;
  for (float t = 0.0; t < 50.0; t++) {
    h = distFunc(ro + rd * c);
    if (h < 0.001) {
      return shadowCoef;
    }
    r = min(r, h * 16.0 / c);
    c += h;
  }
  return mix(shadowCoef, 1.0, r);
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
  for (int i = 0; i < 256; i++) {
    dist = distFunc(disPos);
    if (dist < 0.001){ break; }
    tmp += dist;
    disPos = camPos + tmp * ray;
  }

  /* light offset */
  vec3 light = normalize(lightDir + vec3(sin(time), 0.0, 0.0));

  /* hit check */
  vec3 color = vec3(0.0);
  float shadow = 1.0;
  if (abs(dist) < 0.001) {
    /* generate normal */
    vec3 normal = genNormal(disPos);
    
    /* light */
    vec3 halfLE = normalize(light - ray);
    float diff = clamp(dot(light, normal), 0.1, 1.0);
    float spec = pow(clamp(dot(halfLE, normal), 0.0, 1.0), 50.0);
    
    /* generate shadow */
    shadow = genShadow(disPos + normal * 0.001, light);
    
    /* generate tile pattern */
    //float u = 1.0 - floor(mod(disPos.x, 2.0));
    float u = 1.0 - floor(mod(disPos.x, 2.0));
    float v = 1.0 - floor(mod(disPos.z, 2.0));
    if ((u == 1.0 && v < 1.0) || (u < 1.0 && v == 1.0)) {
      diff *= 0.7;
    }
    color = vec3(1.0, 1.0, 1.0) * diff + vec3(spec);
    //color = vec3(1.0, 1.0, 1.0) * normal;
  }
  vec3 outColor = vec3(color * max(0.5, shadow));

  fragmentColor = vec4(outColor, 1.0);
}
