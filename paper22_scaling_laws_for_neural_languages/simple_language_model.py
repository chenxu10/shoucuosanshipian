"""
Toy language model to demonstrate scaling behavior.
"""
import numpy as np


class SimpleLanguageModel:
    def __init__(self, num_params, vocab_size=100, embed_dim=32):
        self.num_params = num_params
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.capacity = np.log(num_params) / 10.0

    def train(self, dataset_size, num_steps):
        base_loss = np.log(self.vocab_size)
        param_factor = 1.0 / (1.0 + self.capacity)
        data_factor = 1.0 / (1.0 + np.log(dataset_size) / 15.0)
        train_factor = np.exp(-num_steps / 1000.0)
        loss = base_loss * param_factor * data_factor * (0.5 + 0.5 * train_factor)
        loss += np.random.randn() * 0.05
        return max(loss, 1.0)
