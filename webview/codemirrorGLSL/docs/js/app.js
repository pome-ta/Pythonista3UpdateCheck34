'use strict';

let canvasDiv, cxtCanvas;
let gl;
let uniLocation = new Array();

let mouseX = 0.5;
let mouseY = 0.5;
let canvasW, canvasH;

let isPlaying = 1;
const switchPlayPause = ['Play', 'Pause'];
let playPauseButton;

let time = 0.0;
const FPS = 120;
const frameTime = 1 / FPS;
let prevTimestamp = 0;

const vs = './shaders/vertex/vertexMain.js';
const fs = './shaders/fragment/fragmentMain.js';

const vertexPrimitive = await fetchShader(vs);
const fragmentPrimitive = await fetchShader(fs);

async function fetchShader(path) {
  const res = await fetch(path);
  const shaderText = await res.text();
  return shaderText;
}

function createCanvas() {
  //document.body.style.backgroundColor = 'dimgray';
  document.body.style.backgroundColor = '#232323';
  canvasDiv = document.createElement('div');
  cxtCanvas = document.createElement('canvas');
  canvasDiv.appendChild(cxtCanvas);
  document.body.appendChild(canvasDiv);
  canvasDiv.style.width = '100%';
  //canvasDiv.style.height = '100%';
  cxtCanvas.style.width = '100%';
  //cxtCanvas.style.height = '100%';
}

function createPlayPuseButton() {
  playPauseButton = document.createElement('button');
  playPauseButton.type = 'button';
  playPauseButton.style.width = '100%';
  playPauseButton.style.height = '4rem';
  playPauseButton.textContent = switchPlayPause[isPlaying];
  const playPauseSection = document.createElement('section');
  playPauseSection.style.width = '100%';
  playPauseSection.appendChild(playPauseButton);
  //document.body.appendChild(playPauseSection);
}

function initCanvasSize() {
  // const oneSide = Math.min(canvasDiv.clientWidth, canvasDiv.clientHeight);
  const oneSide = canvasDiv.clientWidth;
  cxtCanvas.width = oneSide;
  cxtCanvas.height = oneSide;
  canvasW = cxtCanvas.width;
  canvasH = cxtCanvas.height;
}

function initShader() {
  gl = cxtCanvas.getContext('webgl2');
  //gl = cxtCanvas.getContext('webgl');
  const prg = create_program(
    create_shader('vs', vertexPrimitive),
    create_shader('fs', fragmentPrimitive)
  );
  uniLocation[0] = gl.getUniformLocation(prg, 'time');
  uniLocation[1] = gl.getUniformLocation(prg, 'mouse');
  uniLocation[2] = gl.getUniformLocation(prg, 'resolution');

  const position = new Float32Array([
    -1.0, 1.0, 0.0, 1.0, 1.0, 0.0, -1.0, -1.0, 0.0, 1.0, -1.0, 0.0,
  ]);
  const index = new Uint16Array([0, 2, 1, 1, 2, 3]);

  const vPosition = create_vbo(position);
  const vIndex = create_ibo(index);
  const vAttLocation = gl.getAttribLocation(prg, 'vertexPosition');

  const VERTEX_SIZE = 3; // vec3

  gl.viewport(0, 0, canvasW, canvasH);

  gl.bindBuffer(gl.ARRAY_BUFFER, vPosition);
  gl.enableVertexAttribArray(vAttLocation);
  gl.vertexAttribPointer(vAttLocation, VERTEX_SIZE, gl.FLOAT, false, 0, 0);
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, vIndex);

  gl.clearColor(0.0, 0.0, 0.0, 1.0);
}

// シェーダを生成する関数
function create_shader(type, text) {
  let shader;
  // scriptタグのtype属性をチェック
  switch (type) {
    // 頂点シェーダの場合
    case 'vs':
      shader = gl.createShader(gl.VERTEX_SHADER);
      break;
    // フラグメントシェーダの場合
    case 'fs':
      shader = gl.createShader(gl.FRAGMENT_SHADER);
      break;
    default:
      return;
  }

  // 生成されたシェーダにソースを割り当てる
  gl.shaderSource(shader, text);
  // シェーダをコンパイルする
  gl.compileShader(shader);
  // シェーダが正しくコンパイルされたかチェック
  if (gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    // 成功していたらシェーダを返して終了
    return shader;
  } else {
    // 失敗していたらエラーログをアラートしコンソールに出力
    // alert(gl.getShaderInfoLog(shader));
    console.log(gl.getShaderInfoLog(shader));
  }
}

// プログラムオブジェクトを生成しシェーダをリンクする関数
function create_program(vs, fs) {
  // プログラムオブジェクトの生成
  const program = gl.createProgram();
  if (!program) {
    return null;
  }
  // プログラムオブジェクトにシェーダを割り当てる
  gl.attachShader(program, vs);
  gl.deleteShader(vs);
  gl.attachShader(program, fs);
  gl.deleteShader(fs);
  // シェーダをリンク
  gl.linkProgram(program);
  // シェーダのリンクが正しく行なわれたかチェック
  if (gl.getProgramParameter(program, gl.LINK_STATUS)) {
    // 成功していたらプログラムオブジェクトを有効にする
    gl.useProgram(program);
    // プログラムオブジェクトを返して終了
    return program;
  } else {
    // 失敗していたら NULL を返す
    return null;
  }
}

// VBOを生成する関数
function create_vbo(data) {
  // バッファオブジェクトの生成
  const vbo = gl.createBuffer();
  // バッファをバインドする
  gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
  // バッファにデータをセット
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(data), gl.STATIC_DRAW);
  gl.bufferData(gl.ARRAY_BUFFER, data, gl.STATIC_DRAW);
  // バッファのバインドを無効化
  gl.bindBuffer(gl.ARRAY_BUFFER, null);
  // 生成した VBO を返して終了
  return vbo;
}

// IBOを生成する関数
function create_ibo(data) {
  // バッファオブジェクトの生成
  const ibo = gl.createBuffer();
  // バッファをバインドする
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ibo);
  // バッファにデータをセット
  // gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Int16Array(data), gl.STATIC_DRAW);
  gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, data, gl.STATIC_DRAW);
  // バッファのバインドを無効化
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, null);
  // 生成したIBOを返して終了
  return ibo;
}

function glRender(time) {
  // カラーバッファをクリア
  gl.clear(gl.COLOR_BUFFER_BIT);
  // uniform 関連
  gl.uniform1f(uniLocation[0], time);
  gl.uniform2fv(uniLocation[1], [mouseX, mouseY]);
  gl.uniform2fv(uniLocation[2], [canvasW, canvasH]);
  // 描画
  gl.drawElements(gl.TRIANGLES, 6, gl.UNSIGNED_SHORT, 0);
  gl.flush();
}

function loop(timestamp) {
  const elapsed = (timestamp - prevTimestamp) / 1000;
  if (elapsed <= frameTime) {
    requestAnimationFrame(loop);
    return;
  }
  prevTimestamp = timestamp;

  if (!isPlaying) {
    requestAnimationFrame(loop);
    return;
  }

  time += frameTime;
  glRender(time);
  // 再帰
  requestAnimationFrame(loop);
}

createCanvas();
createPlayPuseButton();
initCanvasSize();
initShader();
glRender(time);
loop();

playPauseButton.addEventListener('click', checkChange);

function checkChange(event) {
  isPlaying = isPlaying ^ 1;
  playPauseButton.textContent = switchPlayPause[isPlaying];
}

cxtCanvas.addEventListener('touchmove', (event) => {
  event.preventDefault();
});
cxtCanvas.addEventListener('pointermove', moveInteractive);

function moveInteractive(event) {
  event.preventDefault();
  mouseX = event.offsetX / canvasW;
  mouseY = event.offsetY / canvasH;
}
