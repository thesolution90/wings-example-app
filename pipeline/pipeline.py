'''
Diese Datei beinhaltet die auszuführenden Schritte in der GitLab Pipeline
'''
import os
import argparse
from TrelloTask import TrelloTask
from TrelloException import TrelloException
from GitCommit import GitCommit
from GitLabCommit import GitLabCommit
from GitHubCommit import GitHubCommit

parser = argparse.ArgumentParser(
    prog='pipeline',
    description='Dieses Programm führt die Trello Integrationen für GitLab CI/CD aus')
parser.add_argument('--step', action='store', type=str, help='Name der auszuführenden Funktion')
args = parser.parse_args()

allowed_step_strings = [
    'pre_production',
    'post_production',
    'pre_feature_branch',
    'intra_feature_branch',
    'post_feature_branch'
]
if args.step not in allowed_step_strings:
    raise TrelloException('Nicht erlaubter Wert im Argument verwendet')

# Hier werden Instanzen von GitLabCommit und TrelloTask gebildet
source_system = GitCommit.check_source_system()
print(source_system)
git_commit = GitHubCommit() if source_system == 'Github' else GitLabCommit()
trello = TrelloTask(git_commit)

if args.step == allowed_step_strings[0]:
    # Vor der Ausführung der Production Pipeline
    trello.pre_production_pipeline()
elif args.step == allowed_step_strings[1]:
    # Nach der Ausführung der Production Pipeline
    IS_PIPELINE_FAILED = os.environ.get('PIPELINE_FAILED') == 'true'
    trello.post_production_pipeline(IS_PIPELINE_FAILED)
elif args.step == allowed_step_strings[2]:
    # Vor der Ausführung der Feature Branch Pipeline
    trello.pre_feature_branch_pipeline()
elif args.step == allowed_step_strings[3]:
    # Während der Ausführung der Feature Branch Pipeline
    trello.intra_feature_branch_pipeline()
elif args.step == allowed_step_strings[4]:
    # Nach der Ausführung der Feature Branch Pipeline
    IS_PIPELINE_FAILED = os.environ.get('PIPELINE_FAILED') == 'true'
    if os.environ.get('REVIEW_ACCEPTED') is not None \
    and os.environ.get('REVIEW_ACCEPTED').lower() in ['yes', 'true']:
        IS_REVIEW_FAILED = False
    else:
        IS_REVIEW_FAILED = True
    trello.post_feature_branch_pipeline(IS_REVIEW_FAILED, IS_PIPELINE_FAILED)
