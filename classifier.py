import textblob
import re
import spacy
import nltk
import pandas as pd


from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
df = pd.read_csv('emails.csv')

def tense(text):
# Create a spaCy nlp object
# Create a POS tagger
 tagger = pos_tag(word_tokenize(text))
 print(tagger)
 score=0
 ver=0
# Tag the words in the sentence
# Get the POS tag for the verb
# Determine the verb tense
 for y in tagger:
  x=y[1]
  if x== "VBP":
   #print("The verb tense is present progressive.")
   score = score + 1
   ver = ver+1
  elif x == "VBD":
   #print("The verb tense is past tense.")
   score = score + 0.3
   ver = ver+1
  elif x== "VBZ" or x== "VB":
   #print("The verb tense is present tense.")
   score = score + 0.5
   ver = ver+1
  elif x == "VBG":
   score = score + 1
   ver = ver+1
   #print("The verb tense is present participle.")
  elif x == "VBN":
   #print("The verb tense is past participle.")
   score = score + 0.25
   ver = ver+1
 return score,ver



# Define a function to perform tonal urgency analysis
def tonal_urgency_analysis(text):
  """Returns the tonal urgency of the given text as a string."""
  text = str(text)

  # Create a TextBlob object
  blob = textblob.TextBlob(text)

  # Extract all verbs from the text
  verbs = re.findall(r"\w+s", text)
  print(verbs)

  # Calculate the urgency score for each verb
  urgency_scores = []
  # Calculate the overall tonal urgency score
  score= tense(text)
  print(score)
  if score[0]==0 or score[1]==0:
    tonal_urgency_score=0
  else:  
   tonal_urgency_score = score[0]/score[1]

  # Determine the tonal urgency level
  if tonal_urgency_score > 0.8:
    return " Very Urgent"
  elif tonal_urgency_score > 0.65:
    return "Urgent"
  elif tonal_urgency_score < 0.2:
    return "Non-urgent"
  else:
    return "Neutral"

# Define a function to calculate the urgency score of a verb


# Example usage:
df['urgency'] = df['description'].apply(tonal_urgency_analysis)
# Reset the index of the DataFrame
df.reset_index(drop=True, inplace=True)
# Save the updated DataFrame to a new CSV file
df.to_csv('updated_email.csv',index=False) 