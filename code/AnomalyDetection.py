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
    data = json.load(open('json/'+asin+'/analisi_' + asin + '.json'))
    
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
            'vineReview': [],
            'authorEasyGrader': [],
            'authorRepetitiveReviewer': [],
            'authorRank': [],
            'authorOneTimeReviewer': []
            }

    # populate the dictionary previously initialized
    for rev in data:
        scoreDetails = data[rev]['scoreDetails']
        author_data = scoreDetails['authorReliability']
        
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
        review_dict['authorEasyGrader'].append(author_data['easyGrader'])
        review_dict['authorRepetitiveReviewer'].append(author_data['repetitiveReviewer'])
        review_dict['authorRank'].append(author_data['rank'])
        review_dict['authorOneTimeReviewer'].append(author_data['oneTimeReviewer'])
    
    df = pd.DataFrame(review_dict)
    return df
  
    
# structure the data to make the anomaly detection process easier
# extract features only removing 'idReview', useless for the process
def getFeatures(data_frame):
    data = data_frame[['shortAndRepetitive',
            'verifiedPurchase',
            'reviewByUser',
            'variance',
            'reviewDate',
            'repeatedTrigrams',
            'reviewLength',
            'reviewHelpfulness',
            'vineReview',
            'authorEasyGrader',
            'authorRepetitiveReviewer',
            'authorRank',
            'authorOneTimeReviewer']]
    return data


# create a dictionary to easier manage data
def structData (df):
    reviews = {}
    index = df.index.tolist()
    for i in index:
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
                        'authorEasyGrader': df['authorEasyGrader'][i],
                        'authorRepetitiveReviewer': df['authorRepetitiveReviewer'][i],
                        'authorRank': df['authorRank'][i],
                        'authorOneTimeReviewer': df['authorOneTimeReviewer'][i],
                        'category': str(df['category'][i])
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
            if temp[rev]['category'] == v:
                classes[v]['reviews'] = dict(classes[v]['reviews'].items() + temp.items())
                counters[v] = counters[v] + 1
    
    for v in classes:
        classes[v]['elementsNumber'] = counters[v]
        
    return classes


# print result on json file
def printToJson(asin, result):
    #f = open('json/'+asin+'/anomaly_detection_' + asin + '.json', 'w')
    f = open('json/'+asin+'/anomaly_detection_' + asin + '.json', 'w')
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
    
    df.loc[:,'category'] = kmeans[2].predict(features)
    df.loc[:,'category'] = df['category'].map({0: 'cluster 1', 1: 'cluster 2', 2: 'cluster 3'})
    #print '\nCluster\n', df['category'].value_counts()
    
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
    df['category'] = pd.Series(model.predict(features))
    df['category'] = df['category'].map({1: 'normal', -1: 'anomalous'})
    #print '\nIsolation Forest\n', df['category'].valuthe anomaly detection processe_counts()
    
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
    df['category'] = pd.Series(model.predict(features))
    df['category'] = df['category'].map( {1: 'normal', -1: 'anomalous'} )
    #print '\nSVM\n', df['category'].value_counts()
    
    result = getResult(df, ['normal', 'anomalous'])
    return df, result


# procedure to cluster results of isolation forest/svm algorithm:
# anomalous results from isolation forest/svm algorithm can be separated in two clusters
# with different features since some of them can be considered positively anomaluos 
# (we can assume those are the certainly trustable ones) and others negatively anomalous 
# (we can assume those are the fake ones)
def combinations(df, data):
    # cluster initialization
    n_cluster = range(1, 3)
    
    # final result initialization
    final_result = { 
            'Combination Isolation Forest - Cluster' : {},
            'Combination SVM - Cluster' : {} }
    
    # ISOLATION FOREST EXECUTION
    data_frame_if, res_if = isolationForest(df, data)
    # separate normal etries from anlomalous entries 
    normal_only_if = data_frame_if[data_frame_if.category == 'normal']
    anomalous_only_if = data_frame_if[data_frame_if.category == 'anomalous']
    data_if = getFeatures(anomalous_only_if)
    # computing clusters
    kmeans = [KMeans(n_clusters=i).fit(data_if) for i in n_cluster]
    anomalous_only_if.loc[:,'category'] = kmeans[1].predict(data_if)
    anomalous_only_if.loc[:,'category'] = anomalous_only_if['category'].map({0: 'cluster 1', 1: 'cluster 2'})
    # get isolation forest results
    res_clustering_if = getResult(anomalous_only_if, ['cluster 1', 'cluster 2'])
    normal_result_if = getResult(normal_only_if, ['normal'])
    # add isolation forest result to final result
    final_result['Combination Isolation Forest - Cluster'] = dict(final_result['Combination Isolation Forest - Cluster'].items() + normal_result_if.items())
    final_result['Combination Isolation Forest - Cluster'] = dict(final_result['Combination Isolation Forest - Cluster'].items() + {'anomalous': res_clustering_if}.items())

    
    # SVM EXECUTION
    data_frame_svm, res_svm = svm(df, data)
    # separate normal etries from anlomalous entries
    normal_only_svm = data_frame_svm[data_frame_svm.category == 'normal']
    anomalous_only_svm = data_frame_svm[data_frame_svm.category == 'anomalous']
    data_svm = getFeatures(anomalous_only_svm)
    # computing clusters
    kmeans = [KMeans(n_clusters=i).fit(data_svm) for i in n_cluster]
    anomalous_only_svm.loc[:,'category'] = kmeans[1].predict(data_svm)
    anomalous_only_svm.loc[:,'category'] = anomalous_only_svm['category'].map({0: 'cluster 1', 1: 'cluster 2'})
    # get svm results
    res_clustering_svm = getResult(anomalous_only_svm, ['cluster 1', 'cluster 2'])
    normal_result_svm = getResult(normal_only_svm, ['normal'])
    # add svm result to final result
    final_result['Combination SVM - Cluster'] = dict(final_result['Combination SVM - Cluster'].items() + normal_result_svm.items())
    final_result['Combination SVM - Cluster'] = dict(final_result['Combination SVM - Cluster'].items() + {'anomalous': res_clustering_svm}.items())

    #print final_result
            
    return final_result


# method to run a few anomaly detection algorithms
# used method:
    # clustering
    # isolation forest
    # SVM
def applyAlgorithms(df, data):
    cluster_df, res_clustering = clustering (df, data)
    df.loc[:,'cluster'] = cluster_df['category']
    
    isolationForest_df, res_isolationForest = isolationForest(df, data)
    df.loc[:,'isolation forest'] = isolationForest_df['category']
    
    svm_df, res_svm = svm(df, data)
    df.loc[:,'svm'] = svm_df['category']
    
    res_combinations = combinations(df, data)
    
    result = {'Cluster' : res_clustering, 
              'Isolation Forest': res_isolationForest, 
              'SVM': res_svm,
              'Combination Isolation Forest - Cluster': res_combinations['Combination Isolation Forest - Cluster'],
              'Combination SVM - Cluster': res_combinations['Combination SVM - Cluster']
              }
    
    df = df.drop(columns='category')
    #df = df.drop('category', axis=1)
    return df, result


# main method
def anomalyDetection(asin):
    df = makeDataFrame(asin)
    data = getFeatures(df)
    
    data_frame, result = applyAlgorithms(df, data)
    # print results on files
    printToJson(asin, result)
    printToCsv(asin, data_frame)
    
    return result

    