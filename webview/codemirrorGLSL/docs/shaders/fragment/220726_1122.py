// [レイトレーシング入門 | ヘロンの数学ちゃんねる](https://heron-no-suugaku.sakura.ne.jp/code/cg-raytracing/)
// 床と天井


#ifdef GL_ES
precision highp float;
#endif

uniform float time;
uniform vec2 resolution;
uniform vec2 mouse;


const float PI = acos(-1.0);

float pixelSize = 2.0;
const float f = 3.0;
const float c = -5.0;


float checker(float x, float z) {
  return clamp(6.0 * sin(x * PI / 4.0) * cos(z * PI / 4.0), 0.0, 1.0);
}

float briFloor(float x, float z) {
  return clamp(140.0 * checker(x, z) / pow(z, 2.0), 0.0, 1.0);
}

float briFilm(float l, float m) {
  vec3 patternVec3;
  vec3 floorVec3 = vec3(l * f / m, f, f / m);
  vec3 ceilingVec3 = vec3(l * c / m, c, c / m);
  
  //#patternVec3 = lessThan(float(floorVec3.z), float(ceilingVec3.z)) ? floorVec3:ceilingVec3;
  
  if (floorVec3.z < ceilingVec3.z) {
    patternVec3 = floorVec3;
  } else {
    patternVec3 = ceilingVec3;
  }
  
  return briFloor(patternVec3.x, patternVec3.z);
  //#return sin(12.0 * l - time) * sin(12.0 * m - time) + 1.0 / 4.0;
}

void main(void) {
  vec2 p = (gl_FragCoord.xy * 2.0 - resolution) / min(resolution.x, resolution.y);
  
  float x = p.x / pixelSize;
  float y = p.y / pixelSize;
  
  vec3 colorOut = vec3(briFilm(x, y));
  
  gl_FragColor = vec4(colorOut, 1.0);
}

