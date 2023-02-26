import pickle
from typing import List

import numpy as np
import torch
from transformers import AutoTokenizer, BertForSequenceClassification


def predict_categories_on_single_text(text, model, tokenizer, mlb, proba_threshold=0.5):

    encoding = tokenizer(text, return_tensors="pt")
    encoding = {k: v.to(model.device) for k, v in encoding.items()}

    outputs = model(**encoding)
    logits = outputs.logits

    # apply sigmoid + threshold
    sigmoid = torch.nn.Sigmoid()
    probs = sigmoid(logits.squeeze().cpu())
    # predictions = probs.detach().numpy()
    predictions = np.zeros(probs.shape)
    predictions[np.where(probs >= proba_threshold)] = 1

    classes = mlb.inverse_transform(predictions.reshape(1, -1))

    if len(classes) > 0:
        classes = classes[0]
    else:
        classes = []

    return classes, probs


def load_models(
    multilabel_model_path="categories", multilabel_binarizer_path="mlb.pkl"
):
    model = BertForSequenceClassification.from_pretrained(
        multilabel_model_path, problem_type="multi_label_classification"
    )

    tokenizer = AutoTokenizer.from_pretrained(multilabel_model_path)

    with open(multilabel_binarizer_path, "rb") as handle:
        mlb = pickle.load(handle)

    return model, tokenizer, mlb


def predict_categories(queries: List[str], model, tokenizer, mlb, proba_threshold=0.45):

    categories = []

    for query in queries:
        cat, probs = predict_categories_on_single_text(
            query, model, tokenizer, mlb, proba_threshold=proba_threshold
        )

        categories.extend(cat)

    # return sorted(categories.items())
    return sorted(set(categories))
