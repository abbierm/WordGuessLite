# Description
Wordle Clone via API calls using FastAPI. This is a "lite" version of my WordGuessAPI CS50x project and doesn't contain a frontend or any user/account management features.  WordguessLite is just the API with the async capabilities of FastAPI to help manage the current games inside of a cache.


# Quick Start

### Start a new game 

Send a GET request to the following endpoint

        api/start


- You will get a JSON response with a "game_token" key.  This token is used to access your game when making guesses. 

### Making a Guess

Send a POST request to the following endpoint

        api/guess

    
The request body needs to be a JSON with the "game_token" received from the start response and a 5 letter word "guess".

        {
            "game_token": "<token from start response>",
            "guess": "<5-letter guess>"
        }

If the response from the guess request is valid, the client will get returned a payload in the following format:

        {
            "game_token": "<token used to identify game>",
            "token_expiration": "<When the token/game expires>",
            "guess_count": "<Number of valid guesses the current game has>",
            "guesses": "{
                            "1": {
                                    "guess": "<user's 1st guess>",
                                    "feedback": "<feedback from guess>"
                                    },
                            "2": {
                                    "guess": "<user's 2nd guess>",
                                    "feedback": "<feedback from guess>"
                                },
                        }"
            "message": "<Error message if applicable>",
            "status": "True if game is still current or False if game is over.",
            "results": "won/lost or None if game is still current",
            "correct_word": "Displays ***** until game is over and will display correct word"
        }

An example guess response for a client's third guess might look like:

        {
            'game_token': 'e18dc0fab28b5a09', 
            'token_expiration': '2024-10-19T09:32:31.150852+00:00', 'guess_count': 3, 
            'guesses': 
                {
                    '1': {'guess': 'music', 'feedback': 'BBBGG'}, 
                    '2': {'guess': 'relic', 'feedback': 'BBBGG'}, 
                    '3': {'guess': 'toxic', 'feedback': 'BBBGG'}
                }, 
            'message': '', 
            'status': True, 
            'results': None, 
            'correct_word': '*****'
        }

Then using the same game as above, if the user's 4th guess was correct, the response will look like: 

        {
            'game_token': 'e18dc0fab28b5a09', 
            'token_expiration': '2024-10-19T09:32:31.150852+00:00',
            'guess_count': 4, 
            'guesses': {
                        '1': {'guess': 'music', 'feedback': 'BBBGG'}, 
                        '2': {'guess': 'relic', 'feedback': 'BBBGG'},
                        '3': {'guess': 'toxic', 'feedback': 'BBBGG'},
                        '4': {'guess': 'panic', 'feedback': 'GGGGG'}
                        }, 
            'message': '', 
            'status': False, 
            'results': 'won', 
            'correct_word': 'panic'
        }


# Local Deployment

### Requirements 


- Python 3.10 or newer
- FastAPI
- Uvicorn

>Note that if using pip, fastapi will install all of it's necessary dependencies like Pydantic. 



### Running WordGuessLite

Run the main.py file in the root directory with the following terminal command

    python main.py

OR using the fastapi development server by running the command:

    fastapi dev main.py