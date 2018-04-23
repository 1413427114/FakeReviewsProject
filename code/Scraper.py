# -*- coding: utf-8 -*-

from lxml import html
import requests
import datetime
from dateutil import parser as dateparser
from time import sleep
import random
import AuthorCheck as ac

execute_sleep = False

def parseDate(date_to_parse):
    string_of_date = (''.join(date_to_parse)).split('il ')[1]
    string_of_date = string_of_date.replace('gennaio', 'jan')
    string_of_date = string_of_date.replace('febbraio', 'feb')
    string_of_date = string_of_date.replace('marzo', 'mar')
    string_of_date = string_of_date.replace('aprile', 'apr')
    string_of_date = string_of_date.replace('maggio', 'may')
    string_of_date = string_of_date.replace('giugno', 'jun')
    string_of_date = string_of_date.replace('luglio', 'jul')
    string_of_date = string_of_date.replace('agosto', 'aug')
    string_of_date = string_of_date.replace('settembre', 'sep')
    string_of_date = string_of_date.replace('ottobre', 'oct')
    string_of_date = string_of_date.replace('novembre', 'nov')
    string_of_date = string_of_date.replace('dicembre', 'dec')
    try:       
        return dateparser.parse(string_of_date).strftime('%d %b %Y')
    except:
        return date_to_parse
    
    
def parseResponse(response, amazon_url, rev_index):
    p_resp = response
    reviews = p_resp.split('&&&')
    
    XPATH_ID = './/div[@data-hook="review"]'
    XPATH_RATING  = './/i[@data-hook="review-star-rating"]//text()'
    XPATH_TITLE = './/a[@data-hook="review-title"]//text()'
    XPATH_AUTHOR  = './/a[@data-hook="review-author"]//text()'
    XPATH_AUTHOR_PROFILE  = './/a[@data-hook="review-author"]'
    XPATH_POSTED_DATE = './/span[@data-hook="review-date"]//text()'
    XPATH_VERIFIED_PURCHASE = './/span[@data-hook="avp-badge"]//text()'
    XPATH_BODY = './/span[@data-hook="review-body"]//text()'
    XPATH_HELPFUL = './/span[@data-hook="helpful-vote-statement"]//text()'
    
    reviews_list = {}
    
    # the first 3 fields of the array can be discarded since useless
    for i in range(3, len(reviews)):
        rev_fields = reviews[i].split('\",\"')
        
        if len(rev_fields)==3:            
            # the 3rd field (rev_fields[2]) contains the html of the review
            review = rev_fields[2].replace("\\\"", "\"")
            
            is_amazon_vine = True if "Recensione Vine " in review else False
            
            parser = html.fromstring(review)
    
            # DATA COMPUTATION
            # if 'id' field is not found we can assume we are working on a html response referred to a review
            # the last 3 fields contain no information
            review_id = ""
            for elem in parser.xpath(XPATH_ID):
                review_id = elem.attrib['id']
            if review_id is "": 
                break
            raw_review_rating = parser.xpath(XPATH_RATING)
            raw_review_header = parser.xpath(XPATH_TITLE)
            raw_review_author = parser.xpath(XPATH_AUTHOR)            
            # retrieve the link to the review's author profile
            for elem in parser.xpath(XPATH_AUTHOR_PROFILE):
                raw_review_author_profile = elem.attrib['href']
            raw_review_posted_date = parser.xpath(XPATH_POSTED_DATE)
            raw_review_verified_purchase = parser.xpath(XPATH_VERIFIED_PURCHASE)
            raw_review_body = parser.xpath(XPATH_BODY)
            raw_review_helpful_vote = parser.xpath(XPATH_HELPFUL)
            
            # DATA COMPOSITION
            author_name = ' '.join(' '.join(raw_review_author).split()) if raw_review_author else ""
            author_profile = amazon_url + ''.join(raw_review_author_profile) if raw_review_author_profile else ""
            author_code = (author_profile.split("account.")[1]).split("/")[0]
            review_rating = ''.join(raw_review_rating).replace(' su 5 stelle','') if raw_review_rating else ""            
            review_header = ' '.join(' '.join(raw_review_header).split()) if raw_review_header else ""            
            review_text = ' '.join(' '.join(raw_review_body).split()) if raw_review_body else ""            
            review_verified_purchase = True if raw_review_verified_purchase else False
            review_posted_date = parseDate(raw_review_posted_date) if raw_review_posted_date else None             
            try:
                review_helpful_vote = int([x for x in (''.join(raw_review_helpful_vote).split(' ')) if x != ''][1]) if raw_review_helpful_vote else 0
            except: 
                review_helpful_vote = 1
            
            author_id, author_rank = ac.getCustomerId(author_code, amazon_url)
            if author_id<>None:
                author_helpful_votes, author_reviews_count = ac.getHelpfulVotesAndTotalReviewsCount(author_id, amazon_url)
            else: 
                author_helpful_votes, author_reviews_count = -1, -1
            latest_author_reviews = ac.getLatestCustomerReviewAndTextAnalisys(author_code, amazon_url)
            
            # set a sleeping time
            if execute_sleep:
                #sleep(random.uniform(2,4))
                sleep(2)
            
            review_summary = {
                    'reviewId':review_id,
                    'reviewLink': amazon_url + "/gp/customer-reviews/" + review_id,
                    'reviewText': review_text,
                    'reviewPostedDate': review_posted_date,
                    'reviewHeader': review_header,
                    'reviewRating': review_rating,
                    'reviewAuthor': {
                        'name': author_name,
                        'profileLink': author_profile,
                        'code': author_code,
                        'id': author_id,
                        'rank': author_rank,
                        'helpfulVotes': author_helpful_votes,
                        'totalReviewsCount': author_reviews_count,
                        'latestReviews': latest_author_reviews
                    },
                    'reviewVerifiedPurchase': review_verified_purchase,
                    'reviewHelpfulVote': review_helpful_vote,
                    'isAmazonVineReviewer': is_amazon_vine
                }
            reviews_list[rev_index] = review_summary
            rev_index += 1
 
    return reviews_list


def getReviews(asin, amazon_url):  
    # Add some recent user agent to prevent amazon from blocking the request 
    # Find some chrome user agent strings  here https://udger.com/resources/ua-list/browser-detail?browser=Chrome
    user_agents = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36']
    headers = {'User-Agent': user_agents[random.randint(0, (len(user_agents)-1))]}
    
    #parameters for ajax request
    data = {
        'asin': asin,
        'deviceType': 'desktop',
        'filterByKeyword': '',  #example 'ciao+mamma+...'
        'filterByStar': 'all_stars',  #example 'five_star'
        'formatType': '',  #
        'pageNumber': 0,
        'pageSize': 50,
        'reftag': '',
        'reviewerType': 'all_reviews',  #example 'avp_only_reviews'
        'scope': 'reviewsAjax',
        'shouldAppend': 'undefined',
        'sortBy': 'recent'
    }
    
    all_reviews_list = {}
    i = 1
    while True:        
        data['pageNumber'] = i
        data['reftag'] = 'cm_cr_getr_d_paging_btm_'+str(i)
        data['scope'] = 'reviewsAjax'+str(i)
        ajax_request_url = amazon_url + '/ss/customer-reviews/ajax/reviews/get/ref=cm_cr_arp_d_paging_btm_'+str(i)
        response = requests.post(ajax_request_url, data, headers = headers)
        page_response = response.text
       
        # rev_index is the number of the current review in all_reviews_list
        rev_index = len(all_reviews_list) + 1
        print ("Processing page "+str(i)+".")
        data_reviews = parseResponse(page_response, amazon_url, rev_index)
        
        if data_reviews == {}: break
        
        i+=1
        all_reviews_list = dict(all_reviews_list.items() + data_reviews.items())
        
        # set a sleeping time
        if execute_sleep:
            sleep(random.uniform(1,3))
    
    return all_reviews_list


def parseProduct(asin, amazon_url, retrying_time):
     headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}   
     url = amazon_url + "/dp/" + asin
     
     try:
         # Adding verify=False to avold ssl related issues
         response = requests.get(url, headers=headers)
         
         doc = html.fromstring(response.content)
         XPATH_NAME = '//h1[@id="title"]//text()'
         XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
         XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
         XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
         XPATH_AVAILABILITY = '//div[@id="availability"]//text()'
         XPATH_RATING = '//span[@id="acrPopover"]'
         XPATH_REVIEWS_NUMBER = '//span[@id="acrCustomerReviewText"]//text()'
         
         raw_name = doc.xpath(XPATH_NAME)
         raw_sale_price = doc.xpath(XPATH_SALE_PRICE)
         raw_category = doc.xpath(XPATH_CATEGORY)
         raw_original_price = doc.xpath(XPATH_ORIGINAL_PRICE)
         raw_availability = doc.xpath(XPATH_AVAILABILITY)
         raw_rating_elem = doc.xpath(XPATH_RATING)
         raw_product_rating = []
         if raw_rating_elem != []:
             for elem in raw_rating_elem:
                 raw_product_rating = elem.attrib['title']
         raw_number_of_review = doc.xpath(XPATH_REVIEWS_NUMBER)
         
         name = ' '.join(''.join(raw_name).split()) if raw_name else None
         sale_price = ' '.join(''.join(raw_sale_price).split()).strip() if raw_sale_price else None
         category = ' > '.join([i.strip() for i in raw_category]) if raw_category else None
         original_price = ''.join(raw_original_price).strip() if raw_original_price else None
         availability = ''.join(raw_availability).strip() if raw_availability else None
         rating = ''.join(raw_product_rating).replace(' su 5 stelle','') if raw_product_rating else None
         reviews_number = ''.join(raw_number_of_review).replace(' recensioni clienti','') if raw_number_of_review else None
                     
         if not original_price:
             original_price = sale_price
             
         # retrying in case of captcha (only first time)
         if not name:
             if retrying_time:
                 raise ValueError('captcha')
             parseProduct(asin, amazon_url, True)
             return
             
         data = {
                 'name': name,
                 'salePrice': sale_price,
                 'category': category,
                 'originalPrice': original_price,
                 'availability': availability,
                 'url': url,
                 'date': datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
                 'numberOfReviews': reviews_number,
                 'productRating': rating
                 }
         return data
     
     except:
         print ("Error")

    
def executeScraper(asin, amazon_domain):
    reviews_data = getReviews(asin, amazon_domain)
    product_data = parseProduct(asin, amazon_domain, False)
    return [reviews_data, product_data]