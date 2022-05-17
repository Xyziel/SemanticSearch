import dearpygui.dearpygui as dpg
import webbrowser


class SemanticSearchGUI:

    def __init__(self, distances: list, vectorizers: list, decomposers: list, engine):
        self.distances = distances
        self.vectorizers = vectorizers
        self.decomposers = decomposers
        self.engine = engine

    def get_user_data(self):
        user_data = {"question": dpg.get_value("question").lower(),
                     "distance": dpg.get_value("distance").lower(),
                     "vectorizer": dpg.get_value("vectorizer").lower(),
                     "decomposer": dpg.get_value("decomposer").lower(),
                     "n_components": dpg.get_value("n_components")}
        return user_data

    def open_wiki_link(self, sender, app_data, user_data):
        webbrowser.open_new_tab(user_data)

    def add_text_and_href(self, response, index):
        dpg.add_text(response[0], pos=(22, index*60), parent="outputs", color=(255, 150, 50))
        dpg.add_button(label=response[1], pos=(20, 25+index*60), height=27, parent="outputs", callback=self.open_wiki_link, user_data=response[1])

    def refresh_output(self):
        dpg.delete_item("outputs", children_only=True)

    def search(self):
        self.refresh_output()
        user_data = self.get_user_data()
        n_articles = dpg.get_value("n_articles")
        self.engine.set_attributes(user_data)
        self.engine.model = self.engine.prepare_model()
        responses = self.engine.search(user_data["question"], n_articles)
        for index, response in enumerate(responses):
            self.add_text_and_href(response, index+1)

    def run(self):
        window_width = 400
        window_height = 600

        dpg.create_context()
        dpg.create_viewport(title='Semantic Search Engine', width=2*window_width, height=window_height)

        with dpg.font_registry():
            default_font = dpg.add_font("fonts/coolvetica rg.otf", 20)

        with dpg.window(label="Input", width=window_width, height=window_height, no_resize=True, no_title_bar=True, no_move=True, pos=(0,0)):
            dpg.bind_font(default_font)
            dpg.add_text("Welcome, please type your question down below:")
            dpg.add_text("")
            dpg.add_text("Question:", color=(255, 100, 0))
            dpg.add_input_text(hint="your question", tag="question", width=int(0.85*window_width))
            dpg.add_text("")
            dpg.add_text("Distance type:")
            dpg.add_combo(self.distances, default_value="cosine", tag="distance", width=int(0.85*window_width))
            dpg.add_text("Vectorizer type:")
            dpg.add_combo(self.vectorizers, default_value="Tfidf", tag="vectorizer", width=int(0.85*window_width))
            dpg.add_text("Decomposer type:")
            dpg.add_combo(self.decomposers, default_value="PCA", tag="decomposer", width=int(0.85*window_width))
            dpg.add_text("Number of components (if 0 then default None):")
            dpg.add_slider_int(default_value=5, max_value=30, min_value=0, tag="n_components", width=int(0.85*window_width))
            dpg.add_text("")
            dpg.add_text("Number of proposed articles:")
            dpg.add_slider_int(default_value=3, min_value=1, max_value=10, tag="n_articles", width=int(0.85*window_width))
            dpg.add_text("")
            dpg.add_button(label="Search", width=80, height=30, pos=(int(0.35*window_width), 510), callback=self.search)
        with dpg.window(label="Output", tag="output_window", width=window_width, height=window_height, no_resize=True, no_title_bar=True, no_move=True, pos=(400,0)):
            dpg.add_text("Proposed articles:", pos=(20, 10))
            with dpg.group(tag="outputs"):
                pass

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
