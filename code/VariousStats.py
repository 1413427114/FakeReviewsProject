# -*- coding: utf-8 -*-
import json

def getAllReviewsAndRatings(reviews):
    reviews_and_ratings = []
    for rev in reviews:
        review_id = reviews[rev]['reviewId']
        review_rating = reviews[rev]['reviewRating']
        reviews_and_ratings.append((review_id, review_rating))
    return reviews_and_ratings

def getAnomalousReviews(data):
    anomalous_svm, anomalous_isolation = [], []
    anomalous_svm = data['SVM']['anomalous']['reviews'].keys()
    anomalous_isolation = data['Isolation Forest']['anomalous']['reviews'].keys()
    return anomalous_svm, anomalous_isolation
    
def getCombinationAnomalousClusterReviews(data):
    anomalous_svm, anomalous_isolation = [], []
    anomalous_svm = data['Combination SVM - Cluster']['anomalous']['cluster 2']['reviews'].keys()
    anomalous_isolation = data['Combination Isolation Forest - Cluster']['anomalous']['cluster 2']['reviews'].keys()
    return anomalous_svm, anomalous_isolation
    
def getWarningAndFakeReviews(data):
    warning_reviews, fake_reviews = [], []
    warning_reviews = data['warning']['reviews'].keys()
    fake_reviews = data['fake']['reviews'].keys()
    return warning_reviews, fake_reviews

def similar(x,y):
    si = 0
    (minore, maggiore) = (x, y) if len(x)<len(y) else (y, x)
    for el in minore:
        if el in maggiore:
            si += 1
    return round((float(si)/len(maggiore)) * 100, 2)
    
def getFinalRating(rev_and_ratings, anomalous_rev):
    final_rating = 0
    for (r, v) in rev_and_ratings:
        if not(r in anomalous_rev):        
            final_rating += float(v.replace(',', '.'))
    return round((final_rating/(len(rev_and_ratings)-len(anomalous_rev))),1)
    
if __name__ == '__main__':
    asin_list = ['B00PVDMTIC', 'B01LZ1Y47Q', 'B01MY98XEN', 'B01AXOCCG2', 'B01GPEA1QC', 'B00P73B1E4']
    #asin_list = ['B00PVDMTIC'] #'B00PVDMTIC' 'B01LZ1Y47Q' 'B01MY98XEN' 'B01AXOCCG2' 'B01GPEA1QC' 
    
    for asin in asin_list:
        print('\n----- ASIN: '+asin+' -----')
        summary_data = json.load(open('json/'+asin+'/sommario_'+asin+'.json'))
        reviews_and_ratings = getAllReviewsAndRatings(summary_data[asin]['reviews'])
        
        try: anomaly_data = json.load(open('json/'+asin+'/anomaly_detection_'+asin+'.json'))
        except: anomaly_data = json.load(open('json/'+asin+'/combination_anomaly_detection_'+asin+'.json'))   
        anomalous_svm, anomalous_isolation = getAnomalousReviews(anomaly_data) 
        anomalous_svm_cluster, anomalous_isolation_cluster = getCombinationAnomalousClusterReviews(anomaly_data) 
        
        conclusion_data = json.load(open('json/'+asin+'/conclusion_'+asin+'.json'))
        warning_rev, fake_rev = getWarningAndFakeReviews(conclusion_data)
        
        '''
        import difflib
        sm=difflib.SequenceMatcher(None, warning_rev, anomalous_svm)
        print sm.ratio()
        '''
        
        print('Misure di similarità sui warning/anomalous rilevati:')
        print '\tFake + Warning reviews & Anomalous SVM reviews: %s%s' % (similar((fake_rev+warning_rev), anomalous_svm),'%')
        print '\tFake + Warning reviews & Anomalous IF reviews: %s%s' % (similar((fake_rev+warning_rev), anomalous_isolation),'%')
        print '\tAnomalous SVM & Anomalous IF reviews: %s%s' % (similar(anomalous_svm, anomalous_isolation),'%')
        print '\tAnomalous SVM-Cluster 2 & Anomalous IF-Cluster 2 reviews: %s%s' % (similar(anomalous_svm_cluster, anomalous_isolation_cluster),'%')
        '''
        actual_rating = float(summary_data[asin]['productDetails']['productRating'])
        print('Rating finale calcolato rimuovendo i warning-fake/anomalous rilevati:')
        print '\tRating senza Fake-Reviews: %s ---> %s' % (actual_rating, getFinalRating(reviews_and_ratings, fake_rev))
        print '\tRating senza Fake & Warning-Reviews: %s ---> %s' % (actual_rating, getFinalRating(reviews_and_ratings, (fake_rev + warning_rev)))
        print '\tRating senza Anomalous SVM-Reviews: %s ---> %s' % (actual_rating, getFinalRating(reviews_and_ratings, anomalous_svm))
        print '\tRating senza Anomalous IF-Reviews: %s ---> %s' % (actual_rating, getFinalRating(reviews_and_ratings, anomalous_isolation))
        '''