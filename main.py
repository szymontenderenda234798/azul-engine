import neat
import os
from game_engine import GameEngine
from model.neural_network_player import NeuralNetworkPlayer
from model.random_player import RandomPlayer

if __name__ == '__main__':

    def eval_genomes(genomes, config):
        """
        Evaluate the genomes using the game engine.
        """
        for genome_id, genome in genomes:
            print("Playing game with genome {}".format(genome_id))
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

    # Run for up to 300 generations
    winner = p.run(eval_genomes, 300)

    # Display the winning genome
    print('\nBest genome:\n{!s}'.format(winner))