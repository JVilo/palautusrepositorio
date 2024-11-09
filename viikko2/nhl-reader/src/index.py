import requests
from player import Player
from rich.console import Console
from rich.table import Table
from rich.style import Style


class PlayerReader:
    def __init__(self,url):
        self.url = url

    def get_players(self) -> list[Player]:
        response = requests.get(self.url).json()
        players = []

        for player_dict in response:
            player = Player(player_dict)
            players.append(player)
        
        return players

class PlayerStats:
    def __init__(self,reader: PlayerReader):
        self.reader = reader
        self.players = self.reader.get_players()
        
    def top_scorers_by_nationality(self, nationality):
        players = []
        self.players.sort(key=lambda x: x.points, reverse=True)
        for player in self.players:
            if player.nationality == nationality:
                players.append(player)
        return players

def main():
    
    console = Console()
    console.print("[italic]NHL statistics by nationality[/italic] \n")

    console = Console()
    season= console.input("select season [bright_magenta][1018-19/1019-20/2020-21/2021-22/2022-2023/2023-24/2024-25][/bright_magenta]: ")

    console = Console()
    nation = console.input("\nselect nationality \n[bright_magenta][AUT/CZE/AUS/SWE/GER/DEN/SUI/SVK/NOR/RUS/CAN/LAT/BLR/SLO/USA/FIN/GBR][/bright_magenta]: ")
    print("\n")

    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality(nation)


    table = Table(title=f"Top scorers of {nation} season {season}")
    table.add_column("name", style="cyan", no_wrap=True)
    table.add_column("team", justify="right", style="magenta", no_wrap=True)
    table.add_column("goals", justify="right", style="cyan", no_wrap=True)
    table.add_column("assists", justify="right", style="magenta", no_wrap=True)
    table.add_column("points", justify="right", style="cyan", no_wrap=True)

    for player in players:
        table.add_row(f"{player.name}", f"{player.team}", f"{player.goals}", f"{player.assists}", f"{player.points}")

    console = Console()
    console.print(table)

if __name__ == "__main__":
    main()
