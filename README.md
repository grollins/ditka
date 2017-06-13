# ditka
fantasy football draft analysis

## depends on
yos-social-python

## steps
1. run auth.py to get access token
2. run league.py to get league id
3. insert league id in draft.py and run to get draft results
4. insert league id in stats.py and run to get player stats
5. play around with api call in stats.py to find out how many players there were
6. adjust loop length in stats.py based on previous step
7. run stats.py to get player stats
8. run plot.py to see cost vs. points
9. run rank_analysis.R to predict draft prices, based on previous year's data
