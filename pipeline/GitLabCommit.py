'''
Diese Datei beinhaltet die Klasse GitLabCommit.
Sie wird verwendet, wenn als Revisionssystem GitLab verwendet wird.
'''
import os
import re
from GitCommit import GitCommit


class GitLabCommit(GitCommit):
    '''
    Die Klasse extrahiert alle Infomationen aus GitLab und erzeugt einen
    GitCommit. Der Konstruktor bezieht alle Informationen dafür spezifisch
    von GitLab Runnern.
    Diese werden aus den Umgebungsvariablen extrahiert und dem Verwender zur
    Verfügung gestellt.
    '''
    def __init__(self):
        gitlab_commit_message = os.environ.get('CI_COMMIT_MESSAGE')
        # Wenn Prod Pipeline
        if gitlab_commit_message and \
                "Merge branch '" in gitlab_commit_message:
            match = re.search(r"Merge branch '([^']*)'", gitlab_commit_message)
            if match:
                gitlab_branch_name = match.group(1)
        else:
            gitlab_branch_name = os.environ.get('CI_COMMIT_REF_NAME')
        gitlab_commit_hash = os.environ.get('CI_COMMIT_SHA')
        gitlab_image_name = os.environ.get('CI_REGISTRY_IMAGE')
        gitlab_project_url = os.environ.get('CI_PROJECT_URL')
        gitlab_pipeline_id = os.environ.get('CI_PIPELINE_ID')
        gitlab_pipeline_link_url = \
            f'{gitlab_project_url}/-/pipelines/{gitlab_pipeline_id}'
        gitlab_commit_link_url = \
            f'{gitlab_project_url}/-/commit/{gitlab_commit_hash}'
        gitlab_test_report_link_url = f'{gitlab_pipeline_link_url}/test_report'

        super().__init__(gitlab_branch_name, gitlab_commit_hash,
                         gitlab_commit_message, gitlab_image_name,
                         gitlab_project_url, gitlab_pipeline_id,
                         gitlab_pipeline_link_url, gitlab_commit_link_url,
                         gitlab_test_report_link_url)
