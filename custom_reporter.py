import os
import shutil
import neat
import statistics

class CustomReporter(neat.reporting.BaseReporter):
    def __init__(self, filename="fitness_stats.csv"):
        self.filename = filename
        self.generation = 0
        self.directory_path = os.path.dirname(os.path.abspath(filename))
        
        # Open the file and write the header line
        with open(self.filename, "w") as f:
            f.write("Generation,AverageFitness,StdDev,MaxFitness\n")

        # Create a subdirectory for checkpoints
        self.checkpoint_path = os.path.join(self.directory_path, "checkpoints")
        os.makedirs(self.checkpoint_path, exist_ok=True)

    def post_evaluate(self, config, population, species, best_genome):
        # Calculate statistics
        fitnesses = [genome.fitness for genome in population.values() if genome.fitness is not None]
        
        avg_fitness = sum(fitnesses) / len(fitnesses)
        std_dev = statistics.stdev(fitnesses) if len(fitnesses) > 1 else 0
        max_fitness = max(fitnesses)

        self.generation += 1
        
        # Append the stats to the file
        with open(self.filename, "a") as f:
            f.write(f"{self.generation},{avg_fitness},{std_dev},{max_fitness}\n")

        print(f'Generation {self.generation} -- Max Fitness: {max_fitness:.3f}, Avg Fitness: {avg_fitness:.3f}, Std Dev: {std_dev:.3f}')
