#!/bin/bash

NAMESPACE="wings-app"
SERVICE_NAME="wings-example-app"
LOCAL_PORT=5000
REMOTE_PORT=5000

# Funktion zum Beenden der Port-Forwarding-Verbindung
cleanup() {
  echo "Beende Port-Forwarding..."
  kill $PORT_FORWARD_PID
  wait $PORT_FORWARD_PID 2>/dev/null
  echo "Port-Forwarding beendet."
}

echo "Starte Port-Forwarding von ${LOCAL_PORT} zu ${SERVICE_NAME}:${REMOTE_PORT}..."
kubectl port-forward svc/${SERVICE_NAME} ${LOCAL_PORT}:${REMOTE_PORT} --namespace ${NAMESPACE} &
PORT_FORWARD_PID=$!

sleep 5

if ps -p $PORT_FORWARD_PID > /dev/null
then
  echo "Port-Forwarding läuft."

  CURL_RESPONSE=$(curl -s -w "\nHTTP-Status: %{http_code}\n" http://localhost:${LOCAL_PORT})
  
  echo "Antwort von curl:"
  echo "$CURL_RESPONSE"

  cleanup
else
  echo "Port-Forwarding fehlgeschlagen."
  exit 1
fi