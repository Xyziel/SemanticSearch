
import dearpygui.dearpygui as dpg
from SemanticSearch import SemanticSearch
import dearpygui.demo as demo
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

    # with open("NewYork.txt") as file:
    #     corpus.append(file.read())
    # with open("YorkAustralia.txt") as file:
    #     corpus.append(file.read())
    # with open("YorkEngland.txt") as file:
    #     corpus.append(file.read())
    # titles = ["NY", "YA", "YE"]
    # urls = ["1", "2", "3"]

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
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

    # dpg.create_context()
    # dpg.create_viewport(title='Semantic Search Engine', width=700, height=500)
    # demo.show_demo()
    # dpg.setup_dearpygui()
    # dpg.show_viewport()
    # dpg.start_dearpygui()
    # dpg.destroy_context()


if __name__ == '__main__':
    main()
