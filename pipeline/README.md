# Pipeline Trello Integration

## Vorarbeit

1. Ein Trello Board muss erstellt sein. Die ID davon muss bekannt sein. Diese wird in den GitLab CI/CD Variablen eingetragen (Name: `TRELLO_BOARD_ID`).
2. Ein PowerUp muss in Trello erstellt werden und mit dem Board verbunden werden. Der angezeigt API Key wird in die CI/CD Variablen in GitLab eingetragen (Name: `TRELLO_API_KEY`).
3. Der User muss einen API Token erstellen und in die CI/CD Variablen in GitLab eintragen (Name: `TRELLO_API_TOKEN`)
4. Das Board muss mindestens die folgenden Spalten in der exakt gleichen Benamung haben: `In Development`, `In Review`, `Ready to Deploy`, `Deployed`. Es muss ein Label mit dem Namen `gitlab` existieren.
5. Es kann nun eine Karte erstellt werden. Der Titel muss den Namen den zukünftigen Feature Branches beinhalten. Die Karte muss mit den Label "gitlab" versehen werden. Der Name des Feature Branches darf nur einmalig in dem Board vorkommen. Bei Duplikaten bricht das Programm ab.

## Schritte innerhalb der Feature Branch Pipelines

### Vor Ausführung der eigentlichen Pipeline

- Task wird auf den Status "In Developement" gestellt
- Ein Kommentar mit Links zum Commit und zur Pipeline wird angelegt

### Nachdem die Review Umgebung erstellt worden ist

- Task wird auf den Status "In Review" gestellt
- Es werden alle Artefakte aus der Code Prüfung hochgeladen
- Ein Kommentar mit Links zum Commit, Pipeline und Review Umgebung wird angelegt

### Zwischenschritt der Review

Nun muss ein Mitarbeiter der Q&A die Applikation testen. Sobald dies gemacht ist ruft er die Pipeline mit dem Job "Stop Review" auf. Diesen muss er manuell starten. Er trägt sein Ergebnis in den Startbildschirm des Jobs ein. Dies ist eine Variable mit dem Namen `ACCEPTED`. Diese kann er mit dem Wert "Yes" oder "No" belegen und damit angeben ob die Review akzeptiert ist oder nicht.

### Am Schluss der Pipeline

Es wird der Wert der Variable "ACCEPTED" aus dem Vorschritt gelesen.
Falls die Review akzeptiert ist:
- Task wird auf "Ready to Deploy" verschoben
- Es wird eine Erfolgsnachricht als Kommentar an den Task angehängt.
Falls die Review nicht akzeptiert ist:
- Task wird auf "In Development" verschoben
- Ein Kommentar dazu wird in den Task geladen
Schlussendlich werden die beteiligten Personen per Mail informiert.

### Falls die Pipeline fehlerhaft war

Sobald ein Fehler in der gesamten Pipeline auftritt passiert das Folgende:
- Task wird auf "In Development" verschoben
- Ein Kommentar zum Abbruch wird dazu in den Task geschrieben
Schlussendlich werden die beteiligten Personen per Mail informiert.

## Schritte innerhalb der Production Pipeline

Nachdem ein Merge Request erzeugt und akzeptiert worden ist läuft die Pipeline an, damit auf Production deployed werden kann.

### Vor der Ausführung der eigenlichen Pipeline

- Task wird auf den Status "Ready to Deploy" gestellt. Dies sollte eigentlich redundant sein
- Ein Kommentar mit Links zum Commit, Pipeline und Review Umgebung wird angelegt

### Nach der Ausführung der eigentlichen Pipeline

- Task wird auf "Deployed" geschoben
- Eine Erfolgsnachricht wird als Kommentar an den Task angehängt
Schlussendlich werden die beteiligten Personen per Mail informiert.

### Falls die Pipeline fehlerhaft war

Sobald ein Fehler in der gesamten Pipeline auftritt passiert das Folgende:
- Task wird auf "In Development" verschoben
- Ein Kommentar zum Abbruch wird dazu in den Task geschrieben
Schlussendlich werden die beteiligten Personen per Mail informiert.

## Aufruf und Ausführung

Die Funktionen für die Operationen auf dem Task sind in der Klasse `TrelloBoard` in der Datei `trello.py`.
Die Klasse benötigt die folgenden (Umgebungs-)Variablen zur Initialisierung:
| Variablenname | Bedeutung | GitLab Umgebungsvariable |
|----|----|----|
| board_id | ID des Trello Boards | `TRELLO_BOARD_ID` |
| api_key | API Key des Trello PowerUps | `TRELLO_API_KEY` |
| api_token | API Token des Trello Nutzers | `TRELLO_API_TOKEN` |
| gitlab_branch_name | Aktueller Branch im Git Repository | `CI_COMMIT_REF_NAME` |
| gitlab_commit_hash | (langer) Commit Hash im Git Repository | `CI_COMMIT_SHA` |
| gitlab_commit_message | Nachricht innerhalb des Commits | `CI_COMMIT_MESSAGE` |
| gitlab_pipeline_id | ID der Pipeline in GitLab | `CI_PIPELINE_ID` |
| gitlab_project_url | URL zum Repository in GitLab | `CI_PROJECT_URL` |
| gitlab_image_name | Name des Docker Images in der GitLab Registry | `CI_REGISTRY_IMAGE` |

Die folgenden Befehle werden zur Ausführung verwendet:
* Vor der Feature Branch Pipeline
```
pip3 install requests
python3 pipeline.py --step pre_feature_branch
```
* Nachdem die Review Umgebung in der Feature Branch Pipeline erstellt worden ist
```
pip3 install requests
python3 pipeline.py --step intra_feature_branch
```
* Nach der Feature Branch Pipeline
```
pip3 install requests
python3 pipeline.py --step post_feature_branch
```
* Vor der Production Pipeline
```
pip3 install requests
python3 pipeline.py --step pre_production
```
* Nach der Production Pipeline
```
pip3 install requests
python3 pipeline.py --step post_production
```

## Implementierung in der Pipeline

Die eigentlichen Jobs in der Pipeline sind als Templates in der `trello-ci.yaml` Datei hinterlegt.

## TODOs
- Image Name implementieren
- Prod Pipeline testen
- Anhänge implementieren
