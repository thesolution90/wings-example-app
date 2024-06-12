'''
Diese Datei beinhaltet die auszuführenden Schritte in der GitLab Pipeline
'''
import os
import argparse
from sys import exit
from TrelloTask import TrelloTask
from TrelloException import TrelloException
from GitCommit import GitCommit
from GitLabCommit import GitLabCommit
from GitHubCommit import GitHubCommit

parser = argparse.ArgumentParser(
    prog='pipeline',
    description='Dieses Programm ruft die Git und Trello Integration auf')
parser.add_argument('--step', action='store', type=str, help='CI Schritt')
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
git_commit = GitHubCommit() if source_system == 'Github' else None
git_commit = GitLabCommit() if source_system == 'Gitlab' else git_commit
trello = TrelloTask(git_commit)

# Vor der Ausführung der Production Pipeline
if args.step == allowed_step_strings[0]:
    trello.pre_production_pipeline()
    exit(0)

# Nach der Ausführung der Production Pipeline
if args.step == allowed_step_strings[1]:
    IS_PIPELINE_FAILED = os.environ.get('PIPELINE_FAILED') == 'true'
    trello.post_production_pipeline(IS_PIPELINE_FAILED)
    exit(0)

# Vor der Ausführung der Feature Branch Pipeline
if args.step == allowed_step_strings[2]:
    trello.pre_feature_branch_pipeline()
    exit(0)

# Während der Ausführung der Feature Branch Pipeline
if args.step == allowed_step_strings[3]:
    trello.intra_feature_branch_pipeline()
    exit(0)

# Nach der Ausführung der Feature Branch Pipeline
if args.step == allowed_step_strings[4]:
    IS_PIPELINE_FAILED = os.environ.get('PIPELINE_FAILED') == 'true'
    if os.environ.get('REVIEW_ACCEPTED') is not None \
            and os.environ.get('REVIEW_ACCEPTED').lower() in ['yes', 'true']:
        IS_REVIEW_FAILED = False
    else:
        IS_REVIEW_FAILED = True
    trello.post_feature_branch_pipeline(IS_REVIEW_FAILED, IS_PIPELINE_FAILED)
    exit(0)
