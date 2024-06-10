'''
Diese Datei beinhaltet die Klasse GitHubCommit.
Sie wird verwendet, wenn als Revisionssystem GitHub verwendet wird.
'''
import os
import re

class GitHubCommit:
    '''
    Die Klasse beinhaltet die relevanten Informationen eines jeden Git Commits.
    Diese werden aus den Umgebungsvariablen extrahiert und dem Verwender zur
    Verfügung gestellt.
    '''
    def __init__(self):
        commit_message = os.environ.get('GITHUB_REF_NAME')
        # Wenn Prod Pipeline
        if commit_message and "Merge branch '" in commit_message:
            match = re.search(r"Merge branch '([^']*)'", commit_message)
            if match:
                branch_name = match.group(1)
        else:
            branch_name = os.environ.get('GITHUB_REF_NAME')
        self.branch_name = branch_name
        self.commit_hash = os.environ.get('GITHUB_SHA')
        self.commit_message = os.environ.get('CI_COMMIT_MESSAGE')
        self.image_name = os.environ.get('CI_REGISTRY_IMAGE')
        self.project_url = os.environ.get('GITHUB_REPOSITORY') # + GITHUB_URL noch davor
        self.pipeline_id = os.environ.get('CI_PIPELINE_ID')
        
        GITHUB_REPOSITORY