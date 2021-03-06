import os 
import json 
import sys 
import requests 
import webbrowser 
import logging

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
info_dir = os.path.join(base_dir, 'info')
sys.path.append(base_dir) 

from helpers import others_help, api_help, decorators

logger = logging.getLogger('main_logger')
d_logger = logging.getLogger('display_logger')

@decorators.main_logger('spotify_setup.py')
def initial_request(client_info=None, redirect_uri=None, scope=None): 
    """
    Makes initial endpoint request for auth token -- note that this initial authorization is different from the other endpoint auth (so api_help.requests_general not used)
    Accepts string params of client id, redirect url, scope 
    Returns auth_code if successful else None 
    """

    if not all([client_info, redirect_uri, scope]):
        raise Exception('Invalid params for initial_request()')

    client_id, _ = client_info 
    response_type = 'code' 
    endpoint = f'https://accounts.spotify.com/authorize?client_id={client_id}&response_type={response_type}&redirect_uri={redirect_uri}&scope={scope}'
    
    webbrowser.open(endpoint) 

    response = str(input('Please enter redirect url AFTER response: '))

    if not response: 
        raise Exception('No response for redirect url request.')
    
    try: 
        responses = response.split('?')
        first = responses[1]
        first = first[first.index('=')+1:]
        auth_code = first.split('#')[0]

        if first[0] == 'error': 
            raise Exception('User did not authorize or something went wrong.')
        
        return auth_code 

    except: 
        raise Exception('Error during redirect url parsing.')

@decorators.main_logger('spotify_setup.py')
def main(): 
    """
    Handles all initial setup 
    No params
    Returns True if Successful else None  
    """

    client_info = api_help.get_auth() 
    redirect_uri = 'https://www.google.com/' # must be set in app dashboard, set to harmless uri -- NOT SPOTIFY FOR ME B/C SPOTIFY UNAVAILABLE IN KOREA
    scope = 'playlist-modify-public'

    if not client_info: 
        raise Exception("Invalid client info. Check 'spotify-client.json'")

    auth_code = initial_request(client_info, redirect_uri, scope)

    if not auth_code: 
        raise Exception("Error with initial_request()")

    auth_pst = api_help.auth_post(client_info, redirect_uri, auth_code)

    if not auth_pst: 
        raise Exception("Error with auth_post()")
        
    others_help.print_contents('INITIAL SETUP SUCCESS.')

    return True 

if __name__ == "__main__": 
    main() 