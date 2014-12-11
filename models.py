import re
import random

class PlayerDictionary():
    # Master dictionary with positions as keys and dictionaries of 
    # players at that position as objects

    def __init__(self, player_dict):
        positions = ['QB', 'WR', 'RB', 'TE', 'K', 'D']
        new_player_dict = {position: {} for position in positions}
        
        # Transform player_dict so that it is organized by position
        # with player object as values
        for player_name in player_dict:
            player = Player(player_name, player_dict[player_name])
            new_player_dict[player.position][player_name] = player
        
        # Iterate through new dict making positions attributes and
        # the dict of player objects the values
        for position, players in new_player_dict.items():
            setattr(self, position, players)

    def random_team(self):
        # List for teams individual positions
        team_positions = ['QB', 'WR1', 'WR2', 'WR3', 'RB1', 'RB2', 'TE', 'K', 'D']
        
        # Dict to be filled with random players for Team initialization
        rand_team_dict = {}
        
        # Loop through every position for a team
        for position in team_positions:
            # Strip off numbers from complex position names so that
            # they can be used to index into the master dict attributes
            simple_position = ''.join(i for i in position if not i.isdigit())
            
            # Get random player from simple_position in master dict
            position_dict = getattr(self, simple_position)
            rand_player = random.choice(position_dict.keys()) # Check to see if we can take off .keys()
            
            # Set accrodingly in rand_teams dict
            rand_team_dict[position] = position_dict[rand_player]
            
        return Team(rand_team_dict)
        
class SimplePlayerDictionary():
    # Master dictionary with all the player objects as attributes
    # Great for quickly getting into the dict and retriving info
    # via obvious dot notation. 

    def __init__(self, player_dict):
        for player_name in player_dict.keys():
            player = Player(player_name, player_dict[player_name])
            setattr(self, re.sub(r'[^a-zA-Z0-9]','', player_name), player)

class Player():
    # Initialize with name of the player, and the dict that comes 
    # from the normal pandas transormation in to_dict()
    
    def __init__(self, player_name, player_data_dict):
        self.name = player_name
        for attribute, data in player_data_dict.items():
            setattr(self, re.sub(r'[^a-zA-Z0-9]','', attribute.lower()), data) 
            
class Team(PlayerDictionary):
    def __init__(self, set_positions_dict={'QB': None, 'WR1': None, 'WR2': None, 'WR3': None, 
                                'RB1': None, 'RB2': None, 'TE': None, 'K': None, 'D': None}):
        for position, player in set_positions_dict.iteritems():
            setattr(self, position, player)

    def __str__(self):
        # Begin with heading for the string representation
        string_form = '%-10s %-25s %-8s %-9s %-14s %-14s' % ('Position', 'Player', 'Salary', 
                                                'Rating', 'Rating Mutation', 'Mutated Rating')
        string_form += '\n' + '-' * 86

        # Add in a line for each position with the same format
        for position in ['QB', 'WR1', 'WR2', 'WR3', 'RB1', 'RB2', 'TE', 'K', 'D']:
            player = getattr(self, position)
            string_form += '\n%-10s %-25s %-8s %-9s %-14s %-14s' % (position, player.name,
                                            player.salary, player.rating, player.ratingmutation,
                                            player.rating + player.ratingmutation)
        return string_form

    def __add__(self, other):
        # Type check
        #if type(other) is not Team:
        #    raise TypeError('unsupported operand type(s) for +' + ': \''
        #                    +type_as_str(self)+'\' and \''+type_as_str(right)+'\'')
        
        # Choose which positions come from which team
        team_positions = ['QB', 'WR1', 'WR2', 'WR3', 'RB1', 'RB2', 'TE', 'K', 'D']
        self_positions_kept = random.sample(team_positions, 
                                            random.randint(1, len(team_positions )))
        other_positions_kept = list(set(team_positions) - set(self_positions_kept))
        
        # Fill dict for crossed team with corresponding players
        # from the self and other's positions
        crossed_team_dict = {}
        for position in self_positions_kept:
            crossed_team_dict[position] = getattr(self, position)
        for position in other_positions_kept:
            crossed_team_dict[position] = getattr(other, position)
            
        return Team(crossed_team_dict)

