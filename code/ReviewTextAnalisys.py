# -*- coding: utf-8 -*-

import json
import scipy 
from sklearn.feature_extraction.text import CountVectorizer


#bisogna aggiungere una lista di trigrammi già considerati in questo modo uno 
#stesso trigramma non viene inserito tante volte quanti sono i documenti in cui compare
def getDocuments(vectorizer, review_trigrams, min_value, matrix):
    data_index_document = []
    for trigram in review_trigrams:
        #restituisce l'indice del termine/trigramma nel vocabolario
        index = vectorizer.vocabulary_.get(trigram)
        number_of_repetitions = 0
        #si analizza solo la colonna che fa riferimento allo specifico trigramma, presa tramite index
        #ogni elemento della colonna rappresenta il numero di occorrenze del trigramma in quel documento (riga)
        for el in matrix[:, index]:
            if el>=1:  
                number_of_repetitions+=1
        if number_of_repetitions>min_value:  #se il trigramma compare in almeno "min_value" documenti lo appendo alla lista che ritorna
            data_trigram = {
                'term': trigram,
                'termIndex': index,
                'numberOfRepetitions': number_of_repetitions
            }
            data_index_document.append(data_trigram)
    return data_index_document
  
    
def executeAnalisys(reviews_data):    
    my_stop_words = json.load(open('json/stopwords-it.json'))
    
    reviews_id2body, reviews_body = [], []
    for rev in reviews_data:
        reviews_id2body.append([reviews_data[rev]['reviewId'], reviews_data[rev]['reviewText']])
        reviews_body.append(reviews_data[rev]['reviewText'])
    
    #creazione del count vectorizer dal quale creare i trigrammi
    #ngram_range(x,y) -> crea ngrammi da dimensione x a dimensione y 
        #se x=1 e y=3 ad esempio, crea ngrammi di 1, 2 e 3 termini. a noi servono solo da 3
    trigram_vectorizer = CountVectorizer(ngram_range=(3, 3), stop_words=my_stop_words)
    tv = trigram_vectorizer.fit_transform(reviews_body)
    #print trigram_vectorizer.vocabulary_
    #print tv  #tutte le coppie (indice documento, indice termine) con occorenze del termine nel doc
    
    #crea la matrice sparsa degli elementi e la trasforma in array
    m = scipy.sparse.csr_matrix(tv).toarray()
    review_index, data = 0, {}
    
    #creo l'analizzatore che mi serve per creare i trigrammi
    analyze = trigram_vectorizer.build_analyzer()
    for [rev_id, rev_text] in reviews_id2body:
        #creo i trigrammi
        review_trigrams = analyze(rev_text)
        data_index_document = getDocuments(trigram_vectorizer, review_trigrams, 2, m)
        if data_index_document<>[]:  #se almeno uno dei trigrammi della recensione è ripetuto lo salvo. altrimenti ignoro
            data_review = {
                rev_id: {
                    'reviewBody': rev_text,
                    'reviewTrigrams': review_trigrams,
                    'numberOfRepeatedTrigrams': len(data_index_document),
                    'dataIndexDocument': data_index_document
                }
            }
            data = dict(data.items() + data_review.items())
        review_index+=1
    
    return data
 