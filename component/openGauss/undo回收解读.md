
# undo 回收过程

主要函数

UndoRecycleMain	        回收线程的入口函数，会在每个zone上调用RecycleUndoSpace函数
RecycleUndoSpace	按照前述条件回收undo空间，记录日志


参考

[openGauss ustore回滚段设计与MVCC](https://www.modb.pro/db/208954)

