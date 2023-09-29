# NFL Live Score Tracker

Track your favorite team's score live* (or as close as you can). When running, this will check if your team is currently playing a game and check the score as often as you need. This can be then be used to send notifications to your favorite system.

## Requirements
- Python3+

## How to run
1. Clone this repo
2. `python -m venv venv`
3. `source ./venv/bin/activate`
4. `pip install -r requirements.txt`
5. `NFL_SCORE_TRACKER_MY_TEAM=DAL python main.py`

## APIs used
- http://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/:team
- https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/:team/schedule?season=:year
