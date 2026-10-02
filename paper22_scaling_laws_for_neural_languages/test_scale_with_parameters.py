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
        return max(loss, 1.0)

def test_scale_with_parameters(SimpleTrainDataSimulator, dataset_size, num_steps):
    losses = [
        SimpleTrainDataSimulator(num_paras).train(dataset_size, num_steps) for num_paras in (10, 100, 1000)]
    print(losses)
    assert losses[0] > losses[1] > losses[2], losses

if __name__ == "__main__":
    num_datasize, num_steps = 10_000, 1_000
    test_scale_with_parameters(SimpleTrainDataSimulator, num_datasize, num_steps)