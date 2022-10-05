import re
import string

from sentence_transformers import SentenceTransformer


class Embeddings:
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

    # String cleaner
    @staticmethod
    def clean_description(description: str) -> str:
        if not description:
            return ""
        # remove unicode characters
        description = description.encode('ascii', 'ignore').decode()

        # remove punctuation
        description = re.sub('[%s]' % re.escape(string.punctuation), ' ', description)

        # clean up the spacing
        description = re.sub('\s{2,}', " ", description)

        # remove newlines
        description = description.replace("\n", " ")

        # split on capitalized words
        description = " ".join(re.split('(?=[A-Z])', description))

        # clean up the spacing again
        description = re.sub('\s{2,}', " ", description)

        # make all words lowercase
        description = description.lower()

        return description


    def make(self, sentences: list):
        if isinstance(sentences, list):
            sentences = [self.clean_description(description) for description in sentences]
        else:
            sentences = self.clean_description(sentences)
        return self.model.encode(sentences, normalize_embeddings=True)