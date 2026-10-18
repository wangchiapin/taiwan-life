# YouBike 的正解；tools/smoke.py 讀這裡的 ORACLE
ORACLE = """() => {
  const t = Game.task, s = Game.state;
  const m = {
    START: '打開 YouBike 的 App', FIND: '去' + t.borrow.find(x => x.bikes > 0).name + '借車', TAP: '把悠遊卡放在感應區',
    PULL: '拉出綠燈亮著的那一台', SEAT: '把座墊調高一點', ROAD: '騎在馬路的右邊', LIGHT: '停下來，等綠燈',
    RETURN_FIND: '去' + t.ret.find(x => x.docks > 0).name + '還車', DOCK: '把車推進車柱，等「嗶」一聲，看螢幕有沒有「還車成功」'
  };
  return m[s] ?? null;
}"""
