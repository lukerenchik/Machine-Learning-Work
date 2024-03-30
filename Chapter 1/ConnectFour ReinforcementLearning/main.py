# Reinforcement Learning: An Introduction - Project 1
# Following Shangton Zhang's Tic_Tac_Toe Example
# Luke Renchik - March 27th 2024
# Connect 4

from MachineStates import train, compete, play

if __name__ == '__main__':
    train(int(1e5))
    compete(int(1e3))
    play()
