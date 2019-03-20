import cassiopeia as cass
from cassiopeia import Champion, Champions
from cassiopeia import Summoner

from config import API_KEY
cass.set_riot_api_key(API_KEY)  # This overrides the value set in your configuration/settings.
cass.set_default_region("NA")


#champions = Champions(region="NA")
#for champion in champions:
#    print(champion.name, champion.id)
#
## annie = Champion(name="Annie", region="NA")
#annie = Champion(name="Annie", region="NA")
#print(annie.name)
#print(annie.title)
#for spell in annie.spells:
#    print(spell.name, spell.keywords)
#
#print(annie.info.difficulty)
#print(annie.passive.name)
#print({item.name: count for item, count in annie.recommended_itemsets[0].item_sets[0].items.items()})
##print(annie.free_to_play)
#print(annie._Ghost__all_loaded)
#
# ziggs = cass.get_champion(region="NA", "Ziggs")
#ziggs = cass.get_champion("Ziggs", region="NA")
#print(ziggs.name)
#print(ziggs.region)
#print({item.name: count for item, count in ziggs.recommended_itemsets[0].item_sets[0].items.items()})
##print(ziggs.free_to_play)
#for spell in ziggs.spells:
#    for var in spell.variables:
#        print(spell.name, var)
#print(ziggs._Ghost__all_loaded)
#

def print_summoner(name: str, region: str):
    summoner = Summoner(name=name, region=region)
    return summoner
    #print("Name:", summoner.name)
    #print("ID:", summoner.id)
    #print("Account ID:", summoner.account_id)
    #print("Level:", summoner.level)
    #print("Revision date:", summoner.revision_date)
    #print("Profile icon ID:", summoner.profile_icon.id)
    #print("Profile icon name:", summoner.profile_icon.name)
    #print("Profile icon URL:", summoner.profile_icon.url)
    #print("Profile icon image:", summoner.profile_icon.image)


if __name__ == "__main__":
    a = print_summoner("MegaManMusic", "NA")
    print(a)
