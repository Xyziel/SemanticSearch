import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD, PCA, LatentDirichletAllocation


class SemanticSearch:
    def __init__(self, corpus: list, urls: list, topics: list, distance_type="l2", vectorizer="tfidf", decomposer="pca", n_components=5):
        if len(urls) == 0 or len(urls) != len(corpus):
            print("Error: wrong size of urls array")
            exit(-1)
        if len(topics) == 0 or len(topics) != len(corpus):
            print("Error: wrong size of topics array")
            exit(-1)
        if len(corpus) == 0:
            print("Error: empty corpus")
            exit(-1)
        self.corpus = corpus
        self.urls = urls
        self.topics = topics
        self.n_components = n_components
        self.distance_type = distance_type
        self.vectorizer = self.set_vectorizer(vectorizer)
        self.decomposer = self.set_decomposer(decomposer)
        self.model = self.prepare_model()

    def set_vectorizer(self, vectorizer_name: str):
        if vectorizer_name == "tfidf":
            vectorizer = TfidfVectorizer()
        else:
            vectorizer = CountVectorizer()
        return vectorizer

    def set_decomposer(self, decomposer_name: str):
        if decomposer_name == "svd":
            decomposer = TruncatedSVD(n_components=self.n_components)
        elif decomposer_name == "ldia":
            decomposer = LatentDirichletAllocation(n_components=self.n_components)
        else:
            decomposer = PCA(n_components=self.n_components)
        return decomposer

    def prepare_model(self):
        corpus_vectorized = self.vectorizer.fit_transform(self.corpus).toarray()
        return self.decomposer.fit_transform(corpus_vectorized)

    def get_distances(self, X: list, y: list) -> list:
        return pairwise_distances(X, y, self.distance_type)

    def get_n_min_indexes(self, vector: list, n=1):
        vector = np.array(vector)
        vector = vector.flatten()
        return vector.argsort()[:n]

    def transform_question(self, question):
        question_vector = self.vectorizer.transform([question]).toarray()
        return self.decomposer.transform(question_vector)

    def set_attributes(self, attr_dict):
        if attr_dict["n_components"] == 0:
            self.n_components = None
        else:
            self.n_components = attr_dict["n_components"]
        self.distance_type = attr_dict["distance"]
        self.vectorizer = self.set_vectorizer(attr_dict["vectorizer"])
        self.decomposer = self.set_decomposer(attr_dict["decomposer"])

    def search(self, question, n_articles) -> list:
        transformed_question = self.transform_question(question)
        distances = self.get_distances(self.model, transformed_question)
        best_indexes = self.get_n_min_indexes(distances, n_articles)
        responses = []
        for index in best_indexes:
            responses.append((self.topics[index], self.urls[index]))
        return responses
