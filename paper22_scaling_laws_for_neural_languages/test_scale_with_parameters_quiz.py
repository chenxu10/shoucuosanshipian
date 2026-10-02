





class SimulateTrainData:
    def __init__(self, num_paras, vocab_size=500, embed_dim=12):
        pass

def test_scale_with_parameters():
    dataset_size, num_steps = 10_000, 1_000
    num_paras = 1_000
    losses = SimulateTrainData(num_paras).train(dataset_size, num_steps)
    assert losses[0] > losses[1] > losses[2], losses

