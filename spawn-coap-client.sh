#!/bin/sh
## coap client bot
## sends data (int) to a coap uri

COAPURI=coap://edgex/a1r/d1/int

while [ True ];
do
  VAR=$((1 + RANDOM %10))
  coap-client -v9 -m post -t 0 -e $VAR $COAPURI
  sleep 5
done
