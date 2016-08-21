import random
from collections import defaultdict, Counter


class Player(object):
    """docstring for Player"""
    def __init__(self, row):
        self.name = row['full_name']
        self.points = row['points']
        self.position = row['position']
        self.cost = row['cost']

    def __str__(self):
        return "%s %s $%s %.1fpts" % \
            (self.name, self.position, self.cost, self.points)

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)


class Team(object):
    """docstring for Team"""
    def __init__(self):
        self.qb = None
        self.rb = None
        self.wr = []
        self.wr_limit = 2
        self.te = None
        self.kicker = None
        self.defense = None
        self.idp = None
        self.bench = []
        self.bench_limit = 9
        self.budget = 200
        self.minimum_spend_per_player = 1

    def __iter__(self):
        players = [self.qb, self.rb, self.te, self.kicker,
                   self.defense, self.idp] + self.wr + self.bench
        for p in players:
            if p is None:
                continue
            else:
                yield p

    def __str__(self):
        qb_list = [self.qb] + [p for p in self.bench if p.position == 'QB']
        rb_list = [self.rb] + [p for p in self.bench if p.position == 'RB']
        wr_list = self.wr + [p for p in self.bench if p.position == 'WR']
        te_list = [self.te] + [p for p in self.bench if p.position == 'TE']
        k_list = [self.kicker] + [p for p in self.bench if p.position == 'K']
        def_list = [self.defense] + [p for p in self.bench if p.position == 'DEF']
        idp_list = [self.idp] + [p for p in self.bench if p.position == 'D']
        position_list = qb_list + rb_list + wr_list + te_list + k_list + \
                        def_list + idp_list
        my_string = ""
        for p in position_list:
            if p is None:
                continue
            else:
                my_string += '%s\n' % str(p) 
        return my_string

    def score(self):
        score_dict = defaultdict(list)
        for player in self:
            score_dict[player.position].append(player.points)
        total_score = 0.0
        for position, position_scores in score_dict.iteritems():
            position_scores.sort()
            if position == 'WR':
                total_score += sum(position_scores[-2:])
            else:
                total_score += position_scores[-1]
        return total_score

    def score_per_position(self):
        score_dict = defaultdict(list)
        for player in self:
            score_dict[player.position].append(player.points)
        top_score_dict = defaultdict(list)
        for position, position_scores in score_dict.iteritems():
            position_scores.sort()
            if position == 'WR':
                top_score_dict[position] = position_scores[-2:]
            else:
                top_score_dict[position] = [position_scores[-1]]
        return top_score_dict

    def total_cost_per_position(self):
        cost_dict = defaultdict(float)
        for player in self:
            cost_dict[player.position] += player.cost
        return cost_dict

    def players_per_position(self):
        player_counter = Counter()
        for player in self:
            player_counter[player.position] += 1
        return player_counter

    def cost(self):
        return sum([player.cost for player in self])

    def spots_remaining(self):
        num_spots = 0
        for position in [self.qb, self.rb, self.te, self.kicker, self.defense, self.idp]:
            if position is None:
                num_spots += 1
        num_spots += (self.wr_limit - len(self.wr))
        num_spots += (self.bench_limit - len(self.bench))
        return num_spots

    def available_budget(self):
        amount_to_hold = self.minimum_spend_per_player * (self.spots_remaining() - 1)
        amount_to_hold = max(amount_to_hold, 0.0)
        return self.budget - self.cost() - amount_to_hold

    def add_player(self, player):
        if player.cost > self.available_budget():
            return False

        if player.position == 'QB':
            if self.qb is None:
                self.qb = player
                return True
            elif len(self.bench) < self.bench_limit:
                self.bench.append(player)
                return True
            else:
                return False
        elif player.position == 'RB':
            if self.rb is None:
                self.rb = player
                return True
            elif len(self.bench) < self.bench_limit:
                self.bench.append(player)
                return True
            else:
                return False
        elif player.position == 'WR':
            if len(self.wr) < self.wr_limit:
                self.wr.append(player)
                return True
            elif len(self.bench) < self.bench_limit:
                self.bench.append(player)
                return True
            else:
                return False
        elif player.position == 'TE':
            if self.te is None:
                self.te = player
                return True
            elif len(self.bench) < self.bench_limit:
                self.bench.append(player)
                return True
            else:
                return False
        elif player.position == 'K':
            if self.kicker is None:
                self.kicker = player
                return True
            elif len(self.bench) < self.bench_limit:
                self.bench.append(player)
                return True
            else:
                return False
        elif player.position == 'DEF':
            if self.defense is None:
                self.defense = player
                return True
            elif len(self.bench) < self.bench_limit:
                self.bench.append(player)
                return True
            else:
                return False
        elif player.position == 'D':
            if self.idp is None:
                self.idp = player
                return True
            elif len(self.bench) < self.bench_limit:
                self.bench.append(player)
                return True
            else:
                return False
        else:
            raise RuntimeError()

    def _duplicated(self, player):
        for p in self:
            if p == player:
                return True
        return False

    def replace_player_starters_only(self, player):
        if player.cost > self.available_budget():
            return False
        elif self._duplicated(player):
            return False
        else:
            if player.position == 'QB':
                self.qb = player
            elif player.position == 'RB':
                self.rb = player
            elif player.position == 'WR':
                if len(self.wr) < self.wr_limit:
                    self.wr.append(player)
                else:
                    idx = random.choice(range(self.wr_limit))
                    self.wr[idx] = player
            elif player.position == 'TE':
                self.te = player
            elif player.position == 'K':
                self.kicker = player
            elif player.position == 'DEF':
                self.defense = player
            elif player.position == 'D':
                self.idp = player
            else:
                raise RuntimeError()
            return True

def choose_random_team(player_pool):
    t = Team()
    num_trials = 0
    while t.spots_remaining() and num_trials < 1000:
        idx = random.choice(player_pool.index)
        add_successful = t.add_player( Player(player_pool.ix[idx]) )
        player_pool.drop(idx, inplace=True)
        num_trials += 1
    roster_filled = (t.spots_remaining() == 0)
    return t, roster_filled

def fill_remaining_spots(t, player_pool):
    num_trials = 0
    while t.spots_remaining() and num_trials < 1000:
        idx = random.choice(player_pool.index)
        t.add_player( Player(player_pool.ix[idx]) )
        player_pool.drop(idx, inplace=True)
        num_trials += 1
    roster_filled = (t.spots_remaining() == 0)
    return t, roster_filled
