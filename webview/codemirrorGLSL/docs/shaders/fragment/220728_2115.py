// [8分でわかるレイトレーシング | ヘロンの数学ちゃんねる](https://heron-no-suugaku.sakura.ne.jp/code/cg-raytracing/)

#ifdef GL_ES
precision highp float;
#endif

uniform float time;
uniform vec2 resolution;
uniform vec2 mouse;

const float PI = acos(-1.0);

const float pixelSize = 0.1;
const float upToFloor = 3.0;
const float upToCeiling = -5.0;

bool isNan(float val) { return ( val < 0.0 || 0.0 < val || val == 0.0 ) ? false : true;}

vec2 solve(float a, float b, float c) {
  float l = (-b + sqrt(pow(b, 2.0) - 4.0 * a * c)) / 2.0 * a;
  float r = (-b - sqrt(pow(b, 2.0) - 4.0 * a * c)) / 2.0 * a;
  return vec2(l, r);
}

vec3 vec3Mul(float s, vec3 v) { return vec3(s * v.x, s * v.y, s * v.z); }

vec3 vec3Add(vec3 v, vec3 w) { return vec3(v.x + w.x, v.y + w.y, v.z + v.z); }

vec3 vec3Sub(vec3 v, vec3 w) { return vec3Add(v, vec3Mul(-1.0, w)); }

float vec3Dot(vec3 v, vec3 w) { return v.x * w.x + v.y * w.y + v.z * w.z; }

float norm(vec3 v) { return sqrt(pow(v.x, 2.0) + pow(v.y, 2.0) + pow(v.z, 2.0)); }

vec3 vec3Normalize(vec3 v) { return vec3Mul(1.0 / norm(v), v); }


float checker(float x, float z) {
  return clamp(6.0 * sin(x * PI / 4.0 - time) * cos(z * PI / 4.0 - time), 0.0, 1.0);
  // return clamp(8.0 * sin(x * PI / 4.0) * cos(z * PI / 4.0), 0.0, 1.0);
}

float briFloor(float x, float z) {
  if (abs(z) > 60.0) {
    return 0.0;
  }
  return clamp(140.0 * checker(x, z) / pow(z, 2.0), 0.0, 1.0);
  // return clamp(140.0 * checker(x, z), 0.0, 1.0);
}

float briFilm(float l, float m) {
  vec3 w = vec3Normalize(vec3(l, m, 1.0));
  
  // createCanvas(640,640);
  // 213
  vec3 c = vec3(320.0 / 60.0 - 5.5, 1.0, -320.0 / 60.0 + 18.0);
  float r = 2.0;
  
  vec2 solveVec2 = solve(vec3Dot(w, w), 2.0 * vec3Dot(w, vec3Mul(-1.0, c)), vec3Dot(c, c) - pow(r, 2.0));

  float s = min(solveVec2.x, solveVec2.y);
  vec3 sw = vec3Mul(s, w);
  
  if (isNan(s) || !bool(sign(s))) {
    vec3 floorVec3 = vec3(l * upToFloor / m, upToFloor, upToFloor / m);
    vec3 ceilingVec3 = vec3(l * upToCeiling / m, upToCeiling, upToCeiling / m);
    
    if (floorVec3.z < ceilingVec3.z) {
      return briFloor(floorVec3.x, floorVec3.z);
    } else {
      return briFloor(ceilingVec3.x, ceilingVec3.z);
    }
  }
  
  vec3 n = vec3Normalize(vec3Sub(sw, c));
  vec3 b = vec3Add(sw, vec3Mul(vec3Dot(vec3Mul(-2.0, sw), n), n));
  
  vec3 _nA = vec3(0.0, 1.0, 0.0);
  vec3 _nB = vec3(0.0, -1.0, 0.0);
  float indexA = (upToFloor - vec3Dot(_nA, sw)) / vec3Dot(_nA, b);
  float indexB = (abs(upToCeiling) - vec3Dot(_nB, sw)) / vec3Dot(_nB, b);
  
  float u = indexA < indexB ? indexA : indexB;
  vec3 v = vec3Add(sw, vec3Mul(u, b));
  
  return briFloor(v.x, v.z);
}


void main(void) {
  vec2 p = (gl_FragCoord.xy * 2.0 - resolution) / min(resolution.x, resolution.y);
  
  float ps = 100.0 / pixelSize;
  p *= ps;
  vec2 id = floor(p);
  float x = id.x * 1.0 / ps;
  float y = id.y * 1.0 / ps;

  vec3 colorOut = vec3(briFilm(x, y));
  gl_FragColor = vec4(colorOut, 1.0);
}


