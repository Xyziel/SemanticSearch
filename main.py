from SemanticSearch import SemanticSearch
import os
from SemanticSearchGUI import SemanticSearchGUI


VECTORIZERS = ["Tfidf", "BoW"]
DECOMPOSERS = ["SVD", "LDiA", "PCA"]
DISTANCES = ["l1", "l2", "cosine"]


def main():
    corpus = []
    titles = []
    urls = []
    ids = []
    directory = "texts"

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            with open(f, encoding="utf-8") as file:
                content = file.read()
                content_array = content.split(",")
                ids.append(content_array[0])
                titles.append(content_array[1])
                urls.append(content_array[2])
                corpus.append(" ".join(content_array[3:]))
    ss = SemanticSearch(corpus, urls, titles, "l2", "tfidf", "pca", 2)
    gui = SemanticSearchGUI(DISTANCES, VECTORIZERS, DECOMPOSERS, ss)
    gui.run()


if __name__ == '__main__':
    main()
