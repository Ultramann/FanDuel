import models
import random
import nfldb

def genetic_optimize(player_dict, pop_size=50, step=1, team_mutation_prob=0.2,
                         rank_mutation_prob=.05, elite=0.2, max_iterations=100):
    # CONSIDER ADDING VALUE_FUCNTION AS A PARAMETER   
    # Make all players object
    all_players = models.PlayerDictionary(player_dict)
    
    # Build the intitial population
    population = []
    for i in range(pop_size):
        population.append(all_players.random_team())

    # How many winners from each generation
    top_elite = int(elite * pop_size)

    # Main loop
    for i in range(max_iterations):
        scores = [(team.value(), team) for team in population]
        scores.sort(reverse = True)
        ranked_teams = [team for (value, team) in scores]

        # Start with the pure winners
        population = ranked_teams[0:top_elite]

        # Add mutated and bred forms of winners
        while len(population) < pop_size:
            mutated_team = models.Team()
            if random.random() < team_mutation_prob:
                # Mutate team
                team = ranked_teams[random.randint(0, top_elite)]
                mutated_team = all_players.mutate_team(team)

            elif random.random() < rank_mutation_prob:
                # Mutate random player's ranking
                team = ranked_teams[random.randint(0, top_elite)]
                mutated_team = team.mutate_rating()

            else:
                # Crossover
                team1 = ranked_teams[random.randint(0, top_elite)]
                team2 = ranked_teams[random.randint(0, top_elite)]
                mutated_team = team1 + team2

            # Check to see if mutated team is unique
            new_team = True
            for team in population:
                if str(team) == str(mutated_team):
                    new_team = False

            # Add if it's new
            if new_team:
                population.append(mutated_team)
    print scores[0][1]
    return scores[0][1]

def get_o_stats(player_df):
    player_df['O-Rating'] = 0
    for player in player_df.index:
        pass
    pass
