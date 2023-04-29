//function createElements(tags) {
//  return tags.map(tag => document.createElement(tag))
//}

const createElements = (tags) => tags.map((tag) => document.createElement(tag));

const tagArray = ['main', 'div', 'div', 'select', 'div'];
const modeOptions = [
  'classic',
  'geek',
  'geeker',
  'geekest',
  'classic (300 es)',
  'geek (300 es)',
  'geeker (300 es)',
  'geekest (300 es)',
  'classic (MRT)',
  'geek (MRT)',
  'geeker (MRT)',
  'geekest (MRT)',
];

const [wrapDiv, canvasDiv, message, modeSelect, editor] =
  createElements(tagArray);

modeSelect.style.width = '100%';
modeSelect.style.height = '2rem';
modeOptions.forEach((option, index) => {
  const optionElement = document.createElement('option');
  optionElement.value = index;
  optionElement.text = option;
  if ([0, 4].includes(index)) {
    modeSelect.appendChild(optionElement);
  }
});

editor.style.fontFamily = 'monospace';
editor.style.fontSize = '0.8rem';

document.body.appendChild(wrapDiv);
wrapDiv.appendChild(modeSelect);
wrapDiv.appendChild(message);
wrapDiv.appendChild(editor);
wrapDiv.appendChild(canvasDiv);

//wrapDiv.style.display = 'grid';
//wrapDiv.gridTemplateRows = 'auto 1fr';
message.style.height = '2rem';
message.style.fontFamily = 'monospace';
message.textContent = ' ● ready';

wrapDiv.style.height = '100%';
canvasDiv.style.overflow = 'hidden';
canvasDiv.style.height = '100%';

// todo: setting fragmen glCanvas size
const { width, height } = wrapDiv.getBoundingClientRect();
canvasDiv.width = width;
canvasDiv.height = height;

export { wrapDiv, canvasDiv, message, modeSelect, editor };
