from scipy.stats import kendalltau
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="darkgrid")
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from load import player_df
from model import choose_random_team


teams = []
team_scores_and_costs = []

for i in range(1000):
    if (i % 100) == 0:
        print 'round', i
    myteam, roster_filled = choose_random_team(player_df.copy())
    if roster_filled and myteam.score() > 1700:
        teams.append(myteam)
        pos_score = myteam.score_per_position()
        pos_cost = myteam.total_cost_per_position()
        pos_count = myteam.players_per_position()
        score_cost_tuple = \
            (myteam.score(), myteam.cost(),
             pos_cost['QB'], pos_cost['RB'], pos_cost['WR'],
             pos_cost['TE'], pos_cost['K'], pos_cost['DEF'],
             pos_cost['D'],
             sum(pos_score['QB']), sum(pos_score['RB']), sum(pos_score['WR']),
             sum(pos_score['TE']), sum(pos_score['K']), sum(pos_score['DEF']),
             sum(pos_score['D']),
             pos_count['QB'], pos_count['RB'], pos_count['WR'],
             pos_count['TE'], pos_count['K'], pos_count['DEF'],
             pos_count['D'])
        team_scores_and_costs.append( score_cost_tuple )

team_df = \
    pd.DataFrame(team_scores_and_costs,
                 columns=['TotalScore', 'TotalCost', 'QBCost', 'RBCost', 'WRCost', 'TECost',
                          'KCost', 'DEFCost', 'DCost', 'QBScore', 'RBScore', 'WRScore',
                          'TEScore', 'KScore', 'DEFScore', 'DScore',
                          'QBCount', 'RBCount', 'WRCount', 'TECount', 'KCount', 'DEFCount',
                          'DCount'])

print len(teams), "teams"
print team_df.ix[team_df['TotalScore'].argmax()]
top_team = teams[team_df['TotalScore'].argmax()]
print top_team
print "%.2f, $%d" % (top_team.score(), top_team.cost())
print "Score per position"
print top_team.score_per_position()
print "Cost per position"
print top_team.total_cost_per_position()
print "Players drafted per position"
print top_team.players_per_position()

player_names = []
for t in teams:
    for player in t:
        player_names.append("%s_%s" %(player.position, player.name))
s = pd.Series(player_names)
vc = s.value_counts()
vc.to_csv('most_common_players.txt')

X_df = team_df[['TotalScore', 'QBCount', 'RBCount', 'WRCount',
                'TECount', 'KCount', 'DEFCount', 'DCount']].sort('TotalScore', ascending=False)

with open('top_teams.txt', 'w') as f:
    for idx in X_df.index:
        # print idx, teams[idx]
        f.write('%d\n%s' % (idx, teams[idx]))

# print X_df
X = X_df.values
pca = PCA(n_components=2)
X2 = pca.fit_transform(X[:,1:])
plt.plot(X2[:,0], X2[:,1], 'o', ms=8)
plt.show()

kmeans = KMeans(n_clusters=5)
# labels = kmeans.fit_predict(X[:,1:])
labels = kmeans.fit_predict(X2)
X_df['cluster'] = labels
print X_df
plt.scatter(X2[:,0], X2[:,1], c=range(len(X_df)))
plt.show()
