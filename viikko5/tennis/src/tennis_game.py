class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_score = 0
        self.player2_score = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.player1_score += 1
        elif player_name == self.player2_name:
            self.player2_score += 1

    def get_score(self):
        if self.player1_score == self.player2_score:
            return self._score_when_tied()
        elif self.player1_score >= 4 or self.player2_score >= 4:
            return self._score_when_advantage_or_win()
        else:
            return self._score_when_playing()

    def _score_when_tied(self):
        score_names = {
            0: "Love-All",
            1: "Fifteen-All",
            2: "Thirty-All",
        }
        return score_names.get(self.player1_score, "Deuce")

    def _score_when_advantage_or_win(self):
        score_difference = self.player1_score - self.player2_score
        if score_difference == 1:
            return f"Advantage {self.player1_name}"
        elif score_difference == -1:
            return f"Advantage {self.player2_name}"
        elif score_difference >= 2:
            return f"Win for {self.player1_name}"
        else:
            return f"Win for {self.player2_name}"

    def _score_when_playing(self):
        score_names = ["Love", "Fifteen", "Thirty", "Forty"]
        player1_text = score_names[self.player1_score]
        player2_text = score_names[self.player2_score]
        return f"{player1_text}-{player2_text}"
