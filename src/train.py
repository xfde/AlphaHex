from Coach import Coach
from NeuralNet import NeuralNet as nn
import sys

from HexGame import HexGame as Game
import json
from utils import *

args = dotdict({
    'numIters': 1000,
    'numEps': 100,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 25,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 40,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,
})

def main():
    config_file = open('./example.json', 'r')
    params = json.load(config_file)
    config_file.close()

    g = Game(11)
    nnet = nn(g, params)
    # if args.load_model:
    #     log.info('Loading checkpoint "%s/%s"...', args.load_folder_file[0], args.load_folder_file[1])
    #     nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
    # else:
    #     log.warning('Not loading a checkpoint!')
    c = Coach(g, nnet, args, params)
    c.learn()


if __name__ == "__main__":
    main()
