import numpy as np
from scipy.stats import kendalltau
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="darkgrid")

df = pd.read_csv('data.csv', index_col='full_name')
positions = df['position'].value_counts()

grouper = df.groupby('position')
for label, group in grouper:
    num_players = min(len(group), 50)
    # top_players = group.sort('cost', ascending=False).head(num_players)
    top_players = group.sort('cost', ascending=False)
    x, y = top_players['cost'], top_players['points']
    # plt.plot(x, y, 'o', ms=8)
    # sns.jointplot(x, y, kind="reg", stat_func=kendalltau, color="#4CB391")
    g = sns.PairGrid(top_players)
    g = g.map_diag(plt.hist)
    g = g.map_offdiag(plt.scatter)
    ax = plt.gca()
    ax.set_title(label)
    plt.savefig('plots/%s.png' % label)
    plt.clf()

# for p, ax in zip(positions.index, axes.flat):
#     x, y = df['cost'], df['points']
#     sns.kdeplot(x, y, shade=True, ax=ax)
#     ax.set_title(p)
#     # ax.set(xlim=(-3, 3), ylim=(-3, 3))
# f.tight_layout()
# plt.show()
