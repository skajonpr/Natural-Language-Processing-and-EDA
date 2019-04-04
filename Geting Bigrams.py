import re
import nltk
import string


# This funciton is to get most frequent bigrams from reviews in a dataframe.
def get_bigrams(df, N, indv_rating_1 = None, indv_rating_2 = None):
    
    # a list of negative words
    negations = ['no','nor','not','too','don',"don't",'ain','aren',"aren't",'couldn',"couldn't",\
    'didn',"didn't",'doesn','isn',"isn't",'wasn',"wasn't",'weren',"weren't"]
    
    # Call stopwords and remove negative words from them
    stop_words = nltk.corpus.stopwords.words('english')
    stop_words = [word for word in stop_words if not word in negations]
    
    # Get a list of all reviews
    list_of_reviews = df[(df['indv_rating'].apply(float)==indv_rating_1) | \
                  (df['indv_rating'].apply(float)==indv_rating_2)].review.values.tolist()
    # Get a string of text
    text = " ".join(list_of_reviews).lower()
    # Create pattern
    pattern=r'\w[\w\'-]*\w'                        
    # Get tokens
    tokens = nltk.regexp_tokenize(text, pattern)
    # Remove stopwords from tokens
    filtered_tokens = [token for token in tokens if not token in stop_words]
    # Get bigrams
    bigrams=list(nltk.bigrams(filtered_tokens))
    # get freqent bigrams    
    frequent_bigram = {bigram:bigrams.count(bigram) for bigram in set(bigrams)}
    
    # return top N frequent bigrams
    return sorted(frequent_bigram.items(), key=lambda x: x[1])[::-1][:N]
