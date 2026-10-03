const languageButtons = [...document.querySelectorAll('[data-language]')];
languageButtons.forEach(button => button.addEventListener('click', () => {
  languageButtons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  const script = document.getElementById('selected-script');
  script.textContent = button.dataset.script;
  script.lang = button.dataset.lang;
  document.getElementById('selected-language').textContent = `Beautiful input, in ${button.dataset.language}.`;
  document.getElementById('language-description').textContent = button.dataset.description;
}));

const navigation = document.querySelector('.navigation');
const mobile = matchMedia('(max-width: 800px)');
if (navigation) {
  navigation.open = !mobile.matches;
  mobile.addEventListener('change', () => navigation.open = !mobile.matches);
}
navigation?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  if (matchMedia('(max-width: 800px)').matches) navigation.open = false;
}));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && navigation?.open) {
    navigation.open = false;
    navigation.querySelector('summary').focus();
  }
});

const replay = document.getElementById('replay');
if (replay) {
  const tiles = [...document.querySelectorAll('.demo-tiles span')];
  const progress = [...document.querySelectorAll('.demo-progress span')];
  const state = document.getElementById('demo-state');
  const confetti = document.querySelector('.confetti');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let generation = 0;
  const pause = milliseconds => new Promise(resolve => setTimeout(resolve, milliseconds));
  const reset = () => {
    tiles.forEach(tile => { tile.textContent = ''; tile.className = ''; });
    progress.forEach(step => step.className = '');
    confetti.replaceChildren();
  };
  replay.addEventListener('click', async () => {
    const run = ++generation;
    reset();
    replay.disabled = true;
    const show = async (label, action) => {
      if (run !== generation) return false;
      state.textContent = label;
      action();
      if (!reduced.matches) await pause(650);
      return run === generation;
    };
    try {
      if (!await show('Typing, one unit at a time.', () => tiles.forEach(tile => tile.textContent = '●'))) return;
      if (!await show('Select the tile you want to change.', () => tiles[2].className = 'selected')) return;
      if (!await show('Replace it. Keep your flow.', () => tiles[2].textContent = '◆')) return;
      if (!await show('A guess brings a little clarity.', () => tiles.forEach((tile, index) => {
        tile.className = index < 2 ? 'correct' : index === 2 ? 'elsewhere' : 'absent';
        tile.textContent = index < 2 ? '✓' : index === 2 ? '↔' : '−';
      }))) return;
      if (!await show('A clue helps you move forward.', () => progress[0].className = 'done')) return;
      if (!await show('That satisfying moment: solved.', () => tiles.forEach(tile => { tile.className = 'correct'; tile.textContent = '✓'; }))) return;
      if (!await show('A small celebration, then back to calm.', () => {
        if (reduced.matches) return;
        for (let index = 0; index < 18; index++) {
          const particle = document.createElement('i');
          const angle = index * Math.PI * 2 / 18;
          particle.style.setProperty('--dx', `${Math.cos(angle) * 150}px`);
          particle.style.setProperty('--dy', `${Math.sin(angle) * 115}px`);
          particle.style.setProperty('--spin', `${index * 47}deg`);
          confetti.append(particle);
        }
      })) return;
      if (!await show('One more day of wordplay.', () => progress[1].className = 'done')) return;
      await show('One more step in your Journey.', () => progress.forEach(step => step.className = 'done'));
    } finally {
      confetti.replaceChildren();
      replay.disabled = false;
      replay.firstChild.textContent = 'Replay the interaction ';
    }
  });
}
