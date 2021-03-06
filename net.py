import numpy as np
import layers

class Net:
    def __init__(self):
        self.layers = []
        self.outputs = []

    def add(self, layer):
        self.layers.append(layer)

    def compile(self):
        for i, l in enumerate(self.layers):
            if i == 0:
                if l.input_size == 0:
                    print("First layer's input size must be specified")
                continue
            l.input_size = self.layers[i-1].output_size
            if l.output_size == 0:
                l.output_size = l.input_size

        for l in self.layers:
            print('({}, {})'.format(l.input_size, l.output_size))

    def forward(self, input):
        self.outputs = []
        self.outputs.append(input)
        for l in self.layers:
            out = l.forward(self.outputs[-1])
            self.outputs.append(out)

        return self.outputs[-1]

    def backprop(self, labels):
        total_loss = 0.0
        gradient = None
        out = self.outputs[-1]

        for l in reversed(self.layers):
            output = self.outputs.pop()
            input = self.outputs[-1]
            if gradient is None:
                new_grad, loss = l.backward(input, output, labels)
            else:
                new_grad, loss = l.backward(input, output, gradient)
            total_loss += loss
            gradient = new_grad

        total_loss += self.layers[-1].get_loss(out, labels)
        return total_loss

    def update(self, step_size):
        for l in self.layers:
            l.update(step_size)

    def predict(self, input):
        output = self.forward(input)
        return np.argmax(output, axis=1)
