'''
Diese Datei beinhaltet die Klasse GitHubCommit.
Sie wird verwendet, wenn als Revisionssystem GitHub verwendet wird.
'''
import os
from GitCommit import GitCommit

class GitHubCommit(GitCommit):
    '''
    Die Klasse beinhaltet die relevanten Informationen eines jeden Git Commits.
    Diese werden aus den Umgebungsvariablen extrahiert und dem Verwender zur
    Verfügung gestellt.
    '''
    def __init__(self):
        github_commit_message = os.environ.get('GH_COMMIT_MESSAGE')
        github_commit_hash = os.environ.get('GH_COMMIT_HASH')
        github_commit_link_url = os.environ.get('GH_COMMIT_LINK_URL')
        github_branch_name = os.environ.get('GITHUB_REF_NAME')
        github_full_name = os.environ.get('GH_FULL_NAME')
        github_image_name = f'{github_full_name}:{github_commit_hash}'
        github_project_url = os.environ.get('GH_PROJECT_URL')
        github_pipeline_id = os.environ.get('GITHUB_RUN_ID')
        github_pipeline_link_url = f'{github_project_url}/actions/runs/{github_pipeline_id}'
        github_test_report_link_url = github_pipeline_link_url

        super().__init__(github_branch_name, github_commit_hash, github_commit_message,
            github_image_name, github_project_url, github_pipeline_id, github_pipeline_link_url,
            github_commit_link_url, github_test_report_link_url)
