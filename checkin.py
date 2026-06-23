with open('index.html','r',encoding='utf-8') as f:
    c = f.read()

# 1. 在首页顶部添加打卡徽章
c = c.replace('<div style="text-align:center;margin-bottom:var(--space-xl);position:relative">',
  '''<div style="text-align:center;margin-bottom:var(--space-xl);position:relative">
      <div id="checkin-badge" style="position:absolute;right:0;top:0;font-size:var(--text-sm);font-family:var(--font-serif);color:var(--cinnabar);padding:var(--space-xs) var(--space-sm);background:var(--cinnabar-bg);border-radius:var(--radius-full)"></div>''')

# 2. 添加打卡JS
checkin_js = '''
// 每日打卡连续记录
function updateCheckinBadge(){
  const checkins=JSON.parse(localStorage.getItem('guanxin_checkins')||'[]');
  const today=new Date().toDateString();
  const isChecked=checkins.includes(today);
  const badge=document.getElementById('checkin-badge');
  if(badge){badge.textContent=checkins.length+'天 · '+ (isChecked?'已打卡':'未打卡');}
}
function dailyCheckin(){
  let checkins=JSON.parse(localStorage.getItem('guanxin_checkins')||'[]');
  const today=new Date().toDateString();
  if(!checkins.includes(today)){checkins.push(today);localStorage.setItem('guanxin_checkins',JSON.stringify(checkins));alert('打卡成功！今日已观心自省~');}
  updateCheckinBadge();
}
// 页面加载时显示打卡徽章
window.addEventListener('load',()=>{
  updateCheckinBadge();
  // 首页点击标题可打卡
  document.querySelector('.daily-inner h2')?.addEventListener('click',dailyCheckin);
});
'''
c = c.replace('window.addEventListener(\'load\',checkFriendShare);', checkin_js + 'window.addEventListener(\'load\',checkFriendShare);')

with open('index.html','w',encoding='utf-8') as f:
    f.write(c)

print('OK 每日打卡功能完成')
