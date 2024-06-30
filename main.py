import neat
import os
from game_engine import GameEngine
from model.neural_network_player import NeuralNetworkPlayer
from model.random_player import RandomPlayer
import multiprocessing
from custom_reporter import CustomReporter
from datetime import datetime

def eval_genome(genome_tuple):
    genome_id, genome, config = genome_tuple
    """
    Evaluate a single genome using the game engine.
    """
    print(f"Playing game with genome {genome_id}")
    game_engine = GameEngine(print_enabled=False, visualize=False)

    # Create a neural network from the genome
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    # Create players
    player1 = NeuralNetworkPlayer("NN Player", net)
    player2 = RandomPlayer("Random Player")

    # Play the game
    ending_state = game_engine.play_game(player1=player1, player2=player2)

    # Assume that the GameEngine provides a method to get the winner and the scores
    score1, score2 = game_engine.get_scores(ending_state)

    # Calculate fitness
    # You can customize this based on your game's scoring mechanism
    genome.fitness = score1
    if genome.fitness is None:
        genome.fitness = 0
        print(f"Warning: Genome {genome_id} fitness is None, setting to 0.")
    return genome_id, genome.fitness


def eval_genomes(genomes, config):
    # Prepare arguments for starmap
    genome_tuples = [(genome_id, genome, config) for genome_id, genome in genomes]
    
    with multiprocessing.Pool() as pool:
        fitness_values = pool.map(eval_genome, genome_tuples)
        
        for genome_id, fitness in fitness_values:
            for gid, genome in genomes:
                if gid == genome_id:
                    genome.fitness = fitness
                    break

if __name__ == '__main__':

    # Load configuration
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    # Create the population, which is the top-level object for a NEAT run
    p = neat.Population(config)

    # Add a reporter to show progress in the terminal
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Create a timestamp string
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Add the custom reporter with a timestamped filename
    custom_reporter = CustomReporter(f'generation_statistics_{timestamp}.csv')
    p.add_reporter(custom_reporter)

    # Run for up to 300 generations
    winner = p.run(eval_genomes, 300)

    # Display the winning genome
    print('\nBest genome:\n{!s}'.format(winner))