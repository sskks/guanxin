with open('index.html','r',encoding='utf-8') as f:
    c = f.read()

# 重写 renderAlmanac，完整显示日历、宜忌、吉时、养生
c = c.replace('function renderAlmanac(){const now=new Date(),y=now.getFullYear(),m=now.getMonth()+1,d=now.getDate();const jq=getJieqi(m,d);document.getElementById('almanac-content').innerHTML=\'<h3>今日：\'+m+\'月\'+d+\'日</h3><p style="margin-top:var(--space-sm)">\'+(jq?\'当前节气：\'+jq.name+\'：\'+jq.desc:\'下一个节气临近...\')+\'</p>\';}',
'''let almanacDate=new Date();
function navAlmanac(dir){almanacDate.setDate(almanacDate.getDate()+dir);renderAlmanac();}
function renderAlmanac(){
  const y=almanacDate.getFullYear(),m=almanacDate.getMonth()+1,d=almanacDate.getDate();
  const wd=['日','一','二','三','四','五','六'][almanacDate.getDay()];
  const jq=getJieqi(m,d);
  const season=getSeason(m);
  const YIJI_POOL={spring:['踏青','植树','读书','访友','迁居','开市'],summer:['纳凉','游泳','赏荷','品茗','祭祀','祈福'],autumn:['登高','赏菊','收获','晾晒','祭祀','祈福'],winter:['进补','藏书','祭祀','祈福','安床','移徙']};
  const JI_POOL={spring:['动土','破土','远行','嫁娶'],summer:['动火','曝晒','远行','嫁娶'],autumn:['砍伐','杀生','远行','嫁娶'],winter:['受寒','熬夜','远行','嫁娶']};
  const yi=YIJI_POOL[season],ji=JI_POOL[season];
  const seed=(d*7+13)%100;
  const SHI_CHEN=['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥'];
  const SHI_TIME=['23-1','1-3','3-5','5-7','7-9','9-11','11-13','13-15','15-17','17-19','19-21','21-23'];
  const yangsheng={
    spring:'春三月，此谓发陈。天地俱生，万物以荣。夜卧早起，广步于庭，披发缓形，以使志生。宜食辛温发散之品，忌酸收。',
    summer:'夏三月，此谓蕃秀。天地气交，万物华实。夜卧早起，无厌于日。使志无怒，使华英成秀，使气得泄。宜食清淡清热，忌厚味。',
    autumn:'秋三月，此谓容平。天气以急，地气以明。早卧早起，与鸡俱兴。使志安宁，以缓秋刑。收敛神气，使秋气平。宜食润燥生津，忌辛辣。',
    winter:'冬三月，此谓闭藏。水冰地坼，无扰乎阳。早卧晚起，必待日光。使志若伏若匿，若有私意，若已有得。去寒就温，无泄皮肤。宜食温补，忌寒凉。'
  };
  document.getElementById('almanac-content').innerHTML=
    '<div style="text-align:center;padding:var(--space-lg);background:var(--paper-light);border:1px solid var(--ink-ghost);border-radius:var(--radius-md);margin-bottom:var(--space-lg)">' +
    '<div style="font-family:var(--font-display);font-size:var(--text-2xl);color:var(--ink-deep)">'+m+'月'+d+'日</div>' +
    '<div style="font-family:var(--font-serif);font-size:var(--text-sm);color:var(--ink-light);margin-top:var(--space-xs)">星期'+wd+'</div>' +
    (jq?'<div style="margin-top:var(--space-sm);padding:var(--space-xs) var(--space-md);background:var(--cinnabar-bg);border-radius:var(--radius-full);display:inline-block;font-family:var(--font-serif);color:var(--cinnabar)">'+jq.name+'</div><p style="font-family:var(--font-serif);font-size:var(--text-sm);color:var(--ink-light);line-height:1.8;margin-top:var(--space-sm)">'+jq.desc+'</p>':'') +
    '</div>' +
    '<div style="display:flex;gap:var(--space-md);margin-bottom:var(--space-md)">' +
    '<div style="flex:1;padding:var(--space-md);background:rgba(106,142,110,0.1);border-radius:var(--radius-md);text-align:center">' +
    '<span style="font-family:var(--font-display);font-size:var(--text-xl);color:var(--jade)">宜</span>' +
    '<p style="font-family:var(--font-serif);font-size:var(--text-sm);color:var(--ink);line-height:1.8;margin-top:var(--space-xs)">' + yi.slice(seed%3,seed%3+2).join('、') + '</p>' +
    '</div>' +
    '<div style="flex:1;padding:var(--space-md);background:var(--cinnabar-bg);border-radius:var(--radius-md);text-align:center">' +
    '<span style="font-family:var(--font-display);font-size:var(--text-xl);color:var(--cinnabar)">忌</span>' +
    '<p style="font-family:var(--font-serif);font-size:var(--text-sm);color:var(--ink);line-height:1.8;margin-top:var(--space-xs)">' + ji.slice(seed%2,seed%2+1).join('、') + '</p>' +
    '</div></div>' +
    '<div style="background:var(--paper-light);border:1px solid var(--ink-ghost);border-radius:var(--radius-md);padding:var(--space-lg);margin-bottom:var(--space-md)">' +
    '<h4 style="font-family:var(--font-serif);font-size:var(--text-base);color:var(--ink-deep);text-align:center;margin-bottom:var(--space-md)">十二时辰吉凶</h4>' +
    '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:var(--space-xs)">' +
    SHI_CHEN.map((s,i)=>'<div style="text-align:center;padding:var(--space-xs);border-radius:var(--radius-sm);background:'+((seed+i*11)%5<3?'rgba(106,142,110,0.1)':'rgba(168,60,50,0.05)')+'">' +
    '<span style="font-family:var(--font-serif);font-size:var(--text-xs);color:var(--ink-light)">'+s+'时</span><br>' +
    '<span style="font-size:var(--text-sm);color:'+((seed+i*11)%5<3?'var(--jade)':'var(--ink-faint)')+'">'+((seed+i*11)%5<3?'吉':'平')+'</span></div>').join('') +
    '</div></div>' +
    '<div style="background:var(--paper-light);border:1px solid var(--ink-ghost);border-radius:var(--radius-md);padding:var(--space-lg)">' +
    '<h4 style="font-family:var(--font-serif);font-size:var(--text-base);color:var(--ink-deep);text-align:center;margin-bottom:var(--space-md)">节气养生</h4>' +
    '<p style="font-family:var(--font-serif);font-size:var(--text-sm);color:var(--ink);line-height:2;text-align:justify">'+yangsheng[season]+'</p></div>';
}
''')

# 更新日历顶部导航
c = c.replace('<button class="btn btn-outline" style="padding:var(--space-xs) var(--space-sm);min-height:36px;font-size:var(--text-xs)" onclick="goTo(\'home\')">← 返回</button>',
  '<button class="btn btn-outline" style="padding:var(--space-xs) var(--space-sm);min-height:36px;font-size:var(--text-xs)" onclick="navAlmanac(-1)">← 前一天</button>')
c = c.replace('<span style="font-family:var(--font-serif);font-size:var(--text-base);color:var(--ink-deep)">节气日历</span>',
  '<span style="font-family:var(--font-serif);font-size:var(--text-base);color:var(--ink-deep)" id="almanac-title">今日</span>')
c = c.replace('<div style="width:60px"></div>',
  '<button class="btn btn-outline" style="padding:var(--space-xs) var(--space-sm);min-height:36px;font-size:var(--text-xs)" onclick="navAlmanac(1)">后一天 →</button>')

with open('index.html','w',encoding='utf-8') as f:
    f.write(c)

print('OK 二十四节气深化完成')
