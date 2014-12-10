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

    def random_team(self):
        team_positions = ['QB', 'WR1', 'WR2', 'WR3', 'RB1', 'RB2', 'TE', 'K', 'D']
        #                         I THINK \/ SELF IS THE PLAYERDICTIONARY THAT YOU'RE CALLING RANDOM_TEAM ON...
        team_dict= {position: random.choice(getattr(self, ''.join(i for i in position if not i.isdigit())).keys())
                    for position in team_positions}
        # GO BACK TO THIS IF THE DICT COMP DOESN'T WORK
        #for position in team_positions # I THINK \/ SELF IS THE PLAYERDICTIONARY THAT YOU'RE CALLING RANDOM_TEAM ON...
        #     rand_player = random.choice(getattr(self, ''.join(i for i in position if not i.isdigit())).keys())
        rand_team = Team(team_dict)
        return rand_team
        
class SimplePlayerDictionary():
    # Master dictionary with all the player objects as attributes
    # Great for quickly getting into the dict and retriving info
    # via obvious dot notation. 

    def __init__(self, player_dict):
        for player_name in player_dict.keys():
            player = Player(player_name, player_dict[player_name])
            setattr(self, re.sub(r'[^a-zA-Z0-9]','', player_name), player)

class Player():
    def __init__(self, player_name, player_data_dict):
        self.name = player_name
        for attribute, data in player_data_dict.items():
            setattr(self, attribute.lower(), data) 
            
class Team(PlayerDictionary):
    # MAYBE THIS SHOULD JUST BE A DICTIONARY...
    def __init__(self, set_positions_dict={'QB': None, 'WR1': None, 'WR2': None, 'WR3': None, 
                                            'RB1': None, 'RB2': None, 'TE': None, 'K': None, 'D': None}):
        for position, player in set_positions_dict:
            setattr(self, position, player)
    def __str__(self):
        # This defines the how the object is printed as a string
        pass
    def __add__(self, other):
        if type(other) is not Team:
            raise TypeError('unsupported operand type(s) for +' + ': \''+type_as_str(self)+'\' and \''+type_as_str(right)+'\'')
        team_positions = ['QB', 'WR1', 'WR2', 'WR3', 'RB1', 'RB2', 'TE', 'K', 'D']
        # NEED TO SELECT RANDOM SUBSET OF TEAM_POSITIONS AND CONVERSE TO CHOOSE FROM SELF AND OTHER
