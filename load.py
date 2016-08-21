import numpy as np
import pandas as pd


stats = pd.read_csv('stats2015.csv', index_col='player_key')
stats2014 = pd.read_csv('stats2014.csv', index_col='player_key')
stats2013 = pd.read_csv('stats2013.csv', index_col='player_key')
# stats2013.rename({'points': 'points2013'}, inplace=True)
draft = pd.read_csv('draft.csv', index_col='player_key')
df = stats.merge(draft, how='outer', left_index=True, right_index=True)
df = df.merge(stats2014[['points', 'full_name']], how='left', on='full_name',
              suffixes=('', '2014'))
df = df.merge(stats2013[['points', 'full_name']], how='left', on='full_name',
              suffixes=('', '2013'))
df.fillna(0, inplace=True)
df['cost'] = df['cost'].astype(np.int32)
df['pick'] = df['pick'].astype(np.int32)
df.to_csv('data.csv', index=False,
          columns=['full_name','points', 'points2014', 'points2013',
                   'position', 'cost', 'pick'])

df = df.query("points > 0.0")
positions = df['position'].value_counts()
grouper = df.groupby('position')

def f(group):
    num_players = min(len(group), 32)
    top_players = group.sort('points', ascending=False).head(num_players)
    most_expensive_players = group.sort('cost', ascending=False).head(num_players)
    top_players = pd.concat([top_players, most_expensive_players]).drop_duplicates()
    return top_players

player_df = grouper.apply(f)
print player_df['position'].value_counts()
player_df.loc[player_df['cost'] < 1, 'cost'] = 1

# print 'QB'
# for c in player_df.query("(position == 'QB') & (pick > 0)").sort('cost', ascending=False)['cost'].values:
#     print c

# print 'RB'
# for c in player_df.query("(position == 'RB') & (pick > 0)").sort('cost', ascending=False)['cost'].values:
#     print c

# print 'WR'
# for c in player_df.query("(position == 'WR') & (pick > 0)").sort('cost', ascending=False)['cost'].values:
#     print c

# print 'TE'
# for c in player_df.query("(position == 'TE') & (pick > 0)").sort('cost', ascending=False)['cost'].values:
#     print c

# print 'K'
# for c in player_df.query("(position == 'K') & (pick > 0)").sort('cost', ascending=False)['cost'].values:
#     print c

# print 'DEF'
# for c in player_df.query("(position == 'DEF') & (pick > 0)").sort('cost', ascending=False)['cost'].values:
#     print c

# print 'D'
# for c in player_df.query("(position == 'D') & (pick > 0)").sort('cost', ascending=False)['cost'].values:
#     print c
