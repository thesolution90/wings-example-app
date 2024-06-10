# Wings Example App

## Applikation

Diese Applikation ist ein minimaler Webserver der nur die Worte "Hello World" zurückgibt. Der Source Code befindet sich in dieser Datei: `src/main.py`.
Der Server kann mit folgendem Befehl gestartet werden:
```
python3 src/main.py
```
So lässt sich mit der Applikation aus einer Shell kommunizieren:
```
curl localhost:5000/
```

Damit dieser Service einfach deployed werden kann wird dieser zusätzlich in einem Docker Image verpackt. Dazu findet sich eine `Dockerfile` in dem Hauptverzeichnis dieses Repositories.

## Zielsystem

Das Zielsystem ist ein minimales Kubernetes Cluster (Minikube). Die Verbindung dazu findet sich in der Datei `.gitlab/agents/minikube/config.yaml`. Dazu muss noch innerhalb der Kubernetes Clusters ein GitLab Agent installiert sein. Dieser lässt sich folgendermaßen installieren:
```
minikube start
```
```
helm upgrade --install gitlab-agent gitlab/gitlab-agent \
    --namespace gitlab-agent \
    --create-namespace \
    --set config.token=blubbi \
    --set config.kasAddress=wss://kas.gitlab.com
```

## Unit Test

Unit Tests sind in der Datei `src/test_main.py` definiert. Zusätzlich sind für pytest die Konfigurationen in der Datei `pytest.ini` angegeben.

## CI/CD

Für CI/CD wird hauptsächlich das Auto DevOps System von GitLab verwendet. Zusätzlich findet sich die gesamte Integration mit Trello im `pipeline/` Verzeichnis. Dazu existiert auch eine weitere [README](./pipeline/README.md).

## Prozesses

Diese finden sich im `bpmn/` Verzeichnis.
