from scipy.stats import kendalltau
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="darkgrid")
from load import player_df
from model import choose_random_team


teams = []
team_scores_and_costs = []

for i in range(1000):
    if (i % 100) == 0:
        print 'round', i
    myteam, roster_filled = choose_random_team(player_df.copy())
    if roster_filled:
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
print team_df.ix[team_df['TotalScore'].argmax()]
top_team = teams[team_df['TotalScore'].argmax()]
print top_team
print "%.2f, $%d" % (top_team.score(), top_team.cost())
print "Score per position"
print top_team.score_per_position()
print "Cost per position"
print top_team.total_cost_per_position()

column_list = ['TotalCost', 'QBCost', 'RBCost', 'WRCost', 'TECost',
               'KCost', 'DEFCost', 'DCost']
for c in column_list:
    x = team_df[c]
    y = team_df['TotalScore']
    # sns.jointplot(x, y, kind="reg", stat_func=kendalltau, color="#4CB391")
    sns.regplot(x, y, lowess=True, color="#4CB391")
    plt.savefig('plots2/team_score_vs_%s_cost.png' % c)
    plt.clf()

pair_list = [('QB', 'QBCost', 'QBScore'), ('RB', 'RBCost', 'RBScore'),
             ('WR', 'WRCost', 'WRScore'), ('TE', 'TECost', 'TEScore'),
             ('K', 'KCost', 'KScore'), ('DEF', 'DEFCost', 'DEFScore'),
             ('D', 'DCost', 'DScore')]
for p in pair_list:
    x = team_df[p[1]]
    y = team_df[p[2]]
    # sns.jointplot(x, y, kind="reg", stat_func=kendalltau, color="#4CB391")
    sns.regplot(x, y, lowess=True, color="#4CB391")
    plt.savefig('plots3/%s_score_vs_cost.png' % p[0])
    plt.clf()

column_list = ['QBCount', 'RBCount', 'WRCount', 'TECount', 'KCount',
               'DEFCount', 'DCount']
for c in column_list:
    x = team_df[c]
    y = team_df['TotalScore']
    sns.jointplot(x, y, kind="reg", stat_func=kendalltau, color="#4CB391")
    # sns.regplot(x, y, lowess=True, color="#4CB391")
    plt.savefig('plots4/team_score_vs_%s.png' % c)
    plt.clf()

pair_list = [('QB', 'QBCount', 'QBScore'), ('RB', 'RBCount', 'RBScore'),
             ('WR', 'WRCount', 'WRScore'), ('TE', 'TECount', 'TEScore'),
             ('K', 'KCount', 'KScore'), ('DEF', 'DEFCount', 'DEFScore'),
             ('D', 'DCount', 'DScore')]
for p in pair_list:
    x = team_df[p[1]]
    y = team_df[p[2]]
    sns.jointplot(x, y, kind="reg", stat_func=kendalltau, color="#4CB391")
    # sns.regplot(x, y, lowess=True, color="#4CB391")
    plt.savefig('plots5/%s_score_vs_count.png' % p[0])
    plt.clf()
