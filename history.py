with open('index.html','r',encoding='utf-8') as f:
    c = f.read()

# 1. 在首页罗盘下方添加历史入口
c = c.replace('      <p style="font-size:var(--text-xs);margin-top:var(--space-xs)">南离每日 · 北坎命宫 · 东震问卦 · 西兑节气</p>',
  '''      <p style="font-size:var(--text-xs);margin-top:var(--space-xs)">南离每日 · 北坎命宫 · 东震问卦 · 西兑节气</p>
    <div style="text-align:center;margin-top:var(--space-lg)">
      <button onclick="goTo('history')" class="btn btn-outline" style="font-size:var(--text-sm)">📜 占卦回顾</button>
    </div>''')

# 2. 在 goTo map 中添加 history
c = c.replace("const map={splash:'splash-screen',home:'home-screen',almanac:'almanac-screen',birthday:'birthday-screen',bazhai:'bazhai-screen'};",
  "const map={splash:'splash-screen',home:'home-screen',almanac:'almanac-screen',birthday:'birthday-screen',bazhai:'bazhai-screen',history:'history-screen'};")

# 3. 在命宫页后添加历史记录页
history_html = '''
<div id="history-screen" class="screen scrollable">
  <div class="daily-inner" style="width:100%;max-width:500px;padding:var(--space-xl) var(--space-md)">
    <h2 style="font-family:var(--font-display);font-size:var(--text-xl);color:var(--ink-deep);text-align:center;margin-bottom:var(--space-xs);letter-spacing:0.2em">占卦回顾</h2>
    <p style="font-family:var(--font-serif);font-size:var(--text-sm);color:var(--ink-light);text-align:center;margin-bottom:var(--space-lg)">观照自己的心路历程</p>
    <div id="history-list"></div>
    <div id="history-empty" style="text-align:center;padding:var(--space-xl);color:var(--ink-faint)">
      <p>暂无占卦记录</p>
      <p style="font-size:var(--text-xs);margin-top:var(--space-xs)">诚心问卦，答案自在心中</p>
    </div>
    <button onclick="goTo('home')" class="btn btn-outline" style="width:100%;margin-top:var(--space-lg)">返回首页</button>
  </div>
</div>
'''

c = c.replace('</div>\n\n<div id="bazhai-screen"', history_html + '</div>\n\n<div id="bazhai-screen"')

# 4. 在以事问卦功能中添加记录保存逻辑
old_question = 'function doQuestionHex(){ alert(\\'以事问卦功能开发中\\'); }'
new_question = '''function doQuestionHex(){
  const q=prompt('心中所问之事：（诚心正意，卦象方灵）');
  if(!q)return;
  // 简易梅花易数：按问题字数起卦
  const n=q.length;
  const up=n%8||8;
  const down=(n+new Date().getHours())%8||8;
  const guaNames=['乾','兑','离','震','巽','坎','艮','坤'];
  const gua=guaNames[up-1]+guaNames[down-1];
  const yaos=['初爻','二爻','三爻','四爻','五爻','六爻'];
  const yao=(n+new Date().getMinutes())%6;
  // 保存记录
  const records=JSON.parse(localStorage.getItem('guanxin_records')||'[]');
  records.unshift({
    date:new Date().toLocaleDateString('zh-CN'),
    time:new Date().toLocaleTimeString('zh-CN',{hour:'2-digit',minute:'2-digit'}),
    question:q,
    gua:gua,
    yao:yaos[yao],
    id:Date.now()
  });
  localStorage.setItem('guanxin_records',JSON.stringify(records.slice(0,50)));
  alert('得 '+gua+'卦 · '+yaos[yao]+'动\\n\\n诚心观想答案，后续AI解读功能正在开发中');
}
'''
c = c.replace(old_question, new_question)

# 5. 添加历史页面渲染JS
render_history_js = '''
function renderHistory(){
  const list=document.getElementById('history-list');
  const empty=document.getElementById('history-empty');
  const records=JSON.parse(localStorage.getItem('guanxin_records')||'[]');
  if(records.length===0){
    list.innerHTML='';
    empty.style.display='block';
    return;
  }
  empty.style.display='none';
  list.innerHTML=records.map(r=>
    '<div style="background:var(--paper-light);border:1px solid var(--ink-ghost);border-radius:var(--radius-md);padding:var(--space-md);margin-bottom:var(--space-sm)">'+
    '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:var(--space-xs)">'+
    '<span style="font-family:var(--font-display);font-size:var(--text-base);color:var(--cinnabar)">'+r.gua+'</span>'+
    '<span style="font-size:var(--text-xs);color:var(--ink-faint)">'+r.date+' '+r.time+'</span>'+
    '</div>'+
    '<p style="font-family:var(--font-serif);font-size:var(--text-sm);color:var(--ink);line-height:1.7">问：'+r.question+'</p>'+
    '<p style="font-size:var(--text-xs);color:var(--ink-light);margin-top:var(--space-xs)">动爻：'+r.yao+'</p>'+
    '</div>'
  ).join('');
}
// 页面切换时自动渲染
const oldGoTo = c.split('function goTo(page){')[1].split('}')[0]
c = c.replace('function goTo(page){' + oldGoTo + '}', '''function goTo(page){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));
  const map={splash:'splash-screen',home:'home-screen',almanac:'almanac-screen',birthday:'birthday-screen',bazhai:'bazhai-screen',history:'history-screen'};
  const el=document.getElementById(map[page]);
  if(el){el.classList.add('active');window.scrollTo(0,0);}
  if(page==='history')renderHistory();
}''')

with open('index.html','w',encoding='utf-8') as f:
    f.write(c)

print('OK 占卦历史功能完成')
