"""
Core Paper:
    - Scaling Laws for Neural Language Models
Related Reading:
    - The Asethetics of randomness nassim taleb black swarm
    - M.EJ Newman(2005)
    - Weng, Lilian. “Scaling Laws, Carefully”. Lil’Log (Jun 2026). https://lilianweng.github.io/posts/2026-06-24-scaling-laws/

Non-test code for paper22.  The tests live in test_power_laws.py and
test_scale_with_parameters.py; run them with `uv run pytest`.
"""

import numpy as np
import matplotlib.pyplot as plt


def power_law(x, alpha, b, c):
    """
    Output of this funciton is loss

    alpha_exponent for paramters, datasize and compute

    alpha_N = 0.076
    alpha_D = 0.095
    alpha_C = 0.050

    Notice these exponents are very small, way smaller than returns in financial markets
    alpha = 2 ~ 3 or even intensity of wars 0.8 and frequency of word use 1.2

    Critical parameter count
    Nc = 8.8e13 parameter count(human brain 8.6e10)
    Dc = 5.4e13
    Cc = 3,1e18 critical compute

    """
    return b * x ** (-alpha) + c


class SimpleTrainDataSimulator:
    def __init__(self, num_paras, vocab_size=100, embed_dim=32):
        self.num_paras = num_paras
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.capacity = self.calculate_capacity_from(num_paras)

    def calculate_capacity_from(self, num_paras):
        capacity = np.log(num_paras) / 10.0
        return capacity

    def data_scaling(self, dataset_size):
        return 1/(1 + np.log(dataset_size)/15.0)

    def parameter_scaling(self):
        return 1/(1 + self.capacity)

    def add_random_noise(self):
        return np.random.randn() * 0.05

    def train(self, dataset_size, num_steps):
        base_loss = np.log(self.vocab_size)
        param_factor = self.parameter_scaling()
        data_factor = self.data_scaling(dataset_size)
        train_convergence_factor = np.exp(-num_steps/1000.0)
        loss = base_loss * param_factor * data_factor * (0.5 + 0.5 * train_convergence_factor)
        loss += self.add_random_noise()
        return loss
        #return max(loss, 1.0)


def scaling_law_parameters(x, a, b):
    return a * x ** (-b)


# Sweep defaults used by both the driver below and the tests.
NUM_DATASIZE = 100_000
NUM_STEPS = 1_000
NUM_OF_PARAMETERS = [1e3, 5e3, 1e4, 5e4, 1e5, 5e5, 1e6, 5e6, 1e7]


def model_by_parameter_size(num_of_parameters, num_datasize, num_steps):
    losses_by_parameters = []

    for n_p in num_of_parameters:
        loss = SimpleTrainDataSimulator(n_p).train(num_datasize, num_steps)
        losses_by_parameters.append(loss)

    losses_by_parameters = np.array(losses_by_parameters)
    return losses_by_parameters


def plot_scale_with_parameters(para_counts, losses_by_parameters):
    plt.figure(figsize=(10,6))
    plt.loglog(para_counts, losses_by_parameters,'s',markersize=10,color='orange',label='measured loss')
    plt.show()


def main():
    losses_by_parameters = model_by_parameter_size(
        NUM_OF_PARAMETERS, NUM_DATASIZE, NUM_STEPS)
    plot_scale_with_parameters(NUM_OF_PARAMETERS, losses_by_parameters)


if __name__ == "__main__":
    main()
