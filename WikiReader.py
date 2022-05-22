import xml.sax
import nltk
import string
from nltk.stem.porter import PorterStemmer
import os


def textPreprocessing(content):
    # The first step is to remove punctuation chars
    text = content.translate(str.maketrans('','',string.punctuation))

    # Second step is to tokenize
    words = nltk.word_tokenize(text)

    # 3rd step lowering the text
    words = [word.lower() for word in words]

    # 4th step is to remove stop words
    stopWords = nltk.corpus.stopwords.words('english')
    words = [word for word in words if word not in stopWords]

    # Final step stemming
    # porterStemmer = PorterStemmer()
    # words=[porterStemmer.stem(word) for word in words]
    # TODO which stemmer would be the best?
    # snowBallStemmer=nltk.stem.SnowballStemmer('english')
    # words=[snowBallStemmer.stem(word) for word in words]

    return words


class WikiReader(xml.sax.handler.ContentHandler):

    def __init__(self) -> None:
        super().__init__()
        self.id = ""
        self.title = ""
        self.url = ""
        self.content = ""


    def startElement(self, name, attrs):
        if name != "doc":
            return

        self.id = attrs.get('id')
        self.title = attrs.get('title')
        self.url = attrs.get('url')



    def endElement(self, name):
        if name != "doc":
            return

        preprocessedContent = textPreprocessing(self.content)
        self.writeProccessedArticle(preprocessedContent)
        self.__cleanup()

    def writeProccessedArticle(self,newContent):
        try:
            with open("preprocessed_texts/"+self.title+".txt","w", encoding="utf-8") as f:
                f.write(f"{self.id},{self.title},{self.url}, \n")
                for index,word in enumerate(newContent):
                    if index == len(newContent)-1:
                        f.write(word)
                    else:
                        f.write(word+",")
        except FileNotFoundError:
            print(f"File article contains forbidden signs")

    def characters(self, content):
        self.content += content

    def __cleanup(self):
        self.id = ""
        self.title = ""
        self.url = ""
        self.content = ""


def main():
    print(f'Preprocessing xml to txt files \n')
    handler = WikiReader()
    xml.sax.parse('text/AA/full.xml', handler)


if __name__ == '__main__':
    main()

