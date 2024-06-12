'''
Diese Datei beinhaltet die Klasse GitCommit.
Sie ist die übergeordnete Klasse für alle Quellsysteme, die Git verwenden.
'''
import os
from GitException import GitException


class GitCommit:
    '''
    Diese Klasse beinhaltet die nötigen Informationen eines Git Commits,
    der für Workflow-Systeme eingesetzt wird. Diese Klasse ist nicht
    Quellsystem-spezifisch und wird als Elternklasse für die spezifischen
    Klassen von Gitlab und Github eingesetzt.

    Parameters:
        branch_name (str): Name des Git Branches des Commits
        commit_hash(str): Hashwert des Commits
        commit_message(str): Nachricht des Commits
        image_name(str): Name des Docker-Images für den Commit
        project_url(str): URL zu dem konkreten Projekt bei GitHub/Lab
        pipeline_id(str): ID der aktuellen CI/CD Pipeline
        pipeline_link_url(str): Link zur Pipeline bei GitHub/Lab
        commit_link_url(str): Link zum Commit bei GitHub/Lab
        test_report_link_url(str): Link zum Unittest Report bei GitHub/Lab
    '''
    def __init__(self, branch_name: str, commit_hash: str, commit_message: str,
                 image_name: str, project_url: str, pipeline_id: str, pipeline_link_url: str,
                 commit_link_url: str, test_report_link_url: str):
        self.branch_name = branch_name
        self.commit_hash = commit_hash
        self.commit_message = commit_message
        self.image_name = image_name
        self.project_url = project_url
        self.pipeline_id = pipeline_id
        self.pipeline_link_url = pipeline_link_url
        self.commit_link_url = commit_link_url
        self.test_report_link_url = test_report_link_url

    @staticmethod
    def check_source_system() -> str:
        '''
        Diese Funktion überprüft, ob es sich um GitLab oder GitHub handelt.
        '''
        if os.environ.get('GITHUB_ACTIONS') in ['true', True]:
            return 'Github'
        if os.environ.get('GITLAB_CI') in ['true', True]:
            return 'Gitlab'
        raise GitException('Source system not recognized.')

    def get_branch_name(self) -> str:
        '''
        Gibt den Namen des momentanen Branches zurück.
        '''
        return self.branch_name

    def get_commit_hash(self) -> str:
        '''
        Gibt den Hashwert des aktuellen Commits zurück.
        '''
        return self.commit_hash

    def get_commit_message(self) -> str:
        '''
        Gibt die Commit Nachricht zurück.
        '''
        return self.commit_message

    def get_image_name(self) -> str:
        '''
        Gibt den Namen des zukünftigen Docker Images zurück.
        '''
        return self.image_name

    def get_project_url(self) -> str:
        '''
        Gibt die URL zum GitLab Projekt (Repository) zurück
        '''
        return self.project_url

    def get_pipeline_id(self) -> str:
        '''
        Gibt die ID der aktuellen Pipeline zurück.
        '''
        return self.pipeline_id

    def get_pipeline_link_url(self) -> str:
        '''
        Gibt den Link zur aktuellen Pipeline zurück.
        '''
        return self.pipeline_link_url

    def get_commit_link_url(self) -> str:
        '''
        Gibt den Link zum aktuellen Commit zurück.
        '''
        return self.commit_link_url

    def get_test_report_link_url(self) -> str:
        '''
        Gibt den Link zum Unit Test Report zurück.
        '''
        return self.test_report_link_url
