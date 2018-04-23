# -*- coding: utf-8 -*-

import json
import math


# variabili globali
rev_per_day = {}    # numero reviews per giorno
rev_per_user = {}   # numero reviews per utente
trigrams_data = {} #review che contengono trigrammi ripetuti
avg_length_reviews = 0 #lunghezza media delle recensioni


# creazione mappe relative all'analisi delle reviews per giorno e per utenti
def reviewsPerDay(reviews_info, indexName):
    rev_per_day = {}
    for review in reviews_info:
        review_date = reviews_info[review][indexName]
        try: rev_per_day[review_date] += 1
        except: rev_per_day[review_date] = 1
    return rev_per_day
        

def reviewsPerUser(reviews_info, indexName):
    rev_per_user = {}
    for review in reviews_info:
        review_author = reviews_info[review]['reviewAuthor'][indexName]
        try: rev_per_user[review_author] += 1
        except: rev_per_user[review_author] = 1
    return rev_per_user
        

def setAvgLengthOfReviews(reviews_info):
    avg_length_reviews = 0
    for review in reviews_info:
        rev_length = len(reviews_info[review]['reviewText'].split())
        avg_length_reviews += rev_length
    avg_length_reviews = avg_length_reviews / len(reviews_info)
    return avg_length_reviews
        
        
# return 1 se acquisto verificato, -1 altrimenti        
def checkVerifiedPurchase(review):
    if review['reviewVerifiedPurchase']:
        return 1
    return -1


# return 1 se il giorno non è anomalo, -1 altrimenti
def checkReviewDate(review):
    # verifica se nella data della reviews sono state effettuate un numero
    # di reviews maggiore della media calcolata su tutti i giorni
    average_reviews_per_day = float(sum(rev_per_day.values())) / float(len(rev_per_day))
    rev_day_av = rev_per_day[review['reviewPostedDate']] - average_reviews_per_day
    if rev_day_av <=0 : 
        return 0            
    return -(rev_day_av)
    

# return 1 se l'utente ha realizzato una sola recensione, 0 se ne ha realizzate 2,
# un valore negativo (num_review - 2) altrimenti
def checkReviewsByUser (review):
    # verifica se un utente ha recensito più volte lo stesso prodotto
    num_rev = rev_per_user[review['reviewAuthor']['code']]
    if num_rev >= 2: 
        return (2-num_rev)
    return 1


# return il numero di voti utili che la recensione ha ricevuto
def checkReviewHelpfulness(review):
    return review['reviewHelpfulVote']    
    
    
def checkVariance(review, product):
    diff = float(product['productRating']) - float(review['reviewRating'].replace(',','.'))
    return abs(diff)


def checkRepeatedTrigrams(review):
    rev_id = review['reviewId']
    if rev_id in [revs_id for revs_id in trigrams_data]:
        return -(trigrams_data[rev_id]['numberOfRepeatedTrigrams'])
    return 1
    

def checkIsVineReview(review):
    if review['isAmazonVineReviewer']:
        return 2
    return 0
    

def checkReviewLength(review):
    rev_length = len(review['reviewText'].split())
    if rev_length >= avg_length_reviews:
        return 1
    return -1


# EXAMPLES
# rank:119 - helpfulVotes:2650 - totalReviewsCount:856 --- rank_score = 19,062..
# rank:597 - helpfulVotes:3078 - totalReviewsCount:1069 --- rank_score = 5,511..
# rank:35271 - helpfulVotes:17 - totalReviewsCount:36 --- rank_score = 0,00000173..
# rank:292650 - helpfulVotes:3 - totalReviewsCount:15 --- rank_score = 0,0000000153..
def checkAuthorRank(review):
    author_rank = review['reviewAuthor']['rank']
    author_helpful_votes = review['reviewAuthor']['helpfulVotes']
    author_reviews_count = review['reviewAuthor']['totalReviewsCount']
    if author_reviews_count and author_helpful_votes and author_rank:
        rank_score = float(author_helpful_votes * author_reviews_count) / float(author_rank * 1000) 
        return rank_score
    return 0
    

def checkEasyGrader(review):
    # se almeno un X% delle recensioni sono a 5 stelle, vuol dire che è un easy grader
    # questo riduce la sua affidabilità di osservazioni
    if review['reviewAuthor']['latestReviews']:
        reviews = review['reviewAuthor']['latestReviews']['reviews']
        if reviews:
            five_stars_rating = 0
            for rev in reviews:
                if reviews[rev]['reviewRating']==5:
                    five_stars_rating += 1
            if (five_stars_rating * len(reviews))>=50:  #se almeno il 50% (5 su 10 nel nostro caso) sono 5 stelle è easyGrader
                return -1
            return 1
    return 0
    

def checkOneTimeReviewer(review):
    # se almeno un X% delle recensioni sono in uno stesso giorno, vuol dire che recensisce tutto in una volta
    # questo riduce la sua affidabilità di osservazioni
    if review['reviewAuthor']['latestReviews']:
        reviews = review['reviewAuthor']['latestReviews']['reviews']
        if reviews:
            rev_per_day = reviewsPerDay(reviews, 'reviewDate')    
            for rev in reviews:
                rev_day = reviews[rev]['reviewDate']
                if (rev_per_day[rev_day] * len(reviews))>=50: # se almeno il 50% (5 su 10 nel nostro caso) sono nello stesso giorno è oneTimeReviewer
                    return -1
            return 1
    return 0


def checkRepetitiveReviewer(review):
    if review['reviewAuthor']['latestReviews']:
        trigrams = review['reviewAuthor']['latestReviews']['trigrams']
        if trigrams:
            if len(trigrams)>0:
                return -(len(trigrams))
        return 1
    return 0
    

def checkAuthorReliability(review):
    r_score = checkAuthorRank(review)
    eg_score = checkEasyGrader(review)
    otr_score = checkOneTimeReviewer(review)
    rr_score = checkRepetitiveReviewer(review)
    
    author_score_details = {
        'rank': r_score,
        'easyGrader': eg_score,
        'oneTimeReviewer': otr_score,
        'repetitiveReviewer': rr_score
    }
    
    author_score = r_score + eg_score + otr_score + rr_score
    return author_score_details, author_score    
    

# return review score  
def checkReview(review, product):
    vp_score = checkVerifiedPurchase(review) 
    rd_score = round(checkReviewDate(review), 3) * 0.1
    rbu_score = checkReviewsByUser(review)
    # checkSentence
    rh_score = checkReviewHelpfulness(review)
    v_score = -(round(math.pow(checkVariance(review, product), 2), 4)) if product else 0
    rt_score = checkRepeatedTrigrams(review) * 2
    vr_score = checkIsVineReview(review)
    rl_score = checkReviewLength(review)
    sr_score = -1 if (rt_score<0 and rl_score<0) else 0
    
    partial_author_score, author_score = checkAuthorReliability(review)
    
    final_score = vp_score + rd_score + rbu_score + rh_score + v_score + rt_score + vr_score + rl_score + sr_score + author_score

    score_details = {
        'finalScore': round(final_score, 4),
        'scoreDetails': {
                'verifiedPurchase': vp_score,
                'reviewDate': rd_score,
                'reviewHelpfulness': rh_score,
                'variance': v_score,
                'reviewByUser': rbu_score,
                'repeatedTrigrams': rt_score,
                'vineReview': vr_score,
                'reviewLength': rl_score,
                'shortAndRepetitive': sr_score,
                'authorReliability': partial_author_score
            }
    }
    return score_details
        

# return scores of all the analized reviews    
def reviewsScore(asin):    
    review_data = json.load(open('json/sommario_'+asin+'.json'))
    reviews_data = review_data[asin]['reviews']
    product_data = review_data[asin]['productDetails']
    
    global trigrams_data
    trigrams_data = review_data[asin]['trigrams'] 
    
    global rev_per_day
    rev_per_day = reviewsPerDay(reviews_data, 'reviewPostedDate')
    
    global rev_per_user
    rev_per_user = reviewsPerUser(reviews_data, 'code')
    
    global avg_length_reviews
    avg_length_reviews = setAvgLengthOfReviews(reviews_data)
      
    # test reviews
    reviews_scores={}
    for review in reviews_data:
        id = reviews_data[review]['reviewId']
        reviews_scores[id] = checkReview(reviews_data[review], product_data)
    print len(reviews_scores)
    return reviews_scores 
    
if __name__ == '__main__':
    asin =  'B00PVDMTIC' #'B01LZ1Y47Q' 'B01AXOCCG2' 'B00PVDMTIC'
    reviews_check_score = reviewsScore(asin)

    f = open('json/analisi_' + asin + '.json', 'w')
    json.dump(reviews_check_score, f, indent=4)
    f.close()    