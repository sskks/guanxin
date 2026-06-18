with open('prototype.html','r',encoding='utf-8') as f:
    c = f.read()

# 找到 renderAlmanac 开始，替换整个函数
old_func_start = 'function renderAlmanac(){'
idx = c.find(old_func_start)
end_idx = c.find('}', idx)

# 替换为完整的日历功能
new_func = '''let almanacDate=new Date();
function navAlmanac(dir){almanacDate.setDate(almanacDate.getDate()+dir);renderAlmanac();}
function renderAlmanac(){
  const y=almanacDate.getFullYear(),m=almanacDate.getMonth()+1,d=almanacDate.getDate();
  const wd=['日','一','二','三','四','五','六'][almanacDate.getDay()];
  const jq=getJieqi(m,d);
  const season=getSeason(m);
  const YIJI_POOL={spring:['踏青','植树','读书','访友'],summer:['纳凉','赏荷','品茗'],autumn:['登高','赏菊','收获'],winter:['进补','藏书','祭祀']};
  const JI_POOL={spring:['动土','远行'],summer:['动火','曝晒'],autumn:['砍伐','杀生'],winter:['受寒','熬夜']};
  const yi=YIJI_POOL[season],ji=JI_POOL[season];
  const seed=(d*7+13)%100;
  const yangsheng={spring:'春三月，此谓发陈。天地俱生，万物以荣。夜卧早起，广步于庭，披发缓形，以使志生。',
    summer:'夏三月，此谓蕃秀。天地气交，万物华实。夜卧早起，无厌于日。使志无怒，使华英成秀。',
    autumn:'秋三月，此谓容平。天气以急，地气以明。早卧早起，与鸡俱兴。使志安宁。',
    winter:'冬三月，此谓闭藏。水冰地坼，无扰乎阳。早卧晚起，必待日光。去寒就温。'};
  const SHI_CHEN=['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥'];
  document.getElementById('almanac-title').textContent=m+'月'+d+'日 星期'+wd;
  let html='<div style="text-align:center;padding:var(--space-lg);background:var(--paper-light);border:1px solid var(--ink-ghost);border-radius:var(--radius-md);margin-bottom:var(--space-lg)">';
  if(jq)html+='<div style="padding:var(--space-xs) var(--space-md);background:var(--cinnabar-bg);border-radius:var(--radius-full);display:inline-block;font-family:var(--font-serif);color:var(--cinnabar);margin-bottom:var(--space-sm)">'+jq.name+'</div><p style="font-family:var(--font-serif);font-size:var(--text-sm);color:var(--ink-light);line-height:1.8">'+jq.desc+'</p>';
  html+='</div><div style="display:flex;gap:var(--space-md);margin-bottom:var(--space-md)">' +
    '<div style="flex:1;padding:var(--space-md);background:rgba(106,142,110,0.1);border-radius:var(--radius-md);text-align:center"><span style="font-family:var(--font-display);font-size:var(--text-xl);color:var(--jade)">宜</span><p style="font-family:var(--font-serif);font-size:var(--text-sm);color:var(--ink);line-height:1.8;margin-top:var(--space-xs)">'+yi.slice(seed%2,seed%2+2).join('、')+'</p></div>' +
    '<div style="flex:1;padding:var(--space-md);background:var(--cinnabar-bg);border-radius:var(--radius-md);text-align:center"><span style="font-family:var(--font-display);font-size:var(--text-xl);color:var(--cinnabar)">忌</span><p style="font-family:var(--font-serif);font-size:var(--text-sm);color:var(--ink);line-height:1.8;margin-top:var(--space-xs)">'+ji[seed%2]+'</p></div></div>' +
    '<div style="background:var(--paper-light);border:1px solid var(--ink-ghost);border-radius:var(--radius-md);padding:var(--space-lg);margin-bottom:var(--space-md)"><h4 style="font-family:var(--font-serif);font-size:var(--text-base);color:var(--ink-deep);text-align:center;margin-bottom:var(--space-md)">十二时辰</h4><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:var(--space-xs)">';
  for(let i=0;i<12;i++){
    const isJi=(seed+i*11)%5<3;
    html+='<div style="text-align:center;padding:var(--space-xs);border-radius:var(--radius-sm);background:'+(isJi?'rgba(106,142,110,0.1)':'rgba(168,60,50,0.05)')+'"><span style="font-family:var(--font-serif);font-size:var(--text-xs);color:var(--ink-light)">'+SHI_CHEN[i]+'时</span><br><span style="font-size:var(--text-sm);color:'+(isJi?'var(--jade)':'var(--ink-faint)')+'">'+(isJi?'吉':'平')+'</span></div>';
  }
  html+='</div></div><div style="background:var(--paper-light);border:1px solid var(--ink-ghost);border-radius:var(--radius-md);padding:var(--space-lg)"><h4 style="font-family:var(--font-serif);font-size:var(--text-base);color:var(--ink-deep);text-align:center;margin-bottom:var(--space-md)">节气养生</h4><p style="font-family:var(--font-serif);font-size:var(--text-sm);color:var(--ink);line-height:2;text-align:justify">'+yangsheng[season]+'</p></div>';
  document.getElementById('almanac-content').innerHTML=html;
}
'''
c = c[:idx] + new_func + c[end_idx+1:]

# 修复导航按钮
c = c.replace('onclick="goTo(\'home\')">← 返回</button>', 'onclick="goTo(\'home\')" style="padding:var(--space-xs) var(--space-sm);min-height:36px;font-size:var(--text-xs)">← 返回</button>')
c = c.replace('<div style="width:60px"></div>', '<button class="btn btn-outline" style="padding:var(--space-xs) var(--space-sm);min-height:36px;font-size:var(--text-xs)" onclick="navAlmanac(1)">后一天 →</button>')

with open('prototype.html','w',encoding='utf-8') as f:
    f.write(c)

print('OK 节气日历深化完成')
