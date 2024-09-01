import pandas as pd

class Forecaster():

    def __init__(self, dataset, method: str):
        self.dataset = dataset
        self.method = method

     