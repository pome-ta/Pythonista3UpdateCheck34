import { Fragmen } from './fragmen.js';
import { wrapDiv, canvasDiv, message, modeSelect, editor } from './setDOMs.js';


let currentMode = Fragmen.MODE_CLASSIC; // 現在の Fragmen モード
let currentSource = ''; // 直近のソースコード

// fragmen.js 用のオプションの雛形
const FRAGMEN_OPTION = {
  target: null,
  eventTarget: null,
  //mouse: true,
  mouse: false,
  resize: true,
  escape: false,
};

const fragmenDefaultSource = Fragmen.DEFAULT_SOURCE;
currentSource = fragmenDefaultSource[currentMode];
// メインとなる fragmen のインスタンス
const option = Object.assign(FRAGMEN_OPTION, {
  target: canvasDiv,
  eventTarget: window,
});
const fragmen = new Fragmen(option);
fragmen.onBuild((status, msg) => {
  message.textContent = msg;
});

fragmen.mode = currentMode;
fragmen.render(currentSource);
editor.textContent = currentSource;

canvasDiv.addEventListener('touchmove', (event) => {
  //event.preventDefault();
});

/**
 * シェーダのソースを更新
 */
function update(source) {
  if (fragmen == null) {
    return;
  }
  fragmen.render(source);
}

// モード変更時の処理
modeSelect.addEventListener(
  'change',
  () => {
    const defaultSourceInPrevMode = fragmenDefaultSource[currentMode];

    const source = editor.textContent;
    currentMode = parseInt(modeSelect.value);
    fragmen.mode = currentMode;

    // 既定のソースと同じならモードに応じた既定のソースに書き換える
    if (source === defaultSourceInPrevMode) {
      const defaultSource = fragmenDefaultSource[currentMode];
      editor.textContent = defaultSource;
      /*
      setTimeout(() => {
        editor.gotoLine(1);
      }, 100);
      */
    } else {
      // ソースを置き換えないとしてもビルドはしなおす
      update(editor.textContent);
    }
  },
  false
);
