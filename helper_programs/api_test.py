import sys
sys.path.insert(0, 'clash_royale_auto_battler/')
import api_accesser
import private

api = api_accesser.ApiAccesser(private.developer_key,private.player_id_after_hashtag)
print(api.verify_api_is_working())