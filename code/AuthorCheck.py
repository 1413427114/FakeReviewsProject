# -*- coding: utf-8 -*-
import requests
import json
from dateutil import parser as dateparser
import ReviewTextAnalisys as rta
import random

user_agents = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
               'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36', 
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36']

def getCustomerId(user_code, amazon_domain):
    header = {'User-Agent': user_agents[random.randint(0, (len(user_agents)-1))]}
    customer_url = amazon_domain + "/gp/profile/amzn1.account." + user_code + "/"
    response = requests.get(customer_url, headers=header)
    page_response = response.text

    try:
        customer_id = \
        (page_response.split('window.CustomerProfileRootProps = {\"locale\":\"it\",\"customerId\":\"')[1]).split('\"')[
            0]
    except:
        customer_id = None
    try:
        customer_rank = (page_response.split('topReviewerInfo\":{\"rank\":\"')[1]).split('\"')[0]
    except:
        customer_rank = "-1"
    return customer_id, int(customer_rank.replace('.', ''))


def getHelpfulVotesAndTotalReviewsCount(customer_id, amazon_domain):
    header = {'User-Agent': user_agents[random.randint(0, (len(user_agents)-1))]}
    customer_info_url = amazon_domain + "/hz/gamification/api/contributor/dashboard/" + customer_id
    response = requests.get(customer_info_url, headers=header)
    try:
        json_response = json.loads(response.text.decode("utf-8"))
    except:
        return "-1", "-1"

    try:
        helpful_votes = json_response['helpfulVotes']['helpfulVotesData']['count']
    except:
        helpful_votes = "-1"
    try:
        reviews_count = json_response['reviews']['reviewsCountData']['count']
    except:
        reviews_count = "-1"
    return int(helpful_votes.replace('.', '')), int(reviews_count.replace('.', ''))


def getReviews(user_code, offset, amazon_domain):
    header = {
        'User-Agent': user_agents[random.randint(0, (len(user_agents)-1))],
        'X-Requested-With': 'XMLHttpRequest',
    }
    customer_rev_url = amazon_domain + "/gp/profile/amzn1.account." + user_code + "/activity_feed?review_offset=" + str(
        offset)
    response = requests.get(customer_rev_url, headers=header)
    try:
        json_response = json.loads(response.text)
    except:
        return None
    return json_response


def getLatestCustomerReviewAndTextAnalisys(user_code, amazon_domain):
    json_response = getReviews(user_code, 0, amazon_domain)
    if json_response:
        reviews_data = json_response['reviews']
        avg, rev_num, data = 0, 0, {}
        for rev in reviews_data:
            rev_num += 1
            avg += int(rev['ratingToInteger'])
            rev_data = {
                rev_num: {
                    'reviewId': rev['id'],
                    'reviewTitle': rev['title'],
                    'verifiedPurchase': rev['verifiedPurchase'],
                    'reviewDate': dateparser.parse(rev['date']).strftime('%d %b %Y'),
                    'reviewRating': rev['ratingToInteger'],
                    'reviewProductAsin': rev['productAsin'],
                    'reviewText': (''.join((x + ' ') for x in rev['textArray'])),
                }
            }
            data = dict(data.items() + rev_data.items())

        if rev_num > 0:
            customer_review = {
                'reviews': data,
                'avgReviewsRating': float(avg) / rev_num,
                'trigrams': rta.executeAnalisys(data)
            }

            return customer_review
    return {}

