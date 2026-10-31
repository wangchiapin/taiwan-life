# YouBike 的正解；tools/smoke.py 讀這裡的 ORACLE
ORACLE = """() => {
  const t = Game.task, s = Game.state;
  const m = {
    START: '打開 YouBike 的 App', FIND: '去' + t.borrow.find(x => x.bikes > 0).name + '借車', CHOOSE: '借座墊正常的那一台', TAP: '按綠色的「啟動靠卡」，再把悠遊卡放在感應區',
    OUT: '換旁邊另一台車', PULL: '雙手握住把手，往後拉出來', SEAT: '把座墊調高一點', ROAD: '騎在馬路的右邊', LIGHT: '停下來，等綠燈',
    RETURN_FIND: '去' + t.ret.find(x => x.docks > 0).name + '還車', DOCK: '把車推進車柱，看到「還車成功」，再靠一次悠遊卡',
    END: '查看結果', RESULT: '查看排行榜'
  };
  return m[s] ?? null;
}"""
