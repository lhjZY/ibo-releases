"""Screenshots of Ibo's real pages (popup and Learn window) against fake bridges, both languages."""
import json, pathlib, re, subprocess, sys, tempfile
web = pathlib.Path('/Users/allen/Documents/ravens-space/project/app/ibo/app/app/web')
out = pathlib.Path(sys.argv[1]); out.mkdir(exist_ok=True)
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
J = json.dumps

def bridge(locale, extra_cases, state):
    return '''window.handlers={};window.listeners={};
window.mygo={on(n,f){(listeners[n]||=[]).push(f);handlers[n]=(...a)=>listeners[n].forEach(g=>g(...a));},call:async(n,...a)=>{
 switch(n){ case 'Workspace.State':return %s; case 'Learn.State':return {writable:true,status:'ready',count:48}; %s }
 return null;}};''' % (J({**state, 'locale': locale}), extra_cases)

def tool(locale, mode, text, reply, wait='300'):
    b = bridge(locale, "case 'Workspace.Run':return %s; case 'Review.Mode':return 'tool';" % J(reply),
               {'engine': reply['engine'], 'aiProvider': 'deepseek', 'split': False, 'pinned': False, 'limit': 4000})
    run = "window.addEventListener('load',async()=>{await new Promise(r=>setTimeout(r,50));handlers['workspace:source'](%s);setTimeout(()=>document.body.dataset.h=Math.ceil(document.body.getBoundingClientRect().height),%s);});" % (J({'mode': mode, 'text': text, 'origin': 7, 'translate': True}), wait)
    return 'index.html', b, run, 560

def review(locale, zh):
    names = {'translation': '中文' if zh else 'Chinese', 'dictation': '听写' if zh else 'Dictation', 'correction': '改错' if zh else 'Correction', 'building': '连词成句' if zh else 'Sentence building'}
    exercises = [{'mode': k, 'title': v, 'selected': k == 'translation'} for k, v in names.items()]
    session = {'run': 1, 'position': 3, 'total': 12, 'phase': 'answered', 'paused': False, 'stepIndex': 0, 'stepCount': 1,
      'prompt': '学习一门语言最好的办法，是每天都用它。', 'entryID': 'e1', 'text': 'The best way to learn a language is to use it every day.',
      'note': '读到的一篇博客' if zh else 'From a blog post', 'groupName': '默认' if zh else 'Default',
      'slots': [{'text': w, 'index': i, **({'trailing': '.'} if i == 11 else {})} for i, w in enumerate('The best way to learn a language is to use it every day'.split())],
      'confirmed': 12, 'words': 12, 'typed': '', 'mistakes': 0, 'grade': 'easy', 'gradeText': 'Perfect', 'answer': 'The best way to learn a language is to use it every day.',
      'structure': {'chunks': [
        {'role': 'subject', 'text': 'The best way to learn a language', 'meaning': '学习一门语言最好的办法' if zh else 'the best way to learn a language', 'explanation': '', 'words': [{'text': 'way', 'ipa': 'weɪ', 'gloss': '方法' if zh else 'way'}, {'text': 'learn', 'ipa': 'lɜːn', 'gloss': '学习' if zh else 'learn'}]},
        {'role': 'predicate', 'text': 'is', 'meaning': '是' if zh else 'is', 'explanation': '', 'words': [{'text': 'is', 'ipa': 'ɪz', 'gloss': '是' if zh else 'is'}]},
        {'role': 'complement', 'text': 'to use it', 'meaning': '使用它' if zh else 'to use it', 'explanation': '', 'words': [{'text': 'use', 'ipa': 'juːz', 'gloss': '使用' if zh else 'use'}]},
        {'role': 'adverbial', 'text': 'every day', 'meaning': '每天' if zh else 'every day', 'explanation': '', 'words': [{'text': 'every', 'ipa': 'ˈevri', 'gloss': '每个' if zh else 'every'}, {'text': 'day', 'ipa': 'deɪ', 'gloss': '天' if zh else 'day'}]}]}}
    view = {'exercises': exercises, 'exercise': 'translation', 'exerciseName': names['translation'], 'scope': 'all', 'scopeName': '全部' if zh else 'All',
            'groups': [{'id': '', 'name': '默认' if zh else 'Default', 'count': 48}], 'allCount': 48, 'state': 'reviewing', 'session': session, 'showNote': True, 'speakAfterAnswer': False}
    b = bridge(locale, "case 'Review.Mode':return 'learn'; default: if(n.startsWith('Review.'))return %s;" % J(view),
               {'engine': 'edge', 'aiProvider': 'deepseek', 'split': False, 'pinned': False, 'limit': 4000})
    run = "window.addEventListener('load',async()=>{await new Promise(r=>setTimeout(r,50));handlers['app:mode']&&handlers['app:mode']('learn');setTimeout(()=>{document.activeElement&&document.activeElement.blur();document.body.dataset.h=Math.ceil(document.body.getBoundingClientRect().height)},400);});"
    return 'index.html', b, run, 560

def stats(locale, zh):
    import random; random.seed(7)
    days = []
    for i in range(371):
        c = 0 if random.random() < (0.75 if i < 250 else 0.3) else random.randint(2, 40)
        lv = 0 if c == 0 else 1 if c < 10 else 2 if c < 20 else 3 if c < 30 else 4
        days.append({'date': '2026-11-20', 'count': c, 'level': lv})
    grades = [('again', '再来一次', 'Again'), ('hard', '有点吃力', 'Hard'), ('good', '记住了', 'Good'), ('easy', '很熟练', 'Easy')]
    gn = [{'value': v, 'title': z if zh else e} for v, z, e in grades]
    titles = [('translation', '中文', 'Chinese'), ('dictation', '听写', 'Dictation'), ('correction', '改错', 'Correction'), ('building', '连词成句', 'Sentence building')]
    by = [{'mode': m, 'title': z if zh else e, 'total': t, 'grades': g} for (m, z, e), t, g in zip(titles, [96, 64, 30, 41],
          [{'again': 8, 'hard': 14, 'good': 40, 'easy': 34}, {'again': 9, 'hard': 12, 'good': 25, 'easy': 18}, {'again': 4, 'hard': 6, 'good': 12, 'easy': 8}, {'again': 5, 'hard': 9, 'good': 16, 'easy': 11}])]
    s = {'today': 18, 'streak': 12, 'recent': 231, 'accuracy': 84, 'studyDays': sum(1 for d in days if d['count']), 'yearTotal': sum(d['count'] for d in days), 'empty': False, 'days': days, 'gradeNames': gn, 'byMode': by}
    today = {'due': 14, 'new': 6, 'done': 18, 'streak': 12, 'total': 48}
    b = bridge(locale, "case 'Learn.Today':return %s; case 'Learn.Stats':return %s; case 'Learn.Notebook':return {entries:[],total:48,writable:true,status:'ready',saveFailed:false,groups:[{id:'',name:%s,count:48}]};" % (J(today), J(s), J('默认' if zh else 'Default')), {})
    run = "window.addEventListener('load',async()=>{await new Promise(r=>setTimeout(r,80));document.querySelector('[data-page=\"stats\"]').click();setTimeout(()=>{document.activeElement&&document.activeElement.blur();document.body.dataset.h=640},400);});"
    return 'learn.html', b, run, 900

def shoot(name, page, b, run, width, height=900):
    with tempfile.TemporaryDirectory() as temp:
        html = (web / page).read_text(encoding='utf-8').replace('<head>', '<head><base href="' + web.as_uri() + '/">')
        script = re.search(r'<script src="(app|learn)\.js"></script>', html).group(0)
        html = html.replace(script, '<script>' + b + '</script>' + script + '<script>' + run + '</script>')
        p = pathlib.Path(temp) / 'p.html'; p.write_text(html, encoding='utf-8')
        args = [CHROME, '--headless', '--disable-gpu', '--no-first-run', '--hide-scrollbars', '--allow-file-access-from-files', '--force-device-scale-factor=2',
                '--user-data-dir=' + temp + '/profile', '--virtual-time-budget=6000']
        dom = subprocess.run(args + ['--dump-dom', '--window-size=%d,%d' % (width, height), p.as_uri()], capture_output=True, text=True, timeout=60).stdout
        h = int(re.search(r'data-h="(\d+)"', dom).group(1))
        subprocess.run(args + ['--screenshot=' + str(out / (name + '.png')), '--window-size=%d,%d' % (width, h), p.as_uri()], capture_output=True, timeout=60)
        print(name, width, h)

for locale in ('zh-CN', 'en'):
    zh = locale == 'zh-CN'; sfx = 'zh' if zh else 'en'
    src, tgt = ('The best way to learn a language is to use it every day, even if only for a few minutes.', '学习一门语言最好的办法，是每天都用它，哪怕只有几分钟。')
    if not zh: src, tgt = tgt, src
    shoot('translate-' + sfx, *tool(locale, 'translation', src, {'text': tgt, 'mode': 'translation', 'engine': 'edge'}))
    corrected = 'Thanks for your reply. I have attached the report. Please let me know if you have any questions.'
    shoot('check-' + sfx, *tool(locale, 'grammar', 'Thanks for your reply. I has attached the report, please let me know if you have any question.', {
        'text': corrected, 'mode': 'grammar', 'engine': 'deepseek',
        'grammar': {'Status': 'checked', 'CorrectedText': corrected, 'Meaning': '感谢回复。我已附上报告，如有问题请告诉我。' if zh else 'Thanks for replying. The report is attached; tell me if anything is unclear.',
                    'Issues': [{'Original': 'has', 'Replacement': 'have', 'Explanation': '主语 I 后用 have。' if zh else 'Use “have” after “I”.'},
                               {'Original': 'question', 'Replacement': 'questions', 'Explanation': 'any 后接可数名词复数。' if zh else 'Use the plural after “any”.'}]},
        'diff': [{'Text': 'Thanks for your reply. I ', 'Changed': False}, {'Text': 'have', 'Changed': True}, {'Text': ' attached the report', 'Changed': False}, {'Text': '. Please', 'Changed': True}, {'Text': ' let me know if you have any ', 'Changed': False}, {'Text': 'questions', 'Changed': True}, {'Text': '.', 'Changed': False}]}))
    shoot('review-' + sfx, *review(locale, zh))
    shoot('stats-' + sfx, *stats(locale, zh), height=640)
