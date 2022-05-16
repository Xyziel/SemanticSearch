from sklearn.metrics import pairwise_distances


class SemanticSearch:
    def __init__(self, distance_type: str):
        self.distance_type = distance_type

    def get_distance(self, v1: list, v2: list) -> list:
        return pairwise_distances(v1, v2, self.distance_type)
