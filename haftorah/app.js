const passage = document.querySelector('#passage');
const tropeButton = document.querySelector('#trope-toggle');
const scriptButton = document.querySelector('#script-toggle');
let verses = [];
let showTrope = true;
let scriptMode = false;

function render() {
  passage.replaceChildren();
  document.body.classList.toggle('script-mode', scriptMode);
  tropeButton.classList.toggle('active', showTrope);
  tropeButton.setAttribute('aria-pressed', String(showTrope));
  scriptButton.classList.toggle('active', scriptMode);
  scriptButton.setAttribute('aria-pressed', String(scriptMode));
  let currentChapter;
  verses.forEach(({ chapter, verse, he }) => {
    if (chapter !== currentChapter) {
      const heading = document.createElement('h2');
      heading.className = 'aliyah-heading';
      heading.textContent = `Ezekiel ${chapter}`;
      passage.append(heading);
      currentChapter = chapter;
    }
    const row = document.createElement('div');
    row.className = 'verse-row';
    row.dir = 'rtl';
    row.dataset.reference = `${chapter}:${verse}`;
    const number = document.createElement('span');
    number.className = 'verse-number';
    number.textContent = verse;
    const text = document.createElement('span');
    text.className = 'verse-line';
    text.lang = 'he';
    text.textContent = scriptMode
      ? he.normalize('NFD').replace(/[\u0591-\u05BD\u05BF-\u05C7]/g, '')
      : showTrope ? he : he.replace(/[\u0591-\u05AF]/g, '');
    row.append(number, text);
    passage.append(row);
  });
}

tropeButton.addEventListener('click', () => { showTrope = !showTrope; render(); });
scriptButton.addEventListener('click', () => { scriptMode = !scriptMode; render(); });
fetch('verses.json').then(response => {
  if (!response.ok) throw new Error('Unable to load Haftorah');
  return response.json();
}).then(data => { verses = data; render(); }).catch(() => {
  document.querySelector('#status').textContent = 'The Haftorah could not be loaded. Please refresh to try again.';
});
