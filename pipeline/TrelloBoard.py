'''
Diese Datei beinhaltet die Klasse TrelloBoard
'''
import json
import os
import requests
from TrelloException import TrelloException


class TrelloBoard:
    '''
    Diese Klasse beinhaltet alle Informationen und Verbindungen zu dem
    konkreten Trello Board, was verwendet wird.

    Parameters:
        board_id (str): Id des Trello Boards. Wird in den CI/CD
                        Variablen konfiguriert.
        api_key (str): API Key zur Authentifizierung
        api_token (str): API Token zur Authentifzierung
    '''
    def __init__(self, board_id: str = None, api_key: str = None, api_token: str = None):
        self.board_id = board_id if board_id is not None \
            else os.environ.get('TRELLO_BOARD_ID')
        self.api_key = api_key if api_key is not None \
            else os.environ.get('TRELLO_API_KEY')
        self.api_token = api_token if api_token is not None \
            else os.environ.get('TRELLO_API_TOKEN')
        self.board_lists = self.__query_lists_in_board()

    def get_board_lists(self) -> dict:
        '''
        Gibt alle Listen im Trello Board zurück.

        Returns:
            board_lists (dict): Name aller Boards zusammen mit ihren IDs als
                                Key-Value Paar
        '''
        return self.board_lists

    def query_trello_api(self, url: str, params: dict = None, method: str = 'GET',
                         file_blob: any = None, timeout: int = 10) -> dict:
        '''
        Wrapper für die GET API Requests an die Trello REST API
        '''
        headers = {
            "Accept": "application/json"
        }
        params = {} if params is None else params
        base_params = {
            'key': self.api_key,
            'token': self.api_token
        }
        final_params = {**params, **base_params}
        if file_blob is None:
            response = requests.request(
                method,
                url,
                headers=headers,
                params=final_params,
                timeout=timeout
            )
        else:
            response = requests.request(
                method,
                url,
                headers=headers,
                params=final_params,
                files=file_blob,
                timeout=timeout
            )
        if response.status_code != 200:
            error_message = f'''
            Status Code: {response.status_code}
            URL: {url}
            Params: {final_params}
            Response Text: {response.text}
            '''
            raise TrelloException(error_message)
        return json.loads(response.text)

    def __query_lists_in_board(self) -> dict:
        '''
        Diese Funktion gibt alle Listen inklusive der IDs innerhalb des
        Trello Boards zurück

        Returns:
            lists (dict): Dict aller Listen mit ID und Name
        '''
        url = f"https://api.trello.com/1/boards/{self.board_id}/lists"
        api_response = self.query_trello_api(url)
        result = {}
        for trello_list in api_response:
            result[trello_list['name']] = trello_list['id']
        return result
