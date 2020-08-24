import csv

def import_year_topics(fname):
    out = {}
    with open(fname, 'r') as f:
        for e in csv.reader(f):
            topic_num = int(e[0])
            topics = dict([tuple(element.split(':')) for element in e[1].split()])
            topic_summary = e[2]
            out[topic_num] = (topics, topic_summary)
    f.close()
    return out

def setup(fname):
    out = []
    with open(fname, 'r') as f:
        for row in csv.DictReader(f, skipinitialspace=True):
            article = {k: v for k, v in row.items()}
            words = []
            for e in article['topic'].split():
                word, val = e.split(':')
                words.append((word, val))
            article['topic'] = words
            out.append(article)
        return out

def calculate_similarity_score(topic, article_topic):
    score = 0.0
    for element in article_topic:
        word, val = element
        if word in topic:
            score += float(val)*float(topic[word])
    return score

def match(topics, article_topic):
    score_floor = 0.0005
    l = set()
    for topic in topics:
        sim_score = calculate_similarity_score(topics[topic][0], article_topic)
        if sim_score >= score_floor:
            l.add(topics[topic][1])
    return l

        

if __name__ == '__main__':

    
    for y in range(2020, 2021):
        year = str(y)
        yearly_topics = import_year_topics(year+'_filtered.csv')
        l = []
        for article in setup('Articles_Topics_2020.csv'):
            article_values = match(yearly_topics, article['topic'])
            headline = article['headline']
            print(headline, article_values)
