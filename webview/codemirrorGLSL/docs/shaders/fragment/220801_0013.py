#version 300 es
precision highp float;

uniform float time;
uniform vec2 resolution;
uniform vec2 mouse;

out vec4 fragmentColor;

/* repetition */

const float PI = acos(-1.0);
const float angle = 60.0;
const float fov = angle * 0.5 * PI / 180.0;

vec3 cameraPos = vec3(0.0, 0.0, 2.0);

const float sphereSize = 1.0;
const vec3 lightDir = vec3(-0.577, 0.577, 0.577);


vec3 trans(vec3 p) {
  return mod(p, 4.0) - 2.0;
}

float distanceFunc(vec3 p) {
  // return length(p) - sphereSize;
  // return length(trans(p)) - sphereSize;
  vec3 q = abs(trans(p));
  return length(max(q - vec3(0.5, 0.5, 0.5), 0.0)) - abs(sin(time));
}

vec3 getNormal(vec3 p) {
  float d = 0.0001;
  return normalize(vec3(
    distanceFunc(p + vec3(  d, 0.0, 0.0)) - distanceFunc(p + vec3( -d, 0.0, 0.0)),
    distanceFunc(p + vec3(0.0,   d, 0.0)) - distanceFunc(p + vec3(0.0,  -d, 0.0)),
    distanceFunc(p + vec3(0.0, 0.0,   d)) - distanceFunc(p + vec3(0.0, 0.0,  -d))
  ));
}


void main(void) {
  vec2 p = (gl_FragCoord.xy * 2.0 - resolution) / min(resolution.x, resolution.y);
  
  /* camera */
  
  /* ray */
  vec3 ray = normalize(vec3(sin(fov) * p.x, sin(fov) * p.y, -cos(fov)));
 
  /* marching loop */
  float distance = 0.0;  // レイとオブジェクト間の最短距離
  float rayAddLength = 0.0;  // レイに継ぎ足す長さ
  vec3 rayPos = cameraPos;  // レイの先端位置
  
  for(int i = 0; i < 128; i++) {
    distance = distanceFunc(rayPos);
    rayAddLength += distance;
    rayPos = cameraPos + ray * rayAddLength;
  }
    
  /* hit check */
  vec4 outColor;
  if(abs(distance) < 0.001) {
    vec3 normal = getNormal(rayPos);
    float diff = clamp(dot(lightDir, normal), 0.1, 1.0);
    outColor = vec4(vec3(normal), 1.0);
  } else {
    outColor = vec4(vec3(0.0), 1.0);
  }
  
  fragmentColor = outColor;
}

