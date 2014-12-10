class PlayerDictionary():
    self.QB = {}
    self.WR = {}
    self.RB = {}
    self.TE = {}
    self.K = {}
    self.D = {}
    def __init__(self, player_dict):
        for player_name in player_dict:
            player = Player(player_name, player_dict[player_name][2:]) # I THINK THAT INDEX 1 IS THE POSITION...
            eval('self.' + player.position + '[player_name] = player') # I THINK THIS WILL WORK, BUT I MIGHT END UP WANTING TO HAVE A DICTIONARY WITH KEY: VALUES - PLAYERNAME: PLAYER(CLASS)

class Player():
    def __init__(self, player_name, player_data):
        self.name = player_name
        for i, attribute in enumerate(['position', 'salary', 'rating', 'rating_mutation',
                                        'volatility', 'fppg', 'games_played']):
            setattr(self, attribute, player_data[i])
            
        self.position = player_data[0]
        self.salary = player_data[1]
        self.rating = player_data[2]
        self.rating_mutation = player_data[3]
        self.volatility = player_data[4]
        self.fppg = player_data[5]
        self.games_played = player_data[6]

class Team(PlayerDictionary):
    def __init__(self)
