import requests
import json
import exit_codes

NUMBER_OF_TOWERS = 3
TOKENS_FOR_DESTROYING_TOWER = 100
TOKENS_FOR_REMAINING_TOWER = 50
ELIXIR_SPENT_EVERY_SECOND = 0.357
TOKENS_FOR_SPENDING_ELIXIR = 1
UNDERESTIMATE_FOR_SAFETY = 0.95

class ApiAccesser:

    def __init__(self,developer_key,player_id_after_hashtag):
        self.developer_key = developer_key
        self.player_id_after_hashtag = player_id_after_hashtag

    def verify_api_is_working(self):
        print("testing API access")
        r=requests.get("https://api.clashroyale.com/v1/players/%23"+self.player_id_after_hashtag+"/battlelog", headers={"Accept":"application/json", "authorization": "Bearer "+self.developer_key})
        r_string = json.dumps(r.json())
        r_decoded = json.loads(r_string)
        try:
            last_battle = r_decoded[0]
            print("API access functional")
            return exit_codes.SUCCESS,None
        except:
            print("API access not functional")
            try:
                if "reason" in r_decoded.keys():
                    print("your developer key is likely invalid")
            except:
                print("your player id is likely invalid")
            finally:
                print('did you create a file called "private.py" and enter the necessary information? (see README)')
                return exit_codes.FATAL_ERROR,r_decoded



    def last_battle_time(self):
        print("checking time of last completed battle")
        r=requests.get("https://api.clashroyale.com/v1/players/%23"+self.player_id_after_hashtag+"/battlelog", headers={"Accept":"application/json", "authorization": "Bearer "+self.developer_key})
        r_string = json.dumps(r.json())
        r_decoded = json.loads(r_string)
        try:
            return r_decoded[0]["battleTime"]
        except:
            print("failed to access API")
            return exit_codes.FATAL_ERROR

    def report_battle_and_return_tokens_gained(self,time_of_battle,report_handler):
        r=requests.get("https://api.clashroyale.com/v1/players/%23"+self.player_id_after_hashtag+"/battlelog", headers={"Accept":"application/json", "authorization": "Bearer "+self.developer_key})
        r_string = json.dumps(r.json())
        r_decoded = json.loads(r_string)
        try:
            crowns = r_decoded[0]["team"][0]["crowns"]
            opponent_crowns = r_decoded[0]["opponent"][0]["crowns"]

            tokens_for_destroying_towers = crowns*TOKENS_FOR_DESTROYING_TOWER
            tokens_for_remaining_towers = (NUMBER_OF_TOWERS-opponent_crowns)*TOKENS_FOR_REMAINING_TOWER
            tokens_for_spending_elixir = time_of_battle*ELIXIR_SPENT_EVERY_SECOND*TOKENS_FOR_SPENDING_ELIXIR
            tokens_gained = round((tokens_for_destroying_towers+tokens_for_remaining_towers+tokens_for_spending_elixir)*UNDERESTIMATE_FOR_SAFETY)
            print("estimated "+str(tokens_gained)+" tokens gained")

            report_handler.log_battle(time_of_battle,crowns,opponent_crowns,tokens_gained)

            return tokens_gained
        except:
            return exit_codes.FATAL_ERROR