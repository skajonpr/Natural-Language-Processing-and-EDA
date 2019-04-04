import re
import nltk
import string

# This funciton is to get most frequent trigrams from reviews in a dataframe.
def get_trigrams(df, N, indv_rating_1 = None, indv_rating_2 = None):
    
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
    # Get trigrams
    trigrams=list(nltk.trigrams(filtered_tokens))
    # get freqent trigrams      
    frequent_trigram = {trigram:trigrams.count(trigram) for trigram in set(trigrams)}
    # return top N frequent trigrams
    return sorted(frequent_trigram.items(), key=lambda x: x[1])[::-1][:N]