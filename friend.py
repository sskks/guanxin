with open('prototype.html','r',encoding='utf-8') as f:
    c = f.read()

# 1. 在命宫页 AI 解读下方添加分享给好友按钮
c = c.replace('    <button onclick="goTo(\'home\')" class="btn btn-outline" style="width:100%;margin-top:var(--space-md)">返回首页</button>',
  '''    <div style="margin-top:var(--space-md);text-align:center">
      <button onclick="shareToFriend()" class="btn btn-outline" style="font-size:var(--text-sm)">🌿 分享给好友（互占互助）</button>
    </div>
    <button onclick="goTo('home')" class="btn btn-outline" style="width:100%;margin-top:var(--space-md)">返回首页</button>''')

# 2. 在启动页面添加好友互占入口（检测 URL 参数）
c = c.replace('    <button class="btn btn-primary" style="margin-top:var(--space-xl)" onclick="goTo(\'home\')">进入</button>',
  '''    <button class="btn btn-primary" style="margin-top:var(--space-xl)" onclick="goTo('home')">进入</button>
    <div id="friend-entry" style="display:none;margin-top:var(--space-md)">
      <button class="btn btn-outline" onclick="viewFriendShare()" style="font-size:var(--text-sm)">💫 查看好友分享</button>
    </div>''')

# 3. 添加好友互占屏幕
friend_html = '''
<div id="friend-screen" class="screen scrollable">
  <div style="width:100%;max-width:500px;padding:var(--space-xl) var(--space-md)">
    <h2 style="font-family:var(--font-display);font-size:var(--text-xl);color:var(--ink-deep);text-align:center;margin-bottom:var(--space-xs);letter-spacing:0.2em">好友分享</h2>
    <p style="font-family:var(--font-serif);font-size:var(--text-sm);color:var(--ink-light);text-align:center;margin-bottom:var(--space-lg)">以善心观照，给好友温暖的建议</p>
    <div id="friend-content"></div>
    <div style="margin-top:var(--space-lg)">
      <h4 style="font-family:var(--font-serif);font-size:var(--text-base);color:var(--ink-deep);text-align:center;margin-bottom:var(--space-md)">我的善意建议</h4>
      <textarea id="friend-advice" placeholder="请输入你给好友的善意建议..." style="width:100%;min-height:100px;padding:var(--space-md);border:1px solid var(--ink-ghost);border-radius:var(--radius-md);background:var(--paper-light);font-family:var(--font-serif);font-size:var(--text-sm);line-height:1.8;resize:vertical"></textarea>
      <button onclick="copyAdvice()" class="btn btn-primary" style="width:100%;margin-top:var(--space-md)">✨ 生成祝福卡片</button>
    </div>
    <button onclick="goTo('home')" class="btn btn-outline" style="width:100%;margin-top:var(--space-md)">返回首页</button>
  </div>
</div>
'''
c = c.replace('</div>\n\n<div id="history-screen"', friend_html + '</div>\n\n<div id="history-screen"')

# 4. 更新 goTo map
c = c.replace("const map={splash:'splash-screen',home:'home-screen',almanac:'almanac-screen',birthday:'birthday-screen',bazhai:'bazhai-screen',history:'history-screen'};",
  "const map={splash:'splash-screen',home:'home-screen',almanac:'almanac-screen',birthday:'birthday-screen',bazhai:'bazhai-screen',history:'history-screen',friend:'friend-screen'};")

# 5. 添加好友互占 JS 函数
share_js = '''
// 好友互占功能：生成分享链接
function shareToFriend(){
  const birth=JSON.parse(localStorage.getItem('guanxin_birth')||'{}');
  if(!birth.gua){alert('请先计算命宫');return;}
  const params=new URLSearchParams({g:birth.gua,t:Date.now()});
  const link=window.location.href.split('?')[0]+'?'+params.toString();
  // 复制到剪贴板
  const ta=document.createElement('textarea');ta.value=link;document.body.appendChild(ta);ta.select();
  document.execCommand('copy');document.body.removeChild(ta);
  alert('分享链接已复制！\\n\\n发送给好友，让他/她给你善意的建议~\\n\\n链接：'+link);
}
// 检测是否有好友分享
function checkFriendShare(){
  const p=new URLSearchParams(window.location.search);
  if(p.get('g')){document.getElementById('friend-entry').style.display='block';}
}
window.addEventListener('load',checkFriendShare);
// 查看好友分享
function viewFriendShare(){
  const p=new URLSearchParams(window.location.search);
  const gua=p.get('g');
  if(!gua)return;
  const guaInfo=GUA_ATTR[gua]||GUA_ATTR['乾'];
  document.getElementById('friend-content').innerHTML=
    '<div style="text-align:center;padding:var(--space-xl);background:var(--paper-light);border:1px solid var(--ink-ghost);border-radius:var(--radius-lg)">'+
    '<div style="font-family:var(--font-display);font-size:2.5rem;color:var(--cinnabar);letter-spacing:0.2em">'+gua+'</div>'+
    '<h3 style="font-family:var(--font-serif);font-size:var(--text-base);color:var(--ink-deep);margin-top:var(--space-sm)">'+guaInfo.name+'</h3>'+
    '<p style="font-family:var(--font-serif);font-size:var(--text-sm);color:var(--ink);line-height:1.9;text-align:justify;margin-top:var(--space-md)">'+guaInfo.desc+'</p>'+
    '</div>';
  goTo('friend');
}
// 复制建议
function copyAdvice(){
  const advice=document.getElementById('friend-advice').value.trim();
  if(!advice){alert('请先输入建议');return;}
  const p=new URLSearchParams(window.location.search);
  const gua=p.get('g')||'乾';
  const card='【观心 · 好友祝福】\\n\\n本命卦：'+gua+'\\n\\n好友建议：\\n'+advice+'\\n\\n—— 来自观心APP的善意链接';
  const ta=document.createElement('textarea');ta.value=card;document.body.appendChild(ta);ta.select();
  document.execCommand('copy');document.body.removeChild(ta);
  alert('祝福卡片已复制！\\n\\n发给你的好友吧~');
}
'''
c = c.replace('function openSettings(){', share_js + 'function openSettings(){')

with open('prototype.html','w',encoding='utf-8') as f:
    f.write(c)

print('OK 好友互占功能完成')
