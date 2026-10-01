import numpy as np

class SimpleTrainDataSimulator:
    def __init__(self, num_paras, vocab_size=100, embed_dim=12):
        self.num_paras = num_paras
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.capacity = self.calculate_capacity_from(num_paras)

    def calculate_capacity_from(self, num_paras):
        capacity = np.log(num_paras) / 10.0
        return capacity
        
    def train(self, num_datasize, num_steps):
        pass

if __name__ == "__main__":
    num_datasize, num_steps = 10_000, 1_000
    losses = [
        SimpleTrainDataSimulator(num_paras).train(num_datasize, num_steps) for num_paras in (10, 100, 1000)]
    assert losses[0] > losses[1] > losses[2], losses