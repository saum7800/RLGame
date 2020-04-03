import gym
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import random
from collections import deque


class DQNAgent:

    def __init__(self, env, gamma=0.99, epsilon_start=1.0, epsilon_min=0.1, epsilon_decay=0.0001, replay_capacity=1000,
                 batch_size=64, train_every=5, update_target_every=500, model=None):
        self.epsilon = epsilon_start
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.train_every = train_every
        self.update_target_every = update_target_every
        self.batch_size = batch_size
        self.replay_capacity = replay_capacity
        self.gamma = gamma
        self.env = env
        self.num_actions = self.env.action_space.n
        self.num_observations = len(self.env.observation_space.high)
        self.replay = deque()
        self.num_replays = 0
        self.total_timesteps = 0

        if model is None:
            self.model = tf.keras.Sequential([
                layers.Dense(128, activation='relu', input_shape=(self.num_observations,)),
                layers.Dense(64, activation='relu'),
                layers.Dense(self.num_actions)
            ])
            self.model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
        else:
            self.model = tf.keras.models.load_model(model + '.h5')

        self.model_fixed_target = tf.keras.models.clone_model(self.model)
        self.model_fixed_target.set_weights(self.model.get_weights())

    def updateEpsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon -= self.epsilon_decay

    def get_action(self, state):
        if random.random() < self.epsilon:
            action = self.env.action_space.sample()
        else:
            action = np.argmax(self.model.predict(np.reshape(state, (1, self.num_observations))))
        self.updateEpsilon()
        return action

    def get_batch(self, replay_arr):
        batch = random.sample(replay_arr, self.batch_size)
        batch = np.array(batch)
        curr_states = np.array([batch[i][0] for i in range(self.batch_size)])
        new_states = np.array([batch[i][3] for i in range(self.batch_size)])
        return batch, curr_states, new_states

    def get_target(self, batch, curr_states, new_states):
        Y = self.model.predict(curr_states)
        new_state_Q_values = self.model_fixed_target.predict(new_states)

        for i, (state, action, reward, next_state, done) in enumerate(batch):
            Y[i, action] = reward + self.gamma * np.max(new_state_Q_values[i]) * (1 - done)

        return Y

    def train(self):
        replay_arr = list(self.replay)
        batch, curr_states, new_states = self.get_batch(replay_arr)
        Y = self.get_target(batch, curr_states, new_states)
        self.model.fit(curr_states, Y, epochs=10, verbose=0)

    def update(self, update_array):
        if self.num_replays < self.replay_capacity:
            self.replay.append(update_array)
            self.num_replays += 1
        else:
            self.replay.popleft()
            self.replay.append(update_array)

            if (self.total_timesteps % self.train_every) == 0:
                self.train()

            if (self.total_timesteps % self.update_target_every) == 0:
                self.model_fixed_target.set_weights(self.model.get_weights())

        self.total_timesteps += 1

    def save(self, path):
        self.model.save(path + '.h5')

    def test_agent(self, num_test_eps=10, render_every=1):
        avg_reward = 0
        max_reward = float('-inf')
        render = False
        for i_episode in range(1, num_test_eps + 1):
            episode_reward = 0
            state = self.env.reset()
            if (i_episode % render_every) == 0:
                render = True
            while True:
                if render:
                    self.env.render()
                action = np.argmax(self.model.predict(np.reshape(state, (1, self.num_observations))))
                next_state, reward, done, info = self.env.step(action)
                episode_reward += reward
                state = next_state
                if done:
                    if episode_reward > max_reward:
                        max_reward = episode_reward
                    render = False
                    avg_reward += episode_reward
                    print("Episode ", i_episode, ": ", episode_reward)
                    break
        avg_reward = avg_reward / num_test_eps
        return avg_reward, max_reward
