class PlayerDictionary():
    def __init__(self, player_dict):
        positions = ['QB', 'WR', 'RB', 'TE', 'K', 'D']
        new_player_dict = {position: {} for position in positions}
        for player_name in player_dict:
            player = Player(player_name, player_dict[player_name])
            new_player_dict[player.position][player_name] = player
        for position, player in new_player_dict.items():
            setattr(self, position, player)

class Player():
    def __init__(self, player_name, player_data_dict):
        self.name = player_name
        for attribute, data in player_data_dict.items():
            setattr(self, attribute.lower(), data) 
            
#class Team(PlayerDictionary):
#    def __init__(self)
