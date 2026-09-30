"""
The one test: capacity buys lower loss.

This is the whole promise of SimpleLanguageModel and of Kaplan et al. (2001.08361):
holding data and compute fixed, a model with more parameters must reach a lower loss.
Seeding numpy makes the injected noise identical across the three runs, so the
comparison tests the scaling law rather than the RNG.
"""
import numpy as np

from simple_language_model import SimpleLanguageModel


def test_more_parameters_lower_loss():
    np.random.seed(0)
    dataset_size, num_steps = 10_000, 1_000

    losses = [
        SimpleLanguageModel(num_params).train(dataset_size, num_steps)
        for num_params in (10, 100, 1_000)
    ]

    assert losses[0] > losses[1] > losses[2], losses


if __name__ == "__main__":
    test_more_parameters_lower_loss()
    print("ok")
