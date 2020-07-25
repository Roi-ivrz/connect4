import numpy as np
rows = 6
columns = 7
board = np.eye(rows, columns)
print('before: ', board)
newboard = np.array(board).reshape(rows, columns,1)
print('after: ', newboard)

'''
import gym
import random

env = gym.make('CartPole-v1')
print('observation space: ', env.observation_space)
print('Action space: ', env.action_space)

class Agent:
    def get
'''