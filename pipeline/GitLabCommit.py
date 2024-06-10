'''
Diese Datei beinhaltet die Klasse GitLabCommit.
Sie wird verwendet, wenn als Revisionssystem GitLab verwendet wird.
'''
import os
import re

class GitLabCommit:
    '''
    Die Klasse beinhaltet die relevanten Informationen eines jeden Git Commits.
    Diese werden aus den Umgebungsvariablen extrahiert und dem Verwender zur
    Verfügung gestellt.
    '''
    def __init__(self):
        commit_message = os.environ.get('CI_COMMIT_MESSAGE')
        # Wenn Prod Pipeline
        if commit_message and "Merge branch '" in commit_message:
            match = re.search(r"Merge branch '([^']*)'", commit_message)
            if match:
                gitlab_branch_name = match.group(1)
        else:
            gitlab_branch_name = os.environ.get('CI_COMMIT_REF_NAME')
        self.gitlab_branch_name = gitlab_branch_name
        self.gitlab_commit_hash = os.environ.get('CI_COMMIT_SHA')
        self.gitlab_commit_message = os.environ.get('CI_COMMIT_MESSAGE')
        self.gitlab_image_name = os.environ.get('CI_REGISTRY_IMAGE')
        self.gitlab_project_url = os.environ.get('CI_PROJECT_URL')
        self.gitlab_pipeline_id = os.environ.get('CI_PIPELINE_ID')

    def get_branch_name(self):
        '''
        Gibt den Namen des momentanen Branches zurück.
        '''
        return self.gitlab_branch_name

    def get_commit_hash(self):
        '''
        Gibt den Hashwert des aktuellen Commits zurück.
        '''
        return self.gitlab_commit_hash

    def get_commit_message(self):
        '''
        Gibt die Commit Nachricht zurück.
        '''
        return self.gitlab_commit_message

    def get_image_name(self):
        '''
        Gibt den Namen des zukünftigen Docker Images zurück.
        '''
        return self.gitlab_image_name

    def get_project_url(self):
        '''
        Gibt die URL zum GitLab Projekt (Repository) zurück
        '''
        return self.gitlab_project_url

    def get_pipeline_id(self):
        '''
        Gibt die ID der aktuellen Pipeline zurück.
        '''
        return self.get_pipeline_id

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
