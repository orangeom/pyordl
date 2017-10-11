import numpy as np
import layers

class Net:
    def __init__(self):
        self.layers = []
        self.outputs = []
    
    def add_layer(self, layer):
        self.layers.append(layer)

    def forward(self, input):
        self.outputs = []
        self.outputs.append(input)
        for i, l in enumerate(self.layers):
            if i == 0:
                out = l.forward(input)
            else:
                out = l.forward(self.outputs[-1])
            self.outputs.append(out)

        return self.outputs[-1]

    def backprop(self, labels):
        total_loss = 0.0
        gradient = None

        for l in reversed(self.layers):
            output = self.outputs.pop()
            input = self.outputs[-1]
            if gradient is None:
                new_grad, loss = l.backward(input, output, labels)
            else:
                new_grad, loss = l.backward(input, output, gradient)
            total_loss += loss
            gradient = new_grad

        return total_loss

    def update(self, reg, step_size):
        for l in self.layers:
            l.update(reg, step_size)

    def predict(self, input):
        output = self.forward(input)
        return np.argmax(output, axis=1)