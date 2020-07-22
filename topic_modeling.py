import csv
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


no_features = 1000
no_topics = 20
no_top_words = 15

MONTH_DICT = {1: 'Jan.', 2: 'Feb.', 3: 'Mar.', 4: 'Apr.', 5: 'May', 6: 'Jun.', 7: 'Jul.', 8: 'Aug.', 9: 'Sep.', 10: 'Oct.', 11: 'Nov.', 12: 'Dec.'}
TEST_STRING = "Mayor Bill de Blasio’s administration is expected on Tuesday to add the Lunar New Year to the New York public school calendar, allowing the city’s Asian families to celebrate an important holiday with their children without tarnishing attendance records.Mr. de Blasio, a Democrat, pledged to make the change during the 2013 mayoral campaign, but by agreeing to the move now, he avoids a potentially political embarrassment. With a pending bill in Albany that would have added the holiday to the calendar, the mayor faced the uncomfortable prospect of the State Legislature’s enacting his own campaign pledge for him, without the imprimatur of City Hall.The Lunar New Year is celebrated throughout many parts of Asia. When it falls on a school day, some city schools with large Asian populations have more than half their students absent that day.“Finally, students of Asian descent will not be forced to choose between observing the most important holiday of the year and missing important academic work,” Councilwoman Margaret Chin, a Democrat of Lower Manhattan, said in a statement. “Lunar New Year is a deeply important cultural observance for nearly 15 percent of public school students, and this designation gives Lunar New Year the respect and recognition it has long deserved.”This move comes just three months after the de Blasio administration added two Muslim holy days to the school calendar, Eid al-Fitr and Eid al-Adha. Mr. de Blasio’s predecessor, Mayor Michael R. Bloomberg, had declined to do so, saying children needed more time in school.In New York State, schools must have at least 180 days of instruction each year. To accommodate the new time off without losing time in the classroom, the de Blasio administration said it planned to convert two half-days to full days. The new schedule will go into effect this coming school year, with the holiday falling on Feb. 8.State Senator Daniel L. Squadron, a Democrat whose district includes Manhattan’s Chinatown, said the inclusion of the holiday signaled, in part, the increased political presence of the city’s Asian community.“There’s no question this reflects the changing city and the changing significance of the holiday to this city,” Mr. Squadron said.New York is not the first city to add this holiday to its school calendar. Public schools in San Francisco, for example, have observed the holiday for several years.The de Blasio administration made the announcement about Lunar New Year on Twitter on Monday evening, saying it was “working toward a more inclusive city.” The city also posted the news in traditional Chinese and Korean."

def setup(fname):
    """
    This function is specific to me because I'm loading in files in this directory
    """
    with open(fname) as f:
        return [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
    

def create_dataset(articles):
    """
    parameters: the list of article dictionaries
    returns list of texts
    """
    return [clean_string(article['text']) for article in articles]

def clean_string(text):
    """
    Helper function that takes in an article text as a string
    Returns: new string with article text cleaned up, punctuation and stop words removed
    """
    ps = PorterStemmer()
    punct = '?.,!\n1234567890'
    useless_words = {'mr', 'mrs', 'ms', 'dr', 'said', 'says', "new",'yorker', 'yorkers','york', 'city', 'de', 'blasio', 'council', 'bill', 'mayor', 'quinn', 'bloomberg', 'yearly', 'years', 'year', 'also', 'would', 'could'}
    text = text.lower()
    for p in punct:
        text = text.replace(p, ' ')
    stop_words = set(stopwords.words('english'))|useless_words
    word_tokens = word_tokenize(text)
    new_toks = []
    for tok in word_tokens:
        if len(tok) > 1 and tok not in stop_words:
            new_toks.append(ps.stem(tok))
    
    # return new_toks
    new_text = ''
    for token in new_toks:
        new_text += token+' '
    return new_text.strip()
    
    

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
        print('successfully written to file: '+filename)

if __name__ == '__main__':
    #Tests:


    
    ##monthly topics:

    # for y in range(2013, 2021):
    #     year = str(y)
    #     months  = {'01': [], '02': [], '03': [], '04': [], '05': [], '06': [], '07': [], '08': [], '09': [], '10': [], '11': [], '12': []}
    #     articles = setup('New_Articles_'+year+'.csv')
    #     for a in articles:
    #         date = a['date_published'][0:2]
    #         months[date].append(a)
    #     all_topics = []
    #     for k, v in months.items():
    #         if v:
    #             documents = create_dataset(v)
    #             lda, tf_feature_names = run_lda(documents)
    #             lda_topics = display_topics(lda, tf_feature_names, no_top_words)
    #             all_topics+= [(MONTH_DICT[int(k)],)]
    #             all_topics+=lda_topics
    #     write_results_to_csv(all_topics, 'Month_by_Month_LDA_'+year+'.csv')

    """
    Here are NMF tests by year!!!
    """
    for y in range(2013,2021):
        year = str(y)
        articles = setup('New_Articles_'+year+'.csv')
        documents = create_dataset(articles)
        # train_texts = create_dataset(articles)
        # dictionary = Dictionary(train_texts)
        # corpus = [dictionary.doc2bow(text) for text in train_texts]
        # hdpmodel = HdpModel(corpus=corpus, id2word=dictionary)
        # hdptopics = display(hdpmodel.show_topics(formatted = False))
        # write_results_to_csv(hdptopics, 'HDP_'+str(y)+'.csv')
        # lda, tf_feature_names = run_lda(documents)
        # lda_topics = display_topics(lda, tf_feature_names, no_top_words)
        # write_results_to_csv(lda_topics, 'LDA_'+str(y)+'.csv')
        nmf, feature_names = run_nmf(documents)
        nmf_topics = display_topics(nmf, feature_names, no_top_words)
        write_results_to_csv(nmf_topics, 'NMF_'+str(y)+'.csv')



    # articles = setup('New_Articles_2019.csv')
    # train_texts = create_dataset(articles)
    # dictionary = Dictionary(train_texts)
    # corpus = [dictionary.doc2bow(text) for text in train_texts]
    # hdpmodel = HdpModel(corpus=corpus, id2word=dictionary)
    # print(display(hdpmodel.show_topics(formatted = False)))
    # ldamodel = LdaModel(corpus=corpus, num_topics=20, id2word=dictionary)
    # print(display(ldamodel.show_topics(formatted = False)))
    
    # for i in range(5,31):
    #     no_topics = i
    #     lda, tf_feature_names = run_lda(documents)
    #     lda_topics = display_topics(lda, tf_feature_names, no_top_words)
    #     write_results_to_csv(lda_topics, 'LDA_'+str(i)+'_topics.csv')
