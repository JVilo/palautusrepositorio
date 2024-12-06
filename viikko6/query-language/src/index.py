from statistics import Statistics
from player_reader import PlayerReader
from matchers import And, HasAtLeast, PlaysIn, Not, HasFewerThan, All, Or

class QueryBuilder:
    def __init__(self, lst = All()):
        self._list = lst
    
    def build(self):
        return self._list
    
    def plays_in(self,team):
        self._list =QueryBuilder(PlaysIn(team))
        return self._list
    
    def has_at_least(self, value, attribute):
        
        return QueryBuilder(And(self._list,(HasAtLeast(value, attribute))))
    
    def has_fewer_than(self, value,attribute):
        return QueryBuilder(And(self._list,(HasFewerThan(value, attribute))))
    
    def one_of(self, opt1, opt2):
        return QueryBuilder(Or(opt1,opt2))

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2023-24/players.txt"
    reader = PlayerReader(url)
    stats = Statistics(reader)

    query = QueryBuilder()
    matcher = query.build()

    for player in stats.matches(matcher):
        print(player)
    print()

    query = QueryBuilder()
    matcher = query.plays_in("NYR").build()

    for player in stats.matches(matcher):
        print(player)
    print()

    query = QueryBuilder()

    matcher = (
      query
      .plays_in("NYR")
      .has_at_least(10, "goals")
      .has_fewer_than(20, "goals")
      .build()
    )

    for player in stats.matches(matcher):
        print(player)
    print()

    m1 = (
    query
        .plays_in("PHI")
        .has_at_least(10, "assists")
        .has_fewer_than(10, "goals")
        .build()
    )

    m2 = (
    query
        .plays_in("EDM")
        .has_at_least(50, "points")
        .build()
    )

    matcher = query.one_of(m1, m2).build()
    for player in stats.matches(matcher):
        print(player)

if __name__ == "__main__":
    main()
    
    
