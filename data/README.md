# Vector indexation

For vector indexation, we used `sentence-transformers/all-distilroberta-v1` and included the authors to the embedding vector. We then upserted all the embeddings onto the Redis database.

The data was pre-processed by removing unicode characters,  punctuation, newlines, lowercasing and some spacing cleanup.

You can check the [reference notebook](https://github.com/liram11/untitled1-vector-search/tree/master/data/embeddings).

# Training a multilabel model

We decided to train a multilabel classification model as each paper can have more than one category. We fine-tuned a transformers model  (`bert-base-uncased`) on a sample of 400 000 papers and tried it with and without the evaluation. From the outcomes, we can see that the preprocessing function - same as the prior step - managed to improve the model results. 

For running it, you can check [the training notebook.](https://github.com/liram11/untitled1-vector-search/blob/master/data/multilabel_classifier/multilabel-model.ipynb).

There are a few inference examples in a [notebook as well.](https://github.com/liram11/untitled1-vector-search/blob/master/data/multilabel_classifier/multilabel-inference.ipynb)
