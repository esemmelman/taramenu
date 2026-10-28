"""Customize the Aria menu and reading copies for Tara; cache the Vaera text."""
from pathlib import Path
import html
import json
import re
import urllib.request
import urllib.parse

ROOT = Path(__file__).resolve().parents[1]
def read(path): return (ROOT / path).read_text(encoding='utf-8')
def write(path, text): (ROOT / path).write_text(text, encoding='utf-8')
def plain(text):
    text = re.sub(r'<sup\b[^>]*>.*?</sup>', '', text, flags=re.S)
    text = re.sub(r'<i\b[^>]*class="footnote"[^>]*>.*?</i>', '', text, flags=re.S)
    return html.unescape(re.sub('<[^>]+>', '', text)).strip()

chapters = []
for number in range(6, 10):
    version = urllib.parse.quote('Tanakh: The Holy Scriptures, published by JPS', safe='')
    url = f'https://www.sefaria.org/api/texts/Exodus.{number}/en/{version}?context=0'
    with urllib.request.urlopen(url) as response:
        source = json.load(response)
    chapters.append({'chapter': number, 'verses': [
        {'verse': i + 1, 'text': plain(text)} for i, text in enumerate(source['text'])
        if (number != 6 or i >= 1) and (number != 9 or i < 35)
    ]})
    if number == 8:
        hebrew = [plain(text) for text in source['he'][:15]]

# Transcription checked against the supplied photographs, Exodus 8:1–15.
english8 = [
    'And the LORD said to Moses, “Say to Aaron: Hold out your arm with the rod over the rivers, the canals, and the ponds, and bring up the frogs on the land of Egypt.”',
    'Aaron held out his arm over the waters of Egypt, and the frogs came up and covered the land of Egypt.',
    'But the magicians did the same with their spells, and brought frogs upon the land of Egypt.',
    'Then Pharaoh summoned Moses and Aaron and said, “Plead with the LORD to remove the frogs from me and my people, and I will let the people go to sacrifice to the LORD.”',
    'And Moses said to Pharaoh, “You may have this triumph over me: for what time shall I plead in behalf of you and of your courtiers and your people, that the frogs be cut off from you and your houses, to remain only in the Nile?”',
    '“For tomorrow,” he replied. And [Moses] said, “As you say—that you may know that there is none like the LORD our God;',
    'the frogs shall retreat from you and your courtiers and your people; they shall remain only in the Nile.”',
    'Then Moses and Aaron left Pharaoh’s presence, and Moses cried out to the LORD in the matter of the frogs which He had inflicted upon Pharaoh.',
    'And the LORD did as Moses asked; the frogs died out in the houses, the courtyards, and the fields.',
    'And they piled them up in heaps, till the land stank.',
    'But when Pharaoh saw that there was relief, he became stubborn and would not heed them, as the LORD had spoken.',
    'Then the LORD said to Moses, “Say to Aaron: Hold out your rod and strike the dust of the earth, and it shall turn to lice throughout the land of Egypt.”',
    'And they did so. Aaron held out his arm with the rod and struck the dust of the earth, and vermin came upon man and beast; all the dust of the earth turned to lice throughout the land of Egypt.',
    'The magicians did the like with their spells to produce lice, but they could not. The vermin remained upon man and beast;',
    'and the magicians said to Pharaoh, “This is the finger of God!” But Pharaoh’s heart stiffened and he would not heed them, as the LORD had spoken.'
]
for row, text in zip(chapters[2]['verses'], english8): row['text'] = text
chapters[0]['verses'][4]['text'] = chapters[0]['verses'][4]['text'].replace('labors', 'burdens')
write('data/vaera.json', json.dumps(chapters, ensure_ascii=False, indent=2) + '\n')

s = read('../ariamenu/index.html')
s = s.replace('Aria Menu', 'Tara Menu').replace('Revision 1.06', 'Revision 1.0.0')
s = s.replace('https://esemmelman.github.io/bmtimelinear/', 'timeline/')
s = s.replace('https://esemmelman.github.io/aria-torah/', 'torah/')
s = s.replace('https://esemmelman.github.io/ariahaftorah/', 'haftorah/')
s = re.sub(r'^.*<option[^>]*>Zoom Link</option>\n', '', s, flags=re.M)
s = re.sub(r'      if \(selected.text === "Zoom Link"\) \{.*?\n      \}\n', '', s, flags=re.S)
s = s.replace('    let selectedPageIndex = pageList.selectedIndex;\n', '').replace('      selectedPageIndex = pageList.selectedIndex;\n', '')
s = s.replace('Revision 1.0.0', 'Revision 1.0.1')
s = s.replace('ariamenu_homework_documents', 'taramenu_homework_documents')
s = s.replace("B'shalach", 'Vaera').replace('Exodus 13:17–17:16', 'Exodus 6:2–9:35')
s = s.replace('https://www.sefaria.org/Exodus.13.17-17.16?lang=en', 'https://www.sefaria.org/Exodus.6.2-9.35?lang=en')
s = s.replace('Revised JPS, 2023 via Sefaria', 'JPS · English text from the supplied photographs').replace('          · CC BY-NC', '          · Missing text supplemented from Sefaria')
s = re.sub(r'    const presentationId = .*?;\n', '', s)
slides = [{'id':f'page-{n}', 'page':str(n), 'title':f'Page {n}'} for n in range(1,14)]
s = re.sub(r'    const serviceSlides = \[.*?\n    \];', '    const serviceSlides = ' + json.dumps(slides, indent=2) + ';', s, flags=re.S)
s = re.sub(r'    const recordableSlideIds = new Set\(\[.*?\n    \]\);', '    const recordableSlideIds = new Set(serviceSlides.map(slide => slide.id));', s, flags=re.S)
s = re.sub(r'    function serviceUrl\(slideId\) \{.*?\n    \}', '', s, flags=re.S)
start = s.index('        const chapterNumbers =')
end = s.index('        torahLoaded = true;', start)
s = s[:start] + '''        const response = await fetch('data/vaera.json');
        if (!response.ok) throw new Error('Unable to load Vaera');
        const chapters = await response.json();
        torahText.replaceChildren();
        chapters.forEach(({ chapter, verses }) => {
          const heading = document.createElement('h2');
          heading.className = 'torah-chapter';
          heading.textContent = `Exodus ${chapter}`;
          torahText.append(heading);
          verses.forEach(({ verse, text }) => {
            const paragraph = document.createElement('p');
            paragraph.className = 'torah-verse';
            paragraph.dataset.chapter = chapter;
            paragraph.dataset.verse = verse;
            if (chapter === 8 && verse >= 1 && verse <= 15) paragraph.classList.add('highlighted');
            const number = document.createElement('span');
            number.className = 'verse-number';
            number.textContent = verse;
            paragraph.append(number, document.createTextNode(text));
            torahText.append(paragraph);
          });
        });
''' + s[end:]
s = s.replace('?v=1.06', '?v=1.0.0')
# Keep the full PDF accessible from the service navigation.
s = s.replace('<h2>Service slides</h2>', '<h2>Service pages</h2><p><a href="service.pdf" target="_blank" rel="noopener">Open service PDF</a></p>')
write('index.html', s)

s = read('../ariamenu/service-recordings.js')
s = re.sub(r'  const exampleIds = \{.*?\n  \};', '  const exampleIds = {};', s, flags=re.S)
s = s.replace('bradymenu_service_recordings_v1', 'taramenu_service_recordings_v1').replace("name: 'Aria'", "name: 'Tara'")
write('service-recordings.js', s)

for file in ['app.js', 'index.html', 'recordings.js', 'recording.html', 'recording-player.js']:
    s = read('../aria-torah/' + file)
    s = s.replace('aria_torah_highlight_groups_v1', 'tara_torah_highlight_groups_v1')
    s = s.replace('aria_torah_group_recordings_v1', 'tara_torah_group_recordings_v1')
    s = s.replace('aria-torah-group-recordings-v1', 'tara-torah-group-recordings-v1')
    s = s.replace('brady_torah_passage_recordings_v1', 'tara_torah_passage_recordings_v1')
    s = s.replace('aria-torah-highlights-v1', 'tara-torah-highlights-v1')
    s = s.replace('exodus-14-15-30', 'exodus-8-1-15').replace('Aria', 'Tara')
    s = s.replace('Exodus.14.15-31', 'Exodus.8.1-15').replace('Exodus.14.${number}', 'Exodus.8.${number}')
    s = s.replace('Exodus 14:15–31', 'Exodus 8:1–15').replace('Chapter 14, verses 15–31', 'Chapter 8, verses 1–15')
    s = s.replace('Exodus chapter 14, verses 15 through 31', 'Exodus chapter 8, verses 1 through 15')
    s = s.replace('const number = index + 15;', 'const number = index + 1;')
    s = s.replace('Exodus(?:\\\\.| )14', 'Exodus(?:\\\\.| )8')
    if file == 'app.js':
        s = re.sub(r'const FALLBACK_VERSES = \[.*?\n\];', 'const FALLBACK_VERSES = ' + json.dumps(hebrew, ensure_ascii=False, indent=2) + ';', s, flags=re.S)
        s = re.sub(r'const ALIYAH_HEADINGS = new Map\(\[.*?\n\]\);', "const ALIYAH_HEADINGS = new Map([[1, 'Aliyah 1 · 1–3'], [4, 'Aliyah 2 · 4–5'], [6, 'Aliyah 3 · 6–8'], [9, 'Aliyah 4 · 9–11'], [12, 'Aliyah 5 · 12–13'], [14, 'Aliyah 6 · 14–15']]);", s, flags=re.S)
        # The cached pointed Hebrew keeps script and trope working without a network request.
        s = s.replace("fetch('https://www.sefaria.org/api/texts/Exodus.8.1-15?context=0')", "fetch('verses.json')")
    write('torah/' + file, s)
write('torah/verses.json', json.dumps({'he': hebrew}, ensure_ascii=False, indent=2) + '\n')

s = read('../bmtimelinear/src/App.tsx')
s = s.replace('mitzvah_status_', 'tara_mitzvah_status_').replace("'mitzvah-status-live'", "'tara-mitzvah-status-live'")
s = s.replace('new Date(2027, 0, 27)', 'new Date(2027, 0, 5)').replace("'08-31'", "'10-26'").replace('until 1/27', 'until 1/5')
s = s.replace('<h2>Progress sheet</h2>', '<h2>Tara’s progress sheet</h2><p>October 26, 2026 – January 5, 2027</p>')
write('timeline-src/src/App.tsx', s)
s = read('../bmtimelinear/vite.config.ts')
s = s.replace("base: process.env.GITHUB_ACTIONS ? '/bmtimelinear/' : '/',", "base: './',\n  build: { outDir: '../timeline', emptyOutDir: true },")
write('timeline-src/vite.config.ts', s)

print('Customized Tara menu, six aliyot, full Vaera text, and timeline source.')
