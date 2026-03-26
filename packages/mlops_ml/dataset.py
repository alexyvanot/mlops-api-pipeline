from sklearn.datasets import load_iris


FEATURE_NAMES = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
]


def load_training_data() -> tuple[list[list[float]], list[int]]:
    dataset = load_iris()
    return dataset.data.tolist(), dataset.target.tolist()
