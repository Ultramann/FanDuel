import re

class PlayerDictionary():
    # Master dictionary with positions as keys and dictionaries of 
    # players at that position as objects

    def __init__(self, player_dict):
        positions = ['QB', 'WR', 'RB', 'TE', 'K', 'D']
        new_player_dict = {position: {} for position in positions}
        for player_name in player_dict:
            player = Player(player_name, player_dict[player_name])
            new_player_dict[player.position][player_name] = player
        for position, player in new_player_dict.items():
            setattr(self, position, player)

    def randomTeam(self):
        # After I define the team model, this function will be called on the master player dict object and return a team object with randomized players
        pass

class DotNotationPlayerDictionary():
    # Master dictionary with all the player objects as attributes
    # Great for quickly getting into the dict and retriving info
    def __init__(self, player_dict):
        for player_name in player_dict.keys():
            player = Player(player_name, player_dict[player_name])
            setattr(self, re.sub(r'[^a-zA-Z0-9]','', player_name), player)

class Player():
    def __init__(self, player_name, player_data_dict):
        self.name = player_name
        for attribute, data in player_data_dict.items():
            setattr(self, attribute.lower(), data) 
            
#class Team(PlayerDictionary):
#    def __init__(self)
