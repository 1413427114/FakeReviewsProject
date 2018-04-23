# -*- coding: utf-8 -*-

import Scraper as s
import ReviewTextAnalisys as rta
import ReviewCheck as rc
import FinalResult as fr
import AnomalyDetection as ad
import json


def parseSite(site):
    site_fields = site.split('/')
    if len(site_fields) == 1:
        # url fixed on amazon.it
        return site, "https://www.amazon.it"
    else:
        amazon_domain = "amazon" + ((site.split("amazon")[1].split("/")[0]))
        try:  # with https://www.amazon.it/dp/ASIN/ link type
            index = site_fields.index("dp")
        except:  # with https://www.amazon.it/gp/product/ASIN/ link type
            index = site_fields.index("product")
        asin = site_fields[index + 1]
        return asin, amazon_domain


def readAsinAndDomain():
    site = raw_input("Inserisci link prodotto o ASIN (codice) prodotto: ")
    return parseSite(site)


def scrapingAndTextAnalisys(asin, amazon_domain):
    review_product_data = s.executeScraper(asin, amazon_domain)
    # print review_product_data
    review_text_analisys_data = rta.executeAnalisys(review_product_data[0])

    data = {
        asin: {
            'reviews': review_product_data[0],
            'productDetails': review_product_data[1],
            'trigrams': review_text_analisys_data
        }
    }

    f = open('json/sommario_' + asin + '.json', 'w')
    json.dump(data, f, indent=4)
    f.close
    
    return data


def checkingReviews(asin):
    reviews_check_score = rc.reviewsScore(asin)

    f = open('json/analisi_' + asin + '.json', 'w')
    json.dump(reviews_check_score, f, indent=4)
    f.close
    return reviews_check_score


def checkFinalResult(asin):
    conclusion = fr.finalResult(asin)

    f = open('json/conclusion_' + asin + '.json', 'w')
    json.dump(conclusion, f, indent=4)
    f.close
    return conclusion


if __name__ == '__main__':
    import time
    start_time = time.time()
    
    #asin =  #'B00PVDMTIC' 'B01LZ1Y47Q' 'B01AXOCCG2' 'B01GPEA1QC'
    #amazon_domain = 'https://www.amazon.it' 
    asin, amazon_domain = readAsinAndDomain()

    
    print '\nScraping data . . .'
    scraping_data = scrapingAndTextAnalisys(asin, amazon_domain)
    #scraping_data = json.load(open('json/sommario_'+asin+'.json'))
    print 'done'
    
    print '\nChecking reviews scores . . .'
    reviews_check_score = checkingReviews(asin)
    #reviews_check_score = json.load(open('json/analisi_'+asin+'.json'))
    print 'done'
    
    print '\nDetecting anomalies . . .'
    #anomaly_detection = ad.anomalyDetection(asin)
    anomaly_detection = json.load(open('json/anomaly_detection_'+asin+'.json'))
    print 'done'
    
    print '\nProducing conclusive result . . .'
    conclusion = checkFinalResult(asin)
    #conclusion = json.load(open('json/conclusion_'+asin+'.json'))
    print 'done'

    data = {
        asin: {
            'reviewsAndTrigrams': {
                # 'reviews': reviews_data,
                'reviews': scraping_data[asin]['reviews'],
                # 'trigrams': trigrams_data
                'trigrams': scraping_data[asin]['trigrams']
            },
            # 'productDetails': product_data,
            'productDetails': scraping_data[asin]['productDetails'],
            'reviewPartialScores': reviews_check_score,
            'anomalyDetectionResult': anomaly_detection,
            'possibleConclusion': conclusion
        }
    }

    f = open('json/all_in_one_' + asin + '.json', 'w')
    json.dump(data, f, indent=4)
    f.close
    print '\nExecution completed\n'
    print("--- %s seconds ---" % (time.time() - start_time))
    
