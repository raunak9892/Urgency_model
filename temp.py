
from transformers import TFDistilBertForSequenceClassification
import tensorflow as tf
from transformers import DistilBertTokenizer
import pandas as pd


tokenizer_fine_tuned = DistilBertTokenizer.from_pretrained("./saved_model")
model_fine_tuned = TFDistilBertForSequenceClassification.from_pretrained("./saved_model")
def run_model():
    text = pd.read_csv('emails.csv')
    text = text['description']
    for i in range(len(text)):
     predict_input = tokenizer_fine_tuned.encode(
     str(text[i]),
     truncation = True,
     padding = True,
     return_tensors = 'tf'
  )
     output = model_fine_tuned(predict_input)[0]

     prediction_value = tf.argmax(output, axis = 1).numpy()[0]
     



    

