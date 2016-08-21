import random
from scipy.stats import kendalltau
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="darkgrid")
from load import player_df
from model import Team, Player, fill_remaining_spots

# print player_df.query("(cost >= 35) & (cost <= 45) & (position == 'WR')")
# print player_df.ix[player_df.query("(cost > 5) & (position == 'DEF')").index]
# raise

def strategy1(myteam, player_pool):
    # expensive QB strategy
    idx = random.choice(player_pool.query("cost > 90").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    return myteam, player_pool

def strategy2(myteam, player_pool):
    # Expensive RB strategy
    idx = random.choice(player_pool.query("(cost > 40) & (position == 'RB')").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    return myteam, player_pool

def strategy3(myteam, player_pool):
    # Expensive QB + RB strategy
    idx = random.choice(player_pool.query("cost > 90").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    idx = random.choice(player_pool.query("(cost > 40) & (position == 'RB')").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    return myteam, player_pool

def strategy4(myteam, player_pool):
    # Expensive QB + bunch of DEFs
    idx = random.choice(player_pool.query("cost > 90").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    for i in range(9):
        idx = random.choice(player_pool.query("position == 'DEF'").index)
        myteam.add_player( Player(player_pool.ix[idx]) )
        player_pool.drop(idx, inplace=True)
    return myteam, player_pool

def strategy5(myteam, player_pool):
    # Expensive RB + WR + TE
    idx = random.choice(player_pool.query("(cost > 40) & (position == 'RB')").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    idx = random.choice(player_pool.query("(cost > 40) & (position == 'WR')").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    idx = random.choice(player_pool.query("(cost > 40) & (position == 'TE')").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    return myteam, player_pool

def strategy6(myteam, player_pool):
    # no top tier QB, at least one 2nd tier QB
    idx = player_pool.query("(cost > 90) & (position == 'QB')").index
    player_pool.drop(idx, inplace=True)
    idx = random.choice(player_pool.query("(cost >= 40) & (position == 'QB')").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    return myteam, player_pool

def strategy7(myteam, player_pool):
    # top tier QB + RB + decent WR
    idx = random.choice(player_pool.query("cost > 90").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    idx = random.choice(player_pool.query("(cost > 40) & (position == 'RB')").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    idx = random.choice(player_pool.query("(cost >= 35) & (cost <= 45) & (position == 'WR')").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    return myteam, player_pool

def strategy8(myteam, player_pool):
    # top tier QB + WR + decent RB
    idx = random.choice(player_pool.query("cost > 90").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    idx = random.choice(player_pool.query("(cost > 20) & (cost < 35) & (position == 'RB')").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    idx = random.choice(player_pool.query("(cost >= 45) & (cost <= 60) & (position == 'WR')").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    return myteam, player_pool

def strategy9(myteam, player_pool):
    # top tier QB + RB + a few cheap DEF
    idx = random.choice(player_pool.query("cost > 90").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    idx = random.choice(player_pool.query("(cost > 40) & (position == 'RB')").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    idx = random.choice(player_pool.query("(cost >= 1) & (cost <= 3) & (position == 'DEF')").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    idx = random.choice(player_pool.query("(cost >= 1) & (cost <= 3) & (position == 'DEF')").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    idx = random.choice(player_pool.query("(cost >= 1) & (cost <= 3) & (position == 'DEF')").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    idx = random.choice(player_pool.query("(cost >= 1) & (cost <= 3) & (position == 'DEF')").index)
    myteam.add_player( Player(player_pool.ix[idx]) )
    player_pool.drop(idx, inplace=True)
    return myteam, player_pool

def sample_teams(strategy_fcn, players):
    teams = []
    score_and_cost = []

    failure_count = 0
    for i in range(1000):
        if (i % 100) == 0:
            print 'round', i
        myteam = Team()
        player_pool = players.copy()
        myteam, player_pool = strategy_fcn(myteam, player_pool)
        myteam, roster_filled = fill_remaining_spots(myteam, player_pool)
        if roster_filled:
            teams.append(myteam)
            score_cost_tuple = (myteam.score(), myteam.cost())
            score_and_cost.append( score_cost_tuple )
        else:
            failure_count += 1
        df = pd.DataFrame(score_and_cost, columns=("Score", "Cost"))
    print "%d failures" % failure_count
    return teams, df

def print_top_team(teams, df):
    top_team = teams[df['Score'].argmax()]
    print top_team
    print "%.2f, $%d" % (top_team.score(), top_team.cost())

# team_list = []
df_list = []

for s in [strategy1, strategy2, strategy3, strategy4, strategy5,
          strategy6, strategy7, strategy8]:
    df = pd.read_csv('%s.csv' % s.__name__)
    df_list.append((s.__name__, df))

for s in [strategy9]:
    strategy_name = s.__name__
    print strategy_name
    teams, df = sample_teams(s, player_df)
    # team_list.append(teams)
    df_list.append((strategy_name, df))
    print_top_team(teams, df)
    df.to_csv('%s.csv' % strategy_name, index=False)

print "Median scores"
for strategy_name, df in df_list:
    print strategy_name, df['Score'].median()

ax = sns.distplot(df_list[0][1]['Score'], rug=False, hist=False,
                  label=df_list[0][0])

for strategy_name, df in df_list[1:]:
    sns.distplot(df['Score'], rug=False, hist=False,
                 label=strategy_name, ax=ax)

plt.savefig('strategy_comparison.png')
plt.clf()
print 'Wrote strategy_comparison.png'

