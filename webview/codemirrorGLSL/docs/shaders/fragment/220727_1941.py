// [8分でわかるレイトレーシング | ヘロンの数学ちゃんねる](https://heron-no-suugaku.sakura.ne.jp/code/cg-raytracing/)
// 2変数関数のグラフを描く
// bit を粗く表現したい

#ifdef GL_ES
precision highp float;
#endif

uniform float time;
uniform vec2 resolution;
uniform vec2 mouse;


const float PI = acos(-1.0);

float pixelSize = 6.0;

float briFilm(float l, float m) {
  //return sin(12.0 * l - time) * sin(12.0 * m - time) + 1.0 / 4.0;
  //return sin(12.0 * l) * sin(12.0 * m) + 1.0 / 4.0;
  return sin(6.0 * l) * sin(6.0 * m) + 1.0 / 4.0;
}


void main(void) {
  vec2 p = (gl_FragCoord.xy * 2.0 - resolution) / min(resolution.x, resolution.y);
  
  float x = p.x;// * 1.0 / pixelSize;
  float y = p.y;// * 1.0 / pixelSize;
  
  vec3 colorOut = vec3(briFilm(x, 1.0));
  
  gl_FragColor = vec4(colorOut, 1.0);
}
