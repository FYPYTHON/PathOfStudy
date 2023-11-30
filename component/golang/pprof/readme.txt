# 参考
https://www.zhihu.com/tardis/bd/art/371713134?source_id=1001

https://www.yuque.com/u12472119/wtxoi6/ny150b

https://www.cnblogs.com/zhanchenjin/p/17101573.html


go tool pprof http://192.168.1.27:8081/debug/pprof/allocs
将数据采集下来
go tool pprof -http=192.168.1.27:8081 pprof.server.alloc_objects.alloc_space.inuse_objects.inuse_space.001.pb.gz 


文件默认在：/root/pprof/ 
go tool pprof http://127.0.0.1:8081/debug/pprof/heap
go tool pprof http://127.0.0.1:8081/debug/pprof/profile

图片查看,需要安装graphviz  https://shidawuhen.github.io/2020/02/08/go-callvis/
go tool pprof -png http://127.0.0.1:9239/debug/pprof/heap > heap.png

