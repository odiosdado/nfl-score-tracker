import requests
import json
from datetime import datetime
import time
import os

DEMO_MODE=False
API_BASE_URL="https://site.api.espn.com/apis/site/v2/sports/football/nfl"
CURRENT_SEASON=datetime.now().year
SCORE_CHECK_INTERVAL_SEC=5

def get_team_schedule(team):
    print(f'Getting data for team: {team}')
    if DEMO_MODE:
        f = open('demo-schedule.json')
        return json.load(f)
    schedule_url = f"{API_BASE_URL}/teams/{team}/schedule?season={CURRENT_SEASON}"
    print(schedule_url)
    try:
        response = requests.get(schedule_url)
        data = response.json()
        if 'code' in data:
            raise Exception(data)
        return data
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

def get_live_competition(events):
    for e in events:
        competition = e['competitions'][0] # only ony competition per live event in NFL
        status = competition['status']
        if status['type']['name'] == "STATUS_IN_PROGRESS":
        # test only!
        # if status_type['name'] == 'STATUS_SCHEDULED' and status_type['completed'] == True:
            return competition
    return None

def get_current_score(my_team_id, competition):
    score = {}
    for c in competition['competitors']:
        if c['id'] == my_team_id:
            score['my_team'] = c['score']['value']
        else:
            score['opposing_team'] = c['score']['value']
    return score

# main
if os.environ.get('NFL_SCORE_TRACKER_MY_TEAM') is None:
    print("""
Error: NFL_SCORE_TRACKER_MY_TEAM environment is required. 
Example: NFL_SCORE_TRACKER_MY_TEAM=DAL python main.py
""")
    exit(1)

while True:
    my_team = os.environ.get('NFL_SCORE_TRACKER_MY_TEAM')
    schedule = get_team_schedule(my_team)
    if schedule is None:
        print(f"Error: No schedule found for {my_team}")
        exit(1)
    my_team_name = schedule['team']['name']
    my_team_id = schedule['team']['id']
    print(f"my_team_id: {my_team_id} my_team_name: {my_team_name}")
    score = { 
        "my_team": 0, 
        "opposing_team": 0
    }
    competition = get_live_competition(schedule['events'])
    if competition != None:
        current_score = get_current_score(my_team_id, competition)
        print(f"score: {score} current_score: {current_score}")
        if score != current_score:
            print("Score has changed!")
        else:
            print("Noone has scored.")
    else:
        print("No live games")
    print(f"Sleeping for {SCORE_CHECK_INTERVAL_SEC} sec(s).")
    time.sleep(SCORE_CHECK_INTERVAL_SEC)