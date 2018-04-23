# -*- coding: utf-8 -*-

import pandas as pd
#import numpy as np
import json

# transform classes to change raw feature vectors into a representation
# that is more suitable for the downstream estimators
from sklearn import preprocessing

# matrix decomposition algorithms
#from sklearn.decomposition import PCA

# anomaly detection algorithms
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM


# An estimation of anomaly population of the dataset (necessary for several algorithm)
outliers_fraction = 0.1


# create a pandas data frame
# it makes the execution of the anomaly detection algorithms below simpler
def makeDataFrame(asin):
    data = json.load(open('json/analisi_' + asin + '.json'))
    print len(data)
    # dictionary with 9 features
    review_dict = {
            'idReview': [],
            'shortAndRepetitive': [],
            'verifiedPurchase': [],
            'reviewByUser': [],
            'variance': [],
            'reviewDate': [],
            'repeatedTrigrams': [],
            'reviewLength': [],
            'reviewHelpfulness': [],
            'vineReview': []
            }

    # populate the dictionary previously initialized
    for rev in data:
        scoreDetails = data[rev]['scoreDetails']
        
        review_dict['idReview'].append(rev)
        review_dict['shortAndRepetitive'].append(scoreDetails['shortAndRepetitive'])
        review_dict['verifiedPurchase'].append(scoreDetails['verifiedPurchase'])
        review_dict['reviewByUser'].append(scoreDetails['reviewByUser'])
        review_dict['variance'].append(scoreDetails['variance'])
        review_dict['reviewDate'].append(scoreDetails['reviewDate'])
        review_dict['repeatedTrigrams'].append(scoreDetails['repeatedTrigrams'])
        review_dict['reviewLength'].append(scoreDetails['reviewLength'])
        review_dict['reviewHelpfulness'].append(scoreDetails['reviewHelpfulness'])
        review_dict['vineReview'].append(scoreDetails['vineReview'])
    
    df = pd.DataFrame(review_dict)
    return df
  

# create a dictionary to easier manage data
def structData (df):
    reviews = {}
    for i in range(0, len(df)):
        data = {
                df['idReview'][i]: {
                        'shortAndRepetitive': df['shortAndRepetitive'][i],
                        'verifiedPurchase': df['verifiedPurchase'][i],
                        'reviewByUser': df['reviewByUser'][i],
                        'variance': df['variance'][i],
                        'reviewDate': df['reviewDate'][i],
                        'repeatedTrigrams': df['repeatedTrigrams'][i],
                        'reviewLength': df['reviewLength'][i],
                        'reviewHelpfulness': df['reviewHelpfulness'][i],
                        'vineReview': df['vineReview'][i],
                        'class': str(df['class'][i])
                        }
                }
        reviews = dict(reviews.items() + data.items())
    return reviews
                

# save recults in a dictionary useful to print results on a json form
def getResult(data_frame, values):
    reviews = structData(data_frame)    
    
    classes, counters = {}, {}
    for v in values:
        c = { v: { 'elementsNumber':'', 'reviews':{} } }
        classes = dict(classes.items() + c.items())
        counters = dict(counters.items() + {v: 0}.items())
    
    for rev in reviews:
        temp = { rev: reviews[rev] }     
        for v in values:
            if temp[rev]['class'] == v:
                classes[v]['reviews'] = dict(classes[v]['reviews'].items() + temp.items())
                counters[v] = counters[v] + 1
    
    for v in classes:
        classes[v]['elementsNumber'] = counters[v]
        
    return classes


# print result on json file
def printToJson(asin, result):
    f = open('json/anomaly_detection_' + asin + '.json', 'w')
    json.dump(result, f, indent=4)
    f.close
    
    
# print data frame on csv file
def printToCsv(asin, data_frame):
    data_frame.to_csv('xls/anomaly_detection_' +asin+ '.xls')    


# cluster based anomaly detection algorithm 
def clustering (df, data):
    # preprocess features: normalization and standardization
    min_max_scaler = preprocessing.StandardScaler()
    np_scaled = min_max_scaler.fit_transform(data)
    features = pd.DataFrame(np_scaled)
    
    '''
    # it is possible to reduce the dimension of the features space
    # reduce to 3 importants features
    pca = PCA(n_components=3)
    features = pca.fit_transform(features)
    
    # standardize these 3 new features
    min_max_scaler = preprocessing.StandardScaler()
    np_scaled = min_max_scaler.fit_transform(features)
    features = pd.DataFrame(np_scaled) 
    '''
    n_cluster = range(1, 4)
    kmeans = [KMeans(n_clusters=i).fit(features) for i in n_cluster]
    df['class'] = kmeans[2].predict(features)
    df['class'] = df['class'].map({0: 'cluster 1', 1: 'cluster 2', 2: 'cluster 3'})
    #print '\nCluster\n', df['class'].value_counts()
    
    result = getResult(df, ['cluster 1', 'cluster 2', 'cluster 3'])
    return df, result


# isolation forest anomaly detection algorithm 
def isolationForest(df, data):
    # preprocess features: normalization and standardization
    min_max_scaler = preprocessing.StandardScaler()
    np_scaled = min_max_scaler.fit_transform(data)
    features = pd.DataFrame(np_scaled)
    
    model =  IsolationForest(contamination = outliers_fraction)
    model.fit(features)
    
    # add the data to the data frame df   
    df['class'] = pd.Series(model.predict(features))
    df['class'] = df['class'].map({1: 'normal', -1: 'anomalous'})
    #print '\nIsolation Forest\n', df['class'].valuthe anomaly detection processe_counts()
    
    result = getResult(df, ['normal', 'anomalous'])
    return df, result
    

# svm anomaly detection algorithm 
def svm(df, data):
    # preprocess features: normalization and standardization
    min_max_scaler = preprocessing.StandardScaler()
    np_scaled = min_max_scaler.fit_transform(data)
    # train one class SVM 
    model =  OneClassSVM(nu=0.95 * outliers_fraction)
    features = pd.DataFrame(np_scaled)
    model.fit(features)
    
    # add the data to the data frame df 
    df['class'] = pd.Series(model.predict(features))
    df['class'] = df['class'].map( {1: 'normal', -1: 'anomalous'} )
    #print '\nSVM\n', df['class'].value_counts()
    
    result = getResult(df, ['normal', 'anomalous'])
    return df, result
    

def combinationIsolationForest_Cluster(df, data):
    #
    data_frame, result = isolationForest(df, data)
    data_frame.drop('normal', 1)
    print data_frame
    #print data_frame['class'].value_counts()
    
    
    
    

# method to run a few anomaly detection algorithms
# used method:
    # clustering
    # isolation forest
    # SVM
def applyAlgorithms(df, data):
    cluster_df, res_clustering = clustering (df, data)
    df['cluster'] = cluster_df['class']
    isolationForest_df, res_isolationForest = isolationForest(df, data)
    df['isolation forest'] = isolationForest_df['class']
    svm_df, res_svm = svm(df, data)
    df['svm'] = svm_df['class']
    
    result = {'Cluster' : res_clustering, 
              'Isolation Forest': res_isolationForest, 
              'SVM': res_svm
              }
    
    df = df.drop(columns='class')
    return df, result


# main method
def anomalyDetection(asin):
    df = makeDataFrame(asin)
    
    # structure the data to make the anomaly detection process easier
    # remove 'idReview', useless for the process
    data = df[['shortAndRepetitive',
            'verifiedPurchase',
            'reviewByUser',
            'variance',
            'reviewDate',
            'repeatedTrigrams',
            'reviewLength',
            'reviewHelpfulness',
            'vineReview']]
    
    data_frame, result = applyAlgorithms(df, data)
    # print results on files
    printToJson(asin, result)
    printToCsv(asin, data_frame)
    
    return result
    


if __name__ == '__main__':
    
    asin = 'B01AXOCCG2'
    data_frame = makeDataFrame(asin)
    
    # structure the data to make the anomaly detection process easier
    # remove 'idReview', useless for the process
    data = data_frame[['shortAndRepetitive',
            'verifiedPurchase',
            'reviewByUser',
            'variance',
            'reviewDate',
            'repeatedTrigrams',
            'reviewLength',
            'reviewHelpfulness',
            'vineReview']]
    
    combinationIsolationForest_Cluster (data_frame, data)










