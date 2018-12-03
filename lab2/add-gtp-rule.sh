#!/usr/bin/env bash

APP_ID="trellis-tutorial"
ONOS_ADDR="127.0.0.1"
FLOW_REST_URL="http://${ONOS_ADDR}:8181/onos/v1/flows"
FLOW_FILE="gtp-flowrule.json"

(set -x; curl --fail -sSL --user onos:rocks --noproxy 127.0.0.1 -X POST \
    -H "Content-Type:application/json" "http://127.0.0.1:8181/onos/v1/flows?appId=${APP_ID}" \
    -d@${FLOW_FILE})
echo
