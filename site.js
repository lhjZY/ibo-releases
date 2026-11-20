// Language: the visitor's last choice, else Chinese for a Chinese browser and English otherwise.
// System: Windows visitors see Windows shortcuts, and every visitor's own installer comes first
// with the filled button. Without a guess (Linux, phones), the rows keep their order, none filled.
(function () {
  'use strict';

  const root = document.documentElement;
  const stored = localStorage.getItem('ibo-language');
  const setLanguage = language => {
    root.dataset.lang = language;
    root.lang = language === 'zh' ? 'zh-CN' : 'en';
  };
  setLanguage(stored || (navigator.language.toLowerCase().startsWith('zh') ? 'zh' : 'en'));

  document.getElementById('language').addEventListener('click', () => {
    const next = root.dataset.lang === 'zh' ? 'en' : 'zh';
    localStorage.setItem('ibo-language', next);
    setLanguage(next);
  });

  const platform = (navigator.userAgentData && navigator.userAgentData.platform) || navigator.platform || navigator.userAgent;
  const windows = /win/i.test(platform);
  const mac = /mac/i.test(platform) && navigator.maxTouchPoints < 2;
  root.dataset.os = windows ? 'windows' : 'mac';

  const installers = document.querySelector('.installers');
  if (!installers) return;
  const choose = name => {
    const row = installers.querySelector(`[data-for="${name}"]`);
    if (!row) return;
    installers.querySelectorAll('.installer').forEach(other => other.classList.remove('primary'));
    row.classList.add('primary');
    installers.prepend(row);
  };
  if (mac) choose('mac');
  if (windows) {
    choose('windows');
    // Only Chromium browsers tell the processor; an ARM PC on another browser keeps x64 first.
    if (navigator.userAgentData && navigator.userAgentData.getHighEntropyValues) {
      navigator.userAgentData.getHighEntropyValues(['architecture'])
        .then(values => { if (values.architecture === 'arm') choose('windows-arm'); })
        .catch(() => {});
    }
  }
})();
