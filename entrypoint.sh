#!/usr/bin/sh

if [ -f 'cert/.docker' ]
then
	echo '\e[31mWARNING: USING DEFAULT SELF SIGNED CERTIFICATE\e[0m'
	echo '\e[33mDid you forget to mount your cert directory? The certificate included with this\e[0m'
	echo '\e[33mimage is public and should be considered compromised.\e[0m'
fi

uwsgi --master --https 0.0.0.0:8443,cert/public.crt,cert/private.key --wsgi-file ./app.py --need-app
