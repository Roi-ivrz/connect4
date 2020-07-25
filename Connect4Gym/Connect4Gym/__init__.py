from gym.envs.registration import register

register(
    id='connect4-v0',
    entry_point='connect4Gym.envs:connect4_env',
)
register(
    id='connect4-extrahard-v0',
    entry_point='connect4Gym.envs:connect4ExtraHardEnv',
)