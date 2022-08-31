import re
import string

from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F


# Load model from HuggingFace Hub
tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")
model = AutoModel.from_pretrained("allenai/scibert_scivocab_uncased")

# String cleaner
def clean_description(description: str):
    if not description:
        return ""
    # remove unicode characters
    description = description.encode('ascii', 'ignore').decode()

    # remove punctuation
    description = re.sub('[%s]' % re.escape(string.punctuation), ' ', description)

    # clean up the spacing
    description = re.sub('\s{2,}', " ", description)

    # remove urls
    #description = re.sub("https*\S+", " ", description)

    # remove newlines
    description = description.replace("\n", " ")

    # remove all numbers
    #description = re.sub('\w*\d+\w*', '', description)

    # split on capitalized words
    description = " ".join(re.split('(?=[A-Z])', description))

    # clean up the spacing again
    description = re.sub('\s{2,}', " ", description)

    # make all words lowercase
    description = description.lower()

    return description


# Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

# Function to make embeddings
def make(sentences: list):
    # Clean
    if isinstance(sentences, list):
        sentences = [clean_description(description) for description in sentences]
    else:
        sentences = clean_description(sentences)

    # Tokenize sentences
    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)

    # Perform pooling
    embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

    # Normalize embeddings
    embeddings = F.normalize(embeddings, p=2, dim=1)

    print("Sentence embeddings:")
    return embeddings