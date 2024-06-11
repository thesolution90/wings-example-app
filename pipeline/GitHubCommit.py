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

        github_commit_message = os.system('echo "${{ github.event.head_commit.message }}"')
        github_commit_hash = os.system('echo "${{ github.event.head_commit.id }}"')
        github_commit_link_url = os.system(os.system('echo "${{ github.event.head_commit.url }}"'))
        github_branch_name = os.environ.get('GITHUB_REF_NAME')
        github_full_name = os.system('echo "${{ github.repository.full_name }}"')
        github_image_name = f'{github_full_name}/{github_commit_hash}'
        github_project_url = os.system(os.system('echo "${{ github.repository.html_url }}"'))
        github_pipeline_id = os.environ.get('GITHUB_RUN_ID')
        github_pipeline_link_url = f'{github_project_url}/actions/runs/{github_pipeline_id}'
        github_test_report_link_url = 'placeholder_string'
        github_codequality_report_link_url = 'placeholder_string'

        super().__init__(github_branch_name, github_commit_hash, github_commit_message,
            github_image_name, github_project_url, github_pipeline_id, github_pipeline_link_url,
            github_commit_link_url, github_test_report_link_url, github_codequality_report_link_url)
