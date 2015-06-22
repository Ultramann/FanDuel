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
            while True:
                rand_player = random.choice(position_dict.keys())
                old_player = False
                for existing_position in rand_team_dict:
                    player = rand_team_dict[existing_position]
                    if player.name == rand_player: old_player = True
                if not old_player: break
            
            # Set accrodingly in rand_teams dict
            player = position_dict[rand_player]
            rand_team_dict[position] = Player(player.name, player.to_dict())
            
        return Team(rand_team_dict)
    
    def mutate_team(self, team):
        # Copy team
        mutated_team = Team(team.to_dict())
        
        # Choose random position in team to swap with new player
        positions = ['QB', 'WR1', 'WR2', 'WR3', 'RB1', 'RB2', 'TE', 'K', 'D']
        position = random.choice(positions)
        simple_position = ''.join(i for i in position if not i.isdigit())
        
        # Get a new player at that position 
        old_player = getattr(team, position)
        player_dict = getattr(self, simple_position)
        while True:
            player = player_dict[random.choice(player_dict.keys())]
            if player.name != old_player.name: break
        
        # Put a copy of the new player mutated team
        setattr(mutated_team, position, Player(player.name, player.to_dict()))
        return mutated_team    
        
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
            setattr(self, re.sub(r'[^a-zA-Z0-9]','_', attribute.lower()), data) 

    def to_dict(self):
        attributes = ['fppg', 'gp', 'name', 'position', 'rating', 
                        'rating_mutation', 'salary', 'volatility']
        player_dict = {attribute: getattr(self, attribute) for attribute in attributes}
        return player_dict

class Team():
    positions = ['QB', 'WR1', 'WR2', 'WR3', 'RB1', 'RB2', 'TE', 'K', 'D']

    def __init__(self, set_positions_dict={'QB': None, 'WR1': None, 'WR2': None, 'WR3': None, 
                                'RB1': None, 'RB2': None, 'TE': None, 'K': None, 'D': None}):
        for position, player in set_positions_dict.iteritems():
            setattr(self, position, player)

    def __str__(self):
        # Begin with heading for the string representation
        string_form = '%-10s %-25s %-8s %-9s %-16s %-14s' % ('Position', 'Player', 'Salary', 
                                                'Rating', 'Rating Mutation', 'Mutated Rating')
        string_form += '\n' + '-' * 86

        # Add in a line for each position with the same format
        for position in ['QB', 'WR1', 'WR2', 'WR3', 'RB1', 'RB2', 'TE', 'K', 'D']:
            player = getattr(self, position)
            string_form += '\n%-10s %-25s %-8s %-9s %-16s %-14s' % (position, player.name,
                                          player.salary, player.rating, player.rating_mutation,
                                          player.rating + player.rating_mutation)
        
        string_form += '\n' + '-' * 86
        string_form += '\n%-10s %-25s %-8s %-9s %-16s %-14s' % ('', 'Total:', self.cost(), 
                                                                    '', '', self.value())
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
            player = getattr(self, position)
            crossed_team_dict[position] = Player(player.name, player.to_dict())
        for position in other_positions_kept:
            player = getattr(self, position)
            crossed_team_dict[position] = Player(player.name, player.to_dict())
            
        return Team(crossed_team_dict)

    def value(self, position_weights={'QB':1, 'WR1':.95, 'WR2':.8, 'WR3':.6, 
                                        'RB1':.95, 'RB2':.7, 'TE':.7, 'K':.3, 'D':.2}):
        total_value = 0
        for position in ['QB', 'WR1', 'WR2', 'WR3', 'RB1', 'RB2', 'TE', 'K', 'D']:
            player = getattr(self, position)
            total_value += (player.rating + player.rating_mutation) * position_weights[position]
            # HAVE SOMETHING IN HERE THAT LOWERS VALUE OF THE TEAM'S TOTAL VOLITILITY IS OVER SOME VALUE...
            # MAYBE DO THE SAME THING WITH RATING MUTATION
        if self.cost() > 60000: total_value -= 100

        return total_value

    def cost(self):
        total_salary = 0
        for position in ['QB', 'WR1', 'WR2', 'WR3', 'RB1', 'RB2', 'TE', 'K', 'D']:
            player = getattr(self, position)
            total_salary += player.salary

        return total_salary

    def team_analysis(self):
        for position in ['QB', 'WR1', 'WR2', 'WR3', 'RB1', 'RB2', 'TE', 'K', 'D']:
            player = getattr(self, position)
            value = player.rating + player.rating_mutation
            ratio = value / player.salary
            print '{}: {}, cost to value ratio: {} : {} = {}'.format(position, player.name,
                                                                player.salary, value, ratio)

    def to_dict(self):
        team = {position: getattr(self, position) for position in ['QB', 'WR1', 'WR2', 'WR3', 'RB1', 'RB2', 'TE', 'K', 'D']}
        return team   

    def mutate_rating(self):
        mutated_team = Team(self.to_dict())
        positions = ['QB', 'WR1', 'WR2', 'WR3', 'RB1', 'RB2', 'TE', 'K', 'D']
        # Construct weighted list of volitility levels
        weighted_vol_list = [x for y in range(1, 6) for x in range(y, 6)]
        
        # Construct dict of volitility levels with list of player at that level as values
        vol_level_dict = {vol_level: [position for position in positions if getattr(self, position).volatility == vol_level] for vol_level in range(1, 6)}
                          
        # Choose a random volatility level from weighted list of levels
        while 1:
            rand_vol_level = random.choice(weighted_vol_list)
            # Can't choose from as list with nothing in it...
            if len(vol_level_dict[rand_vol_level]) != 0: break
        
        # Get player at random position
        position = random.choice(vol_level_dict[rand_vol_level])
        old_player = getattr(mutated_team, position)
        player = Player(old_player.name, old_player.to_dict())
        player_mutated_rating = player.rating + player.rating_mutation
        
        # Choose rating mutation
        if 0 < player_mutated_rating < 10 and player.rating_mutation != 0:
            if player.rating_mutation > 0: direction = 1
            elif player.rating_mutation < 0: direction = -1
            chance = random.uniform(-1, 5)
            if 0.5 < chance <= (5 - player.rating_mutation * direction):
                rating_mutation = direction
            elif 0 < chance <= 0.5:
                rating_mutation = -1 * direction
            elif (5 - player.rating_mutation * direction) < chance <= 5:
                rating_mutation = -1 * direction
            else: rating_mutation = 0
        elif player.rating_mutation == 10: rating_mutation = random.choice([0, -1])
        elif player.rating_mutation == 0: rating_mutation = random.choice([0, 1])
        else: rating_mutation = random.choice([-1, 0, 1])
        
        # Mutate rating
        player.rating_mutation += rating_mutation
        setattr(mutated_team, position, player)
        return mutated_team
