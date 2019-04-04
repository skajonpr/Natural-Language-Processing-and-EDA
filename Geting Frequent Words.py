import pandas as pd 
import numpy as np
import seaborn as sns
import nltk
import string
import matplotlib.pyplot as plt
import en_core_web_sm
from wordcloud import WordCloud
nlp = en_core_web_sm.load()




# this function is to get either Noun or Adjective from the entered string(text).
def get_words(text, get_noun = True, get_adj = True):
    
    # Strip punctuation from string and lowercase the string
    text = " ".join([token.strip(string.punctuation) for token in text.split()]).lower()
    
    # Define a text to Spacy
    doc = nlp(text)
    
    # call stopwords
    stop_words = nltk.corpus.stopwords.words('english')
    
    words = []
    # Loop through each word in the text.
    for token in doc:
        # Get only adjective
        if (get_adj == True) and (get_noun == False):
            if (not token.text in string.punctuation) and (not token.is_space) \
                    and (not token.text in stop_words) and ((token.pos_ == 'ADJ')):   
                        words.append(token.lemma_)
        # Get only Noun
        elif (get_adj == False) and (get_noun == True):
            if (not token.text in string.punctuation) and (not token.is_space) \
                    and (not token.text in stop_words) and ((token.pos_ == 'NOUN')):   
                        words.append(token.lemma_)
        # Get Both Noun and Adjective
        elif (get_adj == True) and (get_noun == True):
            if (not token.text in string.punctuation) and (not token.is_space) \
                    and (not token.text in stop_words) and ((token.pos_ == 'ADJ'\
                                                           or token.pos_ == 'NOUN')):   
                        words.append(token.lemma_)
        else:
            return "Nothing"
     # Return a list of words   
    return words
    
# This function is to get frequent words of either noun or adjective from a dataframe of reviews
# with specified individual ratings.
def get_frequent_word(df, indv_rating_1 = None,indv_rating_2 = None, get_noun = True, get_adj = True):
    # Get all reviews from a dataframe into a list
    list_of_reviews = df[(df['indv_rating'].apply(float)==indv_rating_1) | \
                      (df['indv_rating'].apply(float)==indv_rating_2)].review.values.tolist()
    
    # get words by calling get_word function.
    tokenized_rating = get_words(" ".join(list_of_reviews), get_noun, get_adj)
    # Count all frequent words
    docs_tokens = {token:tokenized_rating.count(token) for token in set(tokenized_rating)}
     # return a list of top 15 frequent words.
    return sorted(docs_tokens.items(), key=lambda x: x[1])[::-1][:15]

# Get Frequent words from all reviews
def get_frequent_word_all_review(df, N,get_noun = True, get_adj = True):
    # Get all reviews from a dataframe into a list
    list_of_reviews = df.review.values.tolist()
    
    # get words by calling get_word function.
    tokenized_rating = get_words(" ".join(list_of_reviews), get_noun, get_adj)
    # Count all frequent words
    docs_tokens = {token:tokenized_rating.count(token) for token in set(tokenized_rating)}
     # return a list of top 15 frequent words.
    return sorted(docs_tokens.items(), key=lambda x: x[1])[::-1][:N]
    
    
# Call get_frequent_word_all review
Frequent_words = get_frequent_word_all_review(df,N=20, get_noun = False, get_adj = True)
# Get a dataframe of Frequent_words
frequent_word_frequent = pd.DataFrame(Frequent_words)
frequent_word_frequent.columns=["Words", "Frequency"]

# Get a bar chart for frequent words. 
def get_chart_frequent_word(frequent_word_frequent):
    
    sns.set_style("whitegrid");

    plt.figure(figsize=(8,5))
    sns.barplot(x='Words',y='Frequency', data=frequent_word_frequent)
    plt.xticks(rotation=(45))
    plt.show()
    
def create_wordcloud_all_review(df, title= None):
    
    stop_words = nltk.corpus.stopwords.words('english')
    
    list_of_reviews = df.review.values.tolist()
    
    # Get a string of text
    string = " ".join(list_of_reviews).lower()
    # Generate WordCloud
    plt.figure('Review')
    wc = WordCloud(background_color="white", max_words=5000, stopwords=stop_words)              
    wc.generate(string)
    plt.imshow(wc)
    plt.axis('OFF')
    plt.title(title, color = 'b')
    plt.show()