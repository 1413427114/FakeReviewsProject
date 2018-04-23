# -*- coding: utf-8 -*-
import json
import numpy as np
import datetime as dt
from dateutil import parser as dp
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import Counter

def reviewsPerDay(reviews_data):
    all_days = []
    for review in reviews_data:
        review_date = reviews_data[review]['reviewPostedDate']
        all_days.append(review_date)
    return all_days
       
def reviewsPerUser(reviews_data):
    all_users = []
    for review in reviews_data:
        review_author = reviews_data[review]['reviewAuthor']['code']
        all_users.append(review_author)
    return all_users

def trigramsPerRev(trigrams_data):
    trigrams_per_rev = []
    for review in trigrams_data:
        repeated_trigrams = trigrams_data[review]['numberOfRepeatedTrigrams']
        trigrams_per_rev.append(repeated_trigrams)
    return trigrams_per_rev

def plotRevPerDay(all_days, fig, ax):
    rpd_d = []
    for d in all_days:
        try: 
            d = dp.parse(d).strftime('%d %m %Y')
            data = dt.datetime.strptime(d, "%d %m %Y").date()
            rpd_d.append(data)
        except: None
    
    mpl_data = mdates.date2num(np.array(rpd_d))
       
    ax[0].hist(mpl_data, bins=100)
    ax[0].xaxis.set_major_locator(mdates.MonthLocator())
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%m.%y'))
    ax[0].set_title("Frequenza recensioni per periodi")     
    #ax[0].set_xlabel('Mesi', fontsize = 9)
    #ax[0].set_ylabel('Frequenza', fontsize = 9)
    plt.show()
    
def plotRevPerUser(all_users, fig, ax):
    l, v = zip(*Counter(all_users).items()) 
    labels, values = zip(*Counter(v).items())   
    
    indexes = np.arange(len(labels))
    width = 0.5    
    
    ax[1].set_title("Numero Recensioni x Numero Utenti")
    #ax[1].set_xlabel('Numero Recensioni', fontsize = 9)
    #ax[1].set_ylabel('Numero Utenti', fontsize = 9)
    plt.sca(ax[1])
    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5, labels)
    plt.show()

def plotTrigramsPerRep(trigrams_per_rep, fig, ax):
    labels, values = zip(*Counter(trigrams_per_rep).items()) 

    indexes = np.arange(len(labels))
    width = 0.5    
    
    ax[2].set_title("Numero Trigrammi Ripetuti x Numero Recensioni")
    #ax[2].set_xlabel('Numero Trigrammi ripetuti', fontsize = 9)
    #ax[2].set_ylabel('Numero Recensioni', fontsize = 9)
    plt.sca(ax[2])
    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5, labels)
    plt.show()
    
    
if __name__ == '__main__':    
    asin = 'B01AXOCCG2' #'B00PVDMTIC' 'B01LZ1Y47Q' 'B01AXOCCG2' 'B01GPEA1QC' 'B01MY98XEN'
    
    review_data = json.load(open('json/'+asin+'/sommario_'+asin+'.json'))
    reviews_data = review_data[asin]['reviews']
    trigrams_data = review_data[asin]['trigrams']
    all_days = reviewsPerDay(reviews_data)
    all_users = reviewsPerUser(reviews_data)
    trigrams_per_rev = trigramsPerRev(trigrams_data)

    rest = []
    for i in range(0,(len(all_days)-len(trigrams_per_rev))): rest.append(0)
    rest += trigrams_per_rev
    
    fig, ax = plt.subplots(3,1)
    plotRevPerDay(all_days, fig, ax)
    plotRevPerUser(all_users, fig, ax)   
    plotTrigramsPerRep(trigrams_per_rev, fig, ax)
    #plotTrigramsPerRep(rest, fig, ax)