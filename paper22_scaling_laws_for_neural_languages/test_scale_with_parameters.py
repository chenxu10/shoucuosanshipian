"""
Tests for the toy parameter-scaling simulator in scaling_laws.py (paper22).

Both tests take no arguments so pytest can collect them; the sweep settings
come from scaling_laws, so the driver and the tests stay in sync.
"""

from scipy.optimize import curve_fit

from scaling_laws import (
    NUM_DATASIZE,
    NUM_OF_PARAMETERS,
    NUM_STEPS,
    SimpleTrainDataSimulator,
    model_by_parameter_size,
    scaling_law_parameters,
)

ORDERED_PARAM_COUNTS = (10, 100, 1000)


def test_scale_with_parameters():
    losses = [
        SimpleTrainDataSimulator(num_paras).train(NUM_DATASIZE, NUM_STEPS)
        for num_paras in ORDERED_PARAM_COUNTS]
    print(losses)
    assert losses[0] > losses[1] > losses[2], losses


def test_curve_fit():
    losses = model_by_parameter_size(NUM_OF_PARAMETERS, NUM_DATASIZE, NUM_STEPS)
    para_fit, _ = curve_fit(scaling_law_parameters, NUM_OF_PARAMETERS, losses)
    alpha_fit, beta_fit = para_fit
    assert alpha_fit == 1
    assert beta_fit == 2
