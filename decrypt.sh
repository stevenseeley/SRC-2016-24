#!/bin/sh
if [ "$#" -ne 1 ]; then
    echo "(!) Usage: $0 [hash]"
else
    java -classpath "infra_encryption.jar:oraclepki.jar:osdt_core.jar:osdt_cert.jar:commons-codec-1.3.jar" -DKEYSTORE_LOCATION="keystore" com.inquira.infra.security.OKResourceEncryption $1
fi
