import requests
import json

NUMBER_OF_TOWERS = 3
TOKENS_FOR_DESTROYING_TOWER = 100
TOKENS_FOR_REMAINING_TOWER = 50
ELIXIR_SPENT_EVERY_SECOND = 0.357
TOKENS_FOR_SPENDING_ELIXIR = 1
UNDERESTIMATE_FOR_SAFETY = 0.95
MAX_TOKENS = 1000

class ApiAccesser:

    def __init__(self,developer_key,player_id_after_hashtag):
        self.total_tokens_gained = 0
        self.developer_key = developer_key
        self.player_id_after_hashtag = player_id_after_hashtag

    def last_battle_time(self):
        r=requests.get("https://api.clashroyale.com/v1/players/%23"+self.player_id_after_hashtag+"/battlelog", headers={"Accept":"application/json", "authorization": "Bearer "+self.developer_key})
        r_string = json.dumps(r.json())
        r_decoded = json.loads(r_string)
        print("getting time of last completed battle")
        return r_decoded[0]["battleTime"]

    def add_last_battle_season_tokens_to_total(self,time_of_battle):
        r=requests.get("https://api.clashroyale.com/v1/players/%23"+self.player_id_after_hashtag+"/battlelog", headers={"Accept":"application/json", "authorization": "Bearer "+self.developer_key})
        r_string = json.dumps(r.json())
        r_decoded = json.loads(r_string)
        tokens_for_destroying_towers = r_decoded[0]["team"][0]["crowns"]*TOKENS_FOR_DESTROYING_TOWER
        tokens_for_remaining_towers = (NUMBER_OF_TOWERS-r_decoded[0]["opponent"][0]["crowns"])*TOKENS_FOR_REMAINING_TOWER
        tokens_for_spending_elixir = time_of_battle*ELIXIR_SPENT_EVERY_SECOND*TOKENS_FOR_SPENDING_ELIXIR
        tokens_gained = round((tokens_for_destroying_towers+tokens_for_remaining_towers+tokens_for_spending_elixir)*UNDERESTIMATE_FOR_SAFETY)
        print("estimated "+str(tokens_gained)+" tokens gained")
        self.total_tokens_gained += tokens_gained

    def maximum_tokens_reached(self):
        return self.total_tokens_gained >= MAX_TOKENS