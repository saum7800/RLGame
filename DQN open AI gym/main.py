import gym
from DQN import DQNAgent


def train():
    env = gym.make('CartPole-v0')
    agent = DQNAgent(env=env)
    num_episodes = 200
    for i_episode in range(num_episodes):
        state = env.reset()
        total_reward = 0
        while True:
            action = agent.get_action(state)
            next_state, reward, done, info = env.step(action)
            total_reward += reward
            update_array = [state, action, reward, next_state, done]
            agent.update(update_array)
            state = next_state
            if done:
                print("Episode ", i_episode, ": ", total_reward, "  epsilon: ", agent.epsilon)
                break
    agent.save('myClassModel')
    env.close()


def test():
    env = gym.make('CartPole-v0')
    my_test_agent = DQNAgent(env, model='myClassModel')
    avg_reward, max_reward = my_test_agent.test_agent()
    print("average reward: ", avg_reward, " maximum reward: ", max_reward)


if __name__ == "__main__":
    train()
    test()
