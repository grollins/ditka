import random
from copy import deepcopy
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="darkgrid")
from load import player_df
from model import Team, Player


class TeamOptimizer(object):
    """docstring for TeamOptimizer"""
    def __init__(self, player_pool):
        self.team = Team()
        self.player_pool = player_pool
        self.threshold = 0.99
        self.score = 0.0
        self.cost = 0.0
        self.num_trials = 0
        self.trajectory = [(self.num_trials, self.score, self.cost)]
        self.team_list = []

        # get elite qb, remove all others from player pool
        idx = random.choice(self.player_pool.query("cost > 90").index)
        self.team.add_player( Player(self.player_pool.ix[idx]) )
        self.player_pool.drop(idx, inplace=True)
        idx = self.player_pool.query("position == 'QB'").index
        self.player_pool.drop(idx, inplace=True)
        print self.player_pool['position'].value_counts()

    def optimize_team(self, total_trials=999):
        t = 0
        moves_accepted = 0
        trial_score = 0.0
        while t <= total_trials:
            trial_team, trial_score, trial_cost = self._do_trial_move()
            if self._accept_move(trial_score):
                self.score = trial_score
                self.cost = trial_cost
                self.team = trial_team
                moves_accepted += 1
            self.num_trials += 1
            t += 1
            self.trajectory.append((self.num_trials, self.score, self.cost))
            self.team_list.append(deepcopy(self.team))
        print "Accepted %d out of %d" % (moves_accepted, total_trials)

    def _do_trial_move(self):
        trial_team = deepcopy(self.team)
        idx = random.choice(self.player_pool.index)
        player_row = self.player_pool.ix[idx]
        trial_team.replace_player_starters_only( Player(player_row) )
        return trial_team, trial_team.score(), trial_team.cost()

    def _accept_move(self, trial_score):
        delta_score = trial_score - self.score
        if delta_score > 0.0:
            return True
        else:
            return (random.random() > self.threshold)

#  ========
#  = MAIN =
#  ========
opt = TeamOptimizer(player_df)
opt.optimize_team(total_trials=9999)

traj_df = pd.DataFrame(opt.trajectory, columns=['step', 'score', 'cost'])
traj_df.set_index('step', inplace=True)

print traj_df.ix[traj_df['score'].argmax()]
top_team = opt.team_list[traj_df['score'].argmax()]
print top_team

for i in traj_df.sort('score', ascending=False).drop_duplicates().index[:3]:            
    print opt.team_list[i]

traj_df.plot()
plt.show()
plt.clf()
