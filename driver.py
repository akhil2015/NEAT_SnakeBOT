from __future__ import print_function
import os
import neat
import visualize
from snake import Snake

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
#        genome.fitness = 4.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        player = Snake(net)
        out = player.play()
        genome.fitness = out

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    #Show the winning Snake
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    champ = Snake(winner_net)
    champ.play()
    '''
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    for xi, xo in zip(xor_inputs, xor_outputs):
        output = winner_net.activate(xi)
        print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))
    '''
    node_names = {-1:'A', -2: 'B', -3:'C', -4:'D', -5:'E', -6:'F', -7:'G', -8:'H', -9:'I', -10:'J', -11:'K', -12:'L', 0:'DOWN', 1:'UP', 2:'LEFT', 3:'RIGHT'}
    visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    #p.run(eval_genomes, 10)

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)