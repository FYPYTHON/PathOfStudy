None
# 下载安装

## protoc

> 下载地址：https://github.com/protocolbuffers/protobuf/releases

> 文件protoc-22.3-linux-x86_64.zip

> 解压后得bin/protoc

## protoc-gen-go下载

> 下载地址： https://github.com/protocolbuffers/protobuf-go/releases

> 文件protoc-gen-go.v1.30.0.linux.amd64.tar.gz

> 解压后得bin/protoc-gen-go

## protoc-gen-go-grpc下载

> 下载地址：https://github.com/pexip/os-protoc-gen-go-grpc/tags

> 文件Source code(tar.gz) （os-protoc-gen-go-grpc-upstream-1.2.0.tar.gz）

> 或 git clone git@github.com:pexip/os-protoc-gen-go-grpc.git

**安装编译**

```{.python .input}
cd os-protoc-gen-go-grpc-upstream-1.2.0/cmd/protoc-gen-go-grpc
go build -mod=vendor -o bin/protoc-gen-go-grpc *.go
```

# hello.proto

```{.python .input}
syntax = "proto3";
package hello;
option go_package = "../hello";  // go需要
option cc_generic_services = true;
//定义服务接口
service GrpcService {
    rpc hello (HelloRequest) returns (HelloResponse) {}  //一个服务中可以定义多个接口，也就是多个函数功能
}
//请求的参数
message HelloRequest {
    string data = 1;   //数字1,2是参数的位置顺序，并不是对参数赋值
    Skill skill = 2;  //支持自定义的数据格式，非常灵活
};
//返回的对象
message HelloResponse {
    string result = 1;
    map<string, int32> map_result = 2; //支持map数据格式，类似dict
};
message Skill {
    string name = 1;
};
```

```{.python .input}
cd bin/ && ./protoc --plugin=./protoc-gen-go -I ../ hello.proto --go_out=.
```

**生成文件../hello/hello.pb.go**

```{.python .input}
./protoc --plugin=./protoc-gen-go-grpc -I ../ hello.proto --go-grpc_out=require_unimplemented_servers=false:.
```

**生成文件../hello/hello_grpc.pb.go**

.proto生成golang .pb.go .grpc.pg.go完成
