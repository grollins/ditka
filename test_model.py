import random
import pandas as pd
from load import player_df
from model import Team, Player, fill_remaining_spots



myteam = Team()
player_pool = player_df.copy()

print myteam.available_budget()

idx = random.choice(player_pool.query("cost > 90").index)
myteam.add_player( Player(player_pool.ix[idx]) )
player_pool.drop(idx, inplace=True)

print myteam.available_budget()

idx = random.choice(player_pool.query("(cost > 40) & (position == 'RB')").index)
myteam.add_player( Player(player_pool.ix[idx]) )
player_pool.drop(idx, inplace=True)

print myteam.available_budget()

idx = random.choice(player_pool.query("(cost > 40) & (position == 'WR')").index)
myteam.add_player( Player(player_pool.ix[idx]) )
player_pool.drop(idx, inplace=True)

print myteam
print myteam.available_budget()
