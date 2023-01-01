#!/bin/bash
#auth: 1823218990@qq.com
#time: 2022-12-29
#


curdir=$(dirname $0)
curpath=$(pwd $curdir)
cd $curpath


myPwd="pass:123456"

# ssl 证书输出的根目录
sslOutputRoot="./cert"
if [ $# -eq 1 ];then
    sslOutputRoot=$1
fi
rm -rf ${sslOutputRoot}
if [ ! -d ${sslOutputRoot} ];then
    mkdir -p ${sslOutputRoot}
    \cp ./req.cnf ${sslOutputRoot}/
fi
if [ ! -f ${sslOutputRoot}/req.cnf ];then
    \cp ${curpath}/req.cnf ${sslOutputRoot}/
fi


cd ${sslOutputRoot}

echo "开始创建CA根证书..."

# 生成CA根证书私钥
set -x
openssl genrsa -des3 -out ca.key -passout ${myPwd} 2048
set +x


# 生成CA根证书
set -x
openssl req -new -x509 -days 365 -key ca.key -out ca.crt -passin ${myPwd} -config req.cnf
set +x

echo "开始生成服务器证书签署文件及私钥"
# 生成服务器私钥
openssl genrsa -des3 -out server.key -passout ${myPwd} 2048
echo "服务器证书签署文件及私钥完毕"


# 生成服务器证书部署请求文件
openssl req -new -key server.key -out server.csr -passin ${myPwd} -config req.cnf
\cp server.csr server.crt
ls -altrh ./server.*

CSR=./server.csr
CERT=./server.crt
echo "开始使用CA根证书签署服务器证书签署文件..."
# 签署服务器证书,生成server.crt文件
# sh ${curpath}/sign.sh ./server.csr
echo "curpath: $curpath"
# sign the certificate
echo "CA signing: $CSR -> $CERT:"
set -x
openssl ca -config req.cnf -out $CERT -infiles $CSR
echo "CA verifying: $CERT <-> CA cert"
openssl verify -CAfile ./ca.crt $CERT
set +x

# cleanup after SSLeay
#rm -f req.cnf
#rm -f ca.db.serial.old
#rm -f ca.db.index.old

echo "使用CA根证书签署服务器证书签署文件完毕"


# test
exit 0


# 创建客户端证书
\cp -f server.crt client.crt
\cp -f server.key client.key


echo "去除客户端的key限制:"
\cp -f client.key client.key.org
openssl rsa -in client.key.org -out client.key -passout ${myPwd}
echo "去除完毕"

exit 0




