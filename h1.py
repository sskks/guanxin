import re
with open('index.html','r',encoding='utf-8') as f:
    c = f.read()

# 1. 添加历史入口到罗盘下方
c = c.replace('南离每日 · 北坎命宫 · 东震问卦 · 西兑节气</p>',
  '南离每日 · 北坎命宫 · 东震问卦 · 西兑节气</p>' +
  '<div style="text-align:center;margin-top:var(--space-lg)">' +
  '<button onclick="goTo(\'history\')" class="btn btn-outline" style="font-size:var(--text-sm)">📜 占卦回顾</button></div>')

# 2. 更新 goTo map
c = c.replace("const map={splash:'splash-screen',home:'home-screen',almanac:'almanac-screen',birthday:'birthday-screen',bazhai:'bazhai-screen'};",
  "const map={splash:'splash-screen',home:'home-screen',almanac:'almanac-screen',birthday:'birthday-screen',bazhai:'bazhai-screen',history:'history-screen'};")

with open('index.html','w',encoding='utf-8') as f:
    f.write(c)
print('OK step 1')
