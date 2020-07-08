import csv
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

no_features = 1000
no_topics = 20
no_top_words = 10

def setup():
    """
    This function is specific to me because I'm loading in files in this directory
    """
    articles = []
    for i in range(2013, 2021):
        with open(str(i)+'_Articles.csv') as f:
            articles += [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
    return articles

def create_dataset(articles):
    """
    parameters: the list of article dictionaries
    returns list of texts
    """
    return [article['text'] for article in articles]

def run_lda(documents):
    """
    Runs LDA on the list of article texts
    """
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
    tf = tf_vectorizer.fit_transform(documents)
    tf_feature_names = tf_vectorizer.get_feature_names()
    lda = LatentDirichletAllocation(n_components=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
    return (lda, tf_feature_names)

def run_nmf(documents):
    """
    Runs NMF on the list of article texts
    """
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
    tfidf = tfidf_vectorizer.fit_transform(documents)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    nmf = NMF(n_components=no_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)
    return (nmf, tfidf_feature_names)

def display_topics(model, feature_names, no_top_words):
    """
    returns a list of tuples in the following format: (topic 1, [insert topic data here])
    """
    out = []
    for i, topic in enumerate(model.components_):
        top = "Topic %d:" % (i)
        topic_data = " ".join([feature_names[ind] for ind in topic.argsort()[:-no_top_words - 1:-1]])
        out.append((top, topic_data))
    return out

def write_results_to_csv(topic_text, filename):
    """
    parameters: the output from displat_topics, intended filename

    Writes the topic data to a csv file
    """
    with open(filename, 'w') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerow(('Topic #:', 'topic data:'))
        for topic in topic_text:
            wr.writerow(topic)

if __name__ == '__main__':
    #Tests:
    articles = setup()
    documents = create_dataset(articles)
    lda, tf_feature_names = run_lda(documents)
    nmf, tfidf_feature_names = run_nmf(documents)
    nmf_topics = display_topics(nmf, tfidf_feature_names, no_top_words)
    lda_topics = display_topics(lda, tf_feature_names, no_top_words)
    write_results_to_csv(nmf_topics, 'NMF_Results.csv')
    write_results_to_csv(lda_topics, 'LDA_Results.csv')
    
    