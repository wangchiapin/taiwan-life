# 公車的正解；tools/smoke.py 讀這裡的 ORACLE
ORACLE = """() => {
  const t = Game.task, s = Game.state;
  const m = {
    START: '走去公車站牌', STOP: '在「往' + t.dir + '」的站牌等', WAIT: '等' + t.route[1] + '路公車', HAIL: '招手，讓公車停下來',
    TAP_ON: '刷悠遊卡', ASK: '司機大哥，請問這台公車有到' + t.dest + '站嗎？',
    RING: t.stops[Game.step] === t.dest ? '現在按下車鈴' : '先不按，繼續坐', TAP_OFF: '刷悠遊卡，跟司機說「謝謝」'
  };
  return m[s] ?? null;
}"""
