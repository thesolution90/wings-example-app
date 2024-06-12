'''
Diese Datei beinhaltet alle nötigen Funktionen für die Integration
von Trello mit Gitlab CI/CD.
'''
from datetime import datetime
from GitCommit import GitCommit
from TrelloBoard import TrelloBoard
from TrelloException import TrelloException


class TrelloTask(TrelloBoard):
    '''
    Diese Klasse beinhaltet alle Funktionen die in den verschiedenen Pipeline
    Jobs aufgerufen werden können und damit dann der Status des passenden
    Tickets geändert werden kann.
    Damit dies funktioniert muss ein Ticket in dem Trello Board vorhanden sein,
    das den Namen des Branches beinhaltet und das "gitlab" Label hat.

            Parameters:
                    board_id (str): ID des Trello Boards
                    api_key (str): API Key des Trello Power Ups
                    api_token (str): API Token des Trello Benutzers
                    gitlab_branch_name (str): Name des aktuelle Gitlab Branches
                    gitlab_commit_hash (str): (voller) Commit Hash
                    gitlab_commit_message (str): Nachricht des Entwicklers
                                                 innerhalb des Commits
                    gitlab_pipeline_id (str): ID der Gitlab Pipeline
                    gitlab_project_url (str): URL zum Projekt in von Gitlab
                    gitlab_image_name (str): Name des Docker Images in Gitlab
    '''
    def __init__(self, git_commit: GitCommit):
        super().__init__()
        self.git_commit = git_commit
        self.task = self.__get_task()
        # Andere
        now = datetime.now()
        self.now = now.strftime("%d/%m/%Y %H:%M:%S")
        self.source_system = GitCommit.check_source_system()

    def __get_task(self):
        '''
        Auffinden der passenden und eindeutigen Karte im Trello Board

        Returns:
            task_info (dict): Informationen über die passende Karte
        '''
        # Suchen der passenden Karte
        url = "https://api.trello.com/1/search"
        query = {
            'query': self.git_commit.get_branch_name(),
            'partial': 'true',
            'modelTypes': 'cards',
            'idBoards': self.board_id
        }
        api_response = self.query_trello_api(url, query)
        # Prüfen der Karte auf Einmaligkeit
        print(query)
        print(api_response)
        if len(api_response['cards']) != 1:
            raise TrelloException('''Too many cards found. Need exactly one
            result. Check the unique and matching naming of branch and card.
            Aborting.''')
        task = api_response['cards'][0]
        # Prüfen auf das GitLab label
        for label in task['labels']:
            if label['name'] == 'git':
                git_label_existing = True
        if not git_label_existing:
            raise TrelloException('''The identified task has not the git label.
            Aborting.''')
        return {
            'task_id': task['id'],
            'list_id': task['idList']
        }

    def pre_feature_branch_pipeline(self):
        '''
        Diese Funktion wird aufgerufen wenn die Review Pipelines starten.
        Folgende Dinge passieren hier:
            - Card wird auf "In Development" verschoben
            - Link zum Commit wird in das Ticket geschrieben
            - Link zur Pipeline wird in das Ticket geschrieben
        '''
        self.__move_card_to('In Development')

        card_comment_text = f'''
        Automatisiert generierte Nachricht von {self.source_system} um {self.now}:
        - Für diesen Task ist ein [Commit]({self.git_commit.get_commit_link_url()}) auf dem Entwicklungsbranch eingegangen: `{self.git_commit.get_commit_message()}`
        - Der Task wird auf den Status "In Development" verschoben.
        - Die Pipeline für den Commit kann [hier]({self.git_commit.get_pipeline_link_url()}) eingesehen werden.
        '''
        self.__add_new_comment(card_comment_text)

    def intra_feature_branch_pipeline(self):
        '''
        Diese Funktion wird aufgerufen wenn die Review Umgebung in der Pipeline
        gestartet worden ist.
        Folgende Dinge passieren hier:
            - Card wird auf "In Review" verschoben
            - Status Meldung in das Ticket mit der Zeit und dem Link zum Review
              Bereich
        '''
        self.__move_card_to('In Review')

        with open('environment_url.txt', 'r', encoding='utf-8') as file:
            review_url = file.read()
        card_comment_text = f'''
        Automatisiert generierte Nachricht von {self.source_system} um {self.now}:
        - Für den [Commit]({self.git_commit.get_commit_link_url()}) `{self.git_commit.get_commit_message()}` ist die Review gestartet worden.
        - Der Task wird auf den Status "In Review" verschoben.
        - Die Review Instanz kann [hier]({review_url}) eingesehen werden.
        - Die Review muss [hier]({self.git_commit.get_pipeline_link_url()}) akzeptiert oder abgelehnt werden.
        - Die Ergebnisse der CI Tests finden sich im Anhang dieses Tasks.
        - Die Ergebnisse des Unit Tests findet sich [hier]({self.git_commit.get_test_report_link_url()})
        '''
        self.__add_new_comment(card_comment_text)

        # Kann wieder hinzugefügt werden wenn jobs in ci file aktiviert sind
        # self.__upload_attachment('gl-dependency-scanning-report.json')
        # self.__upload_attachment('gl-container-scanning-report.json')
        # self.__upload_attachment('gl-sbom-report.cdx.json')

    def post_feature_branch_pipeline(self, is_review_failed: bool,
                                     is_pipeline_failed: bool):
        '''
        Diese Funktion wird aufgerufen wenn die Review Pipelines enden.
        Folgende Dinge passieren hier:
            - Bei Erfolg:
                - Card wird auf "Ready to Deploy" geschoben
                - Link zum Commit und Pipeline werden in das Ticket geschrieben
                - Link zu Unit Test werden geschrieben
                - Artefakte werden als Anhänge in das Ticket geladen
            - Bei Ablehnung der Review und bei Fehlern in der Pipeline:
                - Card wird auf "In Development" geschoben
                - Fehlermeldung mit Commit wird eingetragen
        '''
        if is_pipeline_failed:
            self.__move_card_to('In Development')

            card_comment_text = f'''
            Automatisiert generierte Nachricht von {self.source_system} um {self.now}:
            - Für den [Commit]({self.git_commit.get_commit_link_url()}) `{self.git_commit.get_commit_message()}` gab es Fehler in der Pipeline.
            - Der Task wird auf den Status "In Development" verschoben.
            - Die Pipeline für den Commit kann [hier]({self.git_commit.get_pipeline_link_url()}) eingesehen werden.
            '''
            return self.__add_new_comment(card_comment_text)

        if not is_review_failed:
            self.__move_card_to('Ready to Deploy')

            card_comment_text = f'''
            Automatisiert generierte Nachricht von {self.source_system} um {self.now}:
            - Für den [Commit]({self.git_commit.get_commit_link_url()}) `{self.git_commit.get_commit_message()}` is der **Review akzeptiert** worden.
            - Der Task wird auf den Status "Ready to Deploy" verschoben.
            - Die Pipeline für den Commit kann [hier]({self.git_commit.get_pipeline_link_url()}) eingesehen werden.
            - Das fertige Docker Image hat den folgenden Namen: `{self.git_commit.get_image_name()}`
            **Der Feature Branch kann nun gemergt werden.**
            '''
            return self.__add_new_comment(card_comment_text)
        else:
            self.__move_card_to('In Development')

            card_comment_text = f'''
            Automatisiert generierte Nachricht von {self.source_system} um {self.now}:
            - Für den [Commit]({self.git_commit.get_commit_link_url()}) `{self.git_commit.get_commit_message()}` is der **Review nicht akzeptiert** worden.
            - Der Task wird auf den Status "In Development" verschoben.
            - Die Pipeline für den Commit kann [hier]({self.git_commit.get_pipeline_link_url()}) eingesehen werden.
            '''
            return self.__add_new_comment(card_comment_text)

    def pre_production_pipeline(self):
        '''
        Diese Funktion wird aufgerufen wenn die Production Pipelines starten.
        Folgende Dinge passieren hier:
            - Card with auf "Ready to Deploy" geschoben
            - Link zum Merge und Commit werden in das Ticket geschrieben
        '''
        self.__move_card_to('Ready to Deploy')

        card_comment_text = f'''
        Automatisiert generierte Nachricht von {self.source_system} um {self.now}:
        - Für diesen Task ist ein [Commit]({self.git_commit.get_commit_link_url()}) auf dem Hauptbranch eingegangen: ```{self.git_commit.get_commit_message()}```
        - Der Task wird auf den Status "Ready to deploy" verschoben.
        - Die Pipeline für den Commit kann [hier]({self.git_commit.get_pipeline_link_url()}) eingesehen werden.
        **Das Produktivsystem wird nun aktualisiert. Dies kann nicht unterbrochen werden**
        '''
        self.__add_new_comment(card_comment_text)

    def post_production_pipeline(self, is_failed: bool) -> None:
        '''
        Diese Funktion wird aufgerufen wenn die Review Pipelines starten.
        Folgende Dinge passieren hier:
            - Bei Fehlern in der Pipeline:
                - Card wird auf "In Development" geschoben
                - Fehlermeldung mit Commit wird eingetragen
            - Bei Erfolg:
                - Card wird auf "Deployed" geschoben
                - Link zum Commit und Pipeline werden in das Ticket geschrieben
        '''
        if not is_failed:
            self.__move_card_to('Deployed')

            card_comment_text = f'''
            Automatisiert generierte Nachricht von {self.source_system} um {self.now}:
            **Das Produktivsystem wurde erfolgreich aktualisiert.**
            - Die Pipeline für den Commit kann [hier]({self.git_commit.get_pipeline_link_url()}) eingesehen werden.
            - Das fertige Docker Image hat den folgenden Namen: `{self.git_commit.get_image_name()}`
            '''
            self.__add_new_comment(card_comment_text)
        else:
            self.__move_card_to('In Development')

            card_comment_text = f'''
            Automatisiert generierte Nachricht von {self.source_system} um {self.now}:
            **Das Produktivsystem konnte nicht aktualisiert werden.**
            - Bei dem [Commit]({self.git_commit.get_commit_link_url()}) `{self.git_commit.get_commit_message()}` ist ein Fehler aufgetreten.
            - Der Task wird auf den Status "In Development" verschoben.
            - Die Pipeline für den Commit kann [hier]({self.git_commit.get_pipeline_link_url()}) eingesehen werden.
            '''
            self.__add_new_comment(card_comment_text)

    def __add_new_comment(self, text: str):
        '''
        Mit dieser Funktion wird ein neuer Kommentar zu einer Card hinzugefügt.
        '''
        url = f'https://api.trello.com/1/cards/{self.task["task_id"]}/actions/comments'
        params = {
            'text': text.strip()
        }
        return self.query_trello_api(url, params, 'POST')

    def __move_card_to(self, list_name: str):
        '''
        Mit dieser Funktion wird die Karte in eine neue Spalte verschoben.
        '''
        url = f'https://api.trello.com/1/cards/{self.task["task_id"]}'
        params = {
            'idList': self.board_lists[list_name]
        }
        return self.query_trello_api(url, params, 'PUT')

    def __upload_attachment(self, file_path):
        '''
        Mit dieser Funktion werden Anhänge hochgeladen.
        '''
        url = f'https://api.trello.com/1/cards/{self.task["task_id"]}/attachments'
        files = {
            'file': open(file_path, 'rb')
        }
        return self.query_trello_api(url, None, 'POST', files)
