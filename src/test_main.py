'''
Unit Tests für main.py
'''
import unittest
import time
from http import HTTPStatus
import requests
from src.main import ServerThread


class TestHTTPServer(unittest.TestCase):
    '''
    Test Cases für den Unit Test
    '''
    @classmethod
    def setUpClass(cls):
        cls.server_thread = ServerThread()
        cls.server_thread.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.server_thread.shutdown()
        cls.server_thread.join()

    def test_server_response(self):
        '''
        Checken ob Rückmeldung des Servers richtig ist
        '''
        response = requests.get('http://localhost:5000', timeout=10)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.content, b'Hallo Welt!')


if __name__ == '__main__':
    unittest.main()
