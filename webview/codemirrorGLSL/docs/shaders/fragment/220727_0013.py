#ifdef GL_ES
precision highp float;
#endif

uniform float time;
uniform vec2 resolution;
uniform vec2 mouse;


const float PI = acos(-1.0);

float pixelSize = 2.0;
const float fSize = 3.0;
const float cSize = -5.0;

vec2 solve(float a, float b, float c) {
  float l = (-b + sqrt(pow(b, 2.0) - 4.0 * a * c)) / 2.0 * a;
  float r = (-b - sqrt(pow(b, 2.0) - 4.0 * a * c)) / 2.0 * a;
  return vec2(l, r);
  
}

vec3 vec3Mul(float s, vec3 v) {
  return vec3(s * v.x, s * v.y, s * v.z);
}

float vec3Dot(vec3 v, vec3 w) {
  return v.x * w.x + v.y * w.y + v.z * w.z;
}

float norm(vec3 v) {
  return sqrt(pow(v.x, 2.0) + pow(v.y, 2.0) + pow(v.z, 2.0));
}

vec3 vec3Normalize(vec3 v) {
  return vec3Mul(1.0 / norm(v), v);
}



float checker(float x, float z) {
  return clamp(6.0 * sin(x * PI / 4.0) * cos(z * PI / 4.0), 0.0, 1.0);
}

float briFloor(float x, float z) {
  if (abs(z) > 60.0) {
    return 0.0;
  }
  return clamp(140.0 * checker(x, z) / pow(z, 2.0), 0.0, 1.0);
}

float briFilm(float l, float m) {
  vec3 w = vec3Normalize(vec3(l, m, 1.0));
  
  // createCanvas(640,640);
  vec3 c = vec3(320.0 / 60.0 - 5.5, 1.0, -320.0 / 60.0 + 18.0);
  float r = 2.0;
  
  vec2 solveVec2 = solve(vec3Dot(w, w), 2.0 * vec3Dot(w, vec3Mul(-1.0, c)), vec3Dot(c, c) - pow(r, 2.0));

  float s = min(solveVec2.x, solveVec2.y);
  vec3 sw = vec3Mul(s, w);

  if (bool(s)) {
    vec3 floorVec3 = vec3(l * fSize / m, fSize, fSize / m);
    vec3 ceilingVec3 = vec3(l * cSize / m, cSize, cSize / m);
    
    if (floorVec3.z < ceilingVec3.z) {
      return briFloor(floorVec3.x, floorVec3.z);
    } else {
      return briFloor(ceilingVec3.x, ceilingVec3.z);
    }
  }

  return s;
}

void main(void) {
  vec2 p = (gl_FragCoord.xy * 2.0 - resolution) / min(resolution.x, resolution.y);
  
  float x = p.x / pixelSize;
  float y = p.y / pixelSize;
  
  vec3 colorOut = vec3(briFilm(x, y));
  
  gl_FragColor = vec4(colorOut, 1.0);
}
