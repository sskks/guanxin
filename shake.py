with open('prototype.html','r',encoding='utf-8') as f:
    c = f.read()

# 1. 在东震问卦功能中改为跳转到摇卦页
c = c.replace('function doQuestionHex(){', '''function doQuestionHex(){goTo('shaking');startShaking();return;}
function startShaking(){
  setTimeout(()=>{
    const q=prompt('心中所问之事：（诚心正意，卦象方灵）');
    if(!q){goTo('home');return;}
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
    records.unshift({date:new Date().toLocaleDateString('zh-CN'),time:new Date().toLocaleTimeString('zh-CN',{hour:'2-digit',minute:'2-digit'}),question:q,gua:gua,yao:yaos[yao],id:Date.now()});
    localStorage.setItem('guanxin_records',JSON.stringify(records.slice(0,50)));
    // 显示结果
    document.getElementById('shaking-result').innerHTML=
      '<div style="text-align:center;padding:var(--space-xl)">' +
      '<div style="font-family:var(--font-display);font-size:3rem;color:var(--cinnabar);letter-spacing:0.2em">'+gua+'</div>' +
      '<h3 style="font-family:var(--font-serif);font-size:var(--text-lg);color:var(--ink-deep);margin-top:var(--space-sm)">卦成</h3>' +
      '<p style="font-family:var(--font-serif);font-size:var(--text-base);color:var(--ink);line-height:1.9;margin-top:var(--space-md)">诚心观想答案，卦象已现</p>' +
      '<p style="font-size:var(--text-sm);color:var(--ink-light);margin-top:var(--space-xs)">动爻：'+yaos[yao]+'</p>' +
      '</div>';
    document.getElementById('shaking-result').style.display='block';
    document.getElementById('shaking-done-btn').style.display='block';
  },3000);
}
function realDoQuestionHex(){''')

# 2. 在 goTo map 中添加 shaking
c = c.replace("const map={splash:'splash-screen',home:'home-screen',almanac:'almanac-screen',birthday:'birthday-screen',bazhai:'bazhai-screen',history:'history-screen',friend:'friend-screen'};",
  "const map={splash:'splash-screen',home:'home-screen',almanac:'almanac-screen',birthday:'birthday-screen',bazhai:'bazhai-screen',history:'history-screen',friend:'friend-screen',shaking:'shaking-screen'};")

# 3. 添加摇卦屏幕 HTML（在节气日历前）
shaking_html = '''
<div id="shaking-screen" class="screen">
  <div style="text-align:center;padding:var(--space-xl)">
    <div id="shaking-bamboo" style="font-size:5rem;margin-bottom:var(--space-xl);animation:bambooShake 0.15s infinite alternate;cursor:pointer">🎋</div>
    <h3 style="font-family:var(--font-display);font-size:var(--text-xl);color:var(--ink-deep);letter-spacing:0.2em;margin-bottom:var(--space-md)">诚心摇卦</h3>
    <p id="shaking-hint" style="font-family:var(--font-serif);font-size:var(--text-base);color:var(--ink-light);line-height:1.8">静心凝神，默念所问之事...</p>
    <div id="shaking-result" style="display:none"></div>
    <button id="shaking-done-btn" onclick="goTo('home')" class="btn btn-primary" style="display:none;margin-top:var(--space-lg)">完成</button>
  </div>
</div>
<style>
@keyframes bambooShake{
  0%{transform:rotate(-5deg) translateY(0)}
  100%{transform:rotate(5deg) translateY(-5px)}
}
</style>
'''

c = c.replace('<div id="almanac-screen"', shaking_html + '<div id="almanac-screen"')

with open('prototype.html','w',encoding='utf-8') as f:
    f.write(c)

print('OK 摇卦动画完成')
