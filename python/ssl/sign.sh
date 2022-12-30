#!/bin/bash
#auth: 1823218990@qq.com
#time: 2022-12-29

curdir=$(dirname $0)
curpath=$(pwd $curdir)
cd $curpath

myPwd="pass:123456"

CSR=$1

if [ $# -ne 1 ];then
    echo "Usage: sign.sh xxx.csr;"
    exit 1
fi
if [ ! -f $CSR ];then
    echo ".csr not found: $CSR;"
    exit 1
fi
cd $(dirname $CSR)

pwd
case $CSR in 
    *.csr ) CERT="`echo $CSR | sed -e 's/\.csr/\.crt/'`" ;;
	*) CERT="$CSR.crt" ;;
esac

cd $(dirname $CSR)


# make sure environment exists
if [ ! -d ca.db.certs ];then
    mkdir ca.db.certs
fi
if [ ! -f ca.db.serial ];then
    echo '01' > ca.db.serial
fi
if [ ! -f ca.db.index ];then
    cp /dev/null ca.db.index
fi


# create an own SSLeay config


#\cp ${curpath}/../req.cnf ./req.cnf
#sed -i "s/curpath/\./g" ./req.cnf

echo "curpath: $curpath"
# sign the certificate
echo "CA signing: $CSR -> $CERT:"
openssl ca -config req.cnf -out $CERT -infiles $CSR --passin ${myPwd}
echo "CA verifying: $CERT <-> CA cert"
openssl verify -CAfile ./ca.crt $CERT

# cleanup after SSLeay
rm -f req.cnf
rm -f ca.db.serial.old
rm -f ca.db.index.old

# die gracefully
exit 0


