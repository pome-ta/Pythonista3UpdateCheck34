#version 300 es
precision highp float;

uniform float time;
uniform vec2 resolution;
uniform vec2 mouse;

out vec4 fragmentColor;


const float sphereSize = 1.0;

float distanceFunc(vec3 p) {
  return length(p) - sphereSize;
}

void main(void) {
  vec2 p = (gl_FragCoord.xy * 2.0 - resolution) / min(resolution.x, resolution.y);
  
  /* camera */
  vec3 cameraPos = vec3(0.0, 0.0, 2.0);
  vec3 cameraDir = vec3(0.0, 0.0, -1.0);
  vec3 cameraUp  = vec3(0.0, 1.0, 0.0);
  vec3 cameraSide = cross(cameraDir, cameraUp);
  
  float targetDepth = 1.0;
  
  /* ray */
  vec3 ray = normalize(cameraSide * p.x
                     + cameraUp * p.y
                     + cameraDir * targetDepth);
 
  /* marching loop */
  float distance = 0.0;  // レイとオブジェクト間の最短距離
  float rayAddLength = 0.0;  // レイに継ぎ足す長さ
  vec3  rayPos = cameraPos;  // レイの先端位置
  
  for(int i = 0; i < 16; i++) {
    distance = distanceFunc(rayPos);
    rayAddLength += distance;
    rayPos = cameraPos + ray * rayAddLength;
  }
    
  /* hit check */
  vec4 outColor;
  if(abs(distance) < 0.001) {
    outColor = vec4(vec3(1.0), 1.0);
  } else {
    outColor = vec4(vec3(0.0), 1.0);
  }
  
  fragmentColor = outColor;
}

