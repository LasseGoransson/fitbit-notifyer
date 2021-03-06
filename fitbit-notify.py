import fitbit
from pushover import Client
import time
import schedule
import yaml

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)


def getMissingSteps(authd_client):
    current_steps = authd_client.activities()["summary"]["steps"]
    goal_steps = authd_client.activities()["goals"]["steps"]
    return goal_steps-current_steps

def formatMsg(missingSteps):
    return f'Du mangler kun {missingSteps:d} skridt!'

def refresh_cb(token_dict):
    """Function for refreshing access_token, refresh_token, and expires_at."""
    global cfg
    cfg['fitbit_tokens']['access_token'] = token_dict['access_token']
    cfg['fitbit_tokens']['expires_at'] = str(token_dict['expires_at'])
    cfg['fitbit_tokens']['refresh_token'] = token_dict['refresh_token']

    with open(r'config.yml', 'w') as file:
        documents = yaml.dump(cfg, file)

    return token_dict


def notify(cfg):


    fitbit_tokens = cfg['fitbit_tokens']
    pushover_tokens = cfg['pushover_tokens']

    po = Client(pushover_tokens['id'], api_token=pushover_tokens['api_token'])

    authd_client = fitbit.Fitbit(fitbit_tokens['client'], fitbit_tokens['secret'],access_token=fitbit_tokens['access_token'], refresh_token=fitbit_tokens['refresh_token'])

    po.send_message(formatMsg(getMissingSteps(authd_client)), title="FitBit")

schedule.every().day.at("20:00").do(notify)
#schedule.every(1).hours.do(notify, cfg=cfg)

notify(cfg)
while True:
    # run_pending
    schedule.run_pending()
    time.sleep(1)
