'''
Diese Datei beinhaltet die Klasse GitCommit.
Sie ist die übergeordnete Klasse für alle Quellsysteme, die Git verwenden.
'''
import os
from GitException import GitException

class GitCommit:
    def __init__(self, branch_name, commit_hash, commit_message,
        image_name, project_url, pipeline_id, pipeline_link_url,
        commit_link_url, test_report_link_url, codequality_report_link_url):
        self.branch_name = branch_name
        self.commit_hash = commit_hash
        self.commit_message = commit_message
        self.image_name = image_name
        self.project_url = project_url
        self.pipeline_id = pipeline_id
        self.pipeline_link_url = pipeline_link_url
        self.commit_link_url = commit_link_url
        self.test_report_link_url = test_report_link_url
        self.codequality_report_link_url = codequality_report_link_url

    @staticmethod
    def check_source_system():
        '''
        Diese Funktion überprüft, ob es sich um GitLab oder GitHub handelt.
        '''
        if os.environ.get('GITHUB_ACTIONS') in ['true', True]:
            return 'github'
        elif os.environ.get('GITLAB_CI') in ['true', True]:
            return 'gitlab'
        else:
            raise GitException('Source system not recognized.')

    def get_branch_name(self):
        '''
        Gibt den Namen des momentanen Branches zurück.
        '''
        return self.branch_name

    def get_commit_hash(self):
        '''
        Gibt den Hashwert des aktuellen Commits zurück.
        '''
        return self.commit_hash

    def get_commit_message(self):
        '''
        Gibt die Commit Nachricht zurück.
        '''
        return self.commit_message

    def get_image_name(self):
        '''
        Gibt den Namen des zukünftigen Docker Images zurück.
        '''
        return self.image_name

    def get_project_url(self):
        '''
        Gibt die URL zum GitLab Projekt (Repository) zurück
        '''
        return self.project_url

    def get_pipeline_id(self):
        '''
        Gibt die ID der aktuellen Pipeline zurück.
        '''
        return self.pipeline_id

    def get_pipeline_link_url(self):
        '''
        Gibt den Link zur aktuellen Pipeline zurück.
        '''
        return f'{self.gitlab_project_url}/-/pipelines/{self.get_pipeline_id}'

    def get_commit_link_url(self):
        '''
        Gibt den Link zum aktuellen Commit zurück.
        '''
        return f'{self.gitlab_project_url}/-/commit/{self.gitlab_commit_hash}'

    def get_test_report_link_url(self):
        '''
        Gibt den Link zum Unit Test Report zurück.
        '''
        return f'{self.get_pipeline_link_url()}/test_report'

    def get_codequality_report_link_url(self):
        '''
        Gibt den Link zum Codequalitäts Report zurück.
        '''
        return f'{self.get_pipeline_link_url()}/codequality_report'