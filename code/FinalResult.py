# -*- coding: utf-8 -*-

import json


def checkReview(review):
    final_score = review['finalScore']
    score_details = review['scoreDetails']
    warning_score = 0  # ws<1 è affidabile, 1<ws<2 è in warning, w>2 è fake
    
    vp_score = score_details['verifiedPurchase']
    rd_score = score_details['reviewDate']
    rbu_score = score_details['reviewByUser']
    rh_score = score_details['reviewHelpfulness']
    v_score = score_details['variance']
    rt_score = score_details['repeatedTrigrams']
    vr_score = score_details['vineReview']
    rl_score = score_details['reviewLength']
    sr_score = score_details['shortAndRepetitive']

    r_score = score_details['authorReliability']['rank']
    eg_score = score_details['authorReliability']['easyGrader']
    otr_score = score_details['authorReliability']['oneTimeReviewer']
    rr_score = score_details['authorReliability']['repetitiveReviewer']

    # computing warning score
    # per review
    ''' check values '''
    vp_score = 0 if vp_score > 0 else 0.3
    rd_score = 0 if rd_score > 0 else 0.2
    rbu_score = 0 if rbu_score > 0 else 0.3
    rh_score = 0 if rh_score > 0 else 0.1
    v_score = 0 if v_score >= 0.16 else 0.1  # 0.16 implica che si discosta dal voto medio di al più 0.4 nel rating
    rt_score = 0 if rt_score > 0 else 0.3
    vr_score = 0 if vr_score > 0 else 0.1
    rl_score = 0 if rl_score > 0 else 0.2
    sr_score = 0 if sr_score == 0 else 0.2
    # per reviewer
    r_score = 0 if r_score > 3 else 0.1  # maggiore di 3 significa più o meno nelle prime 1000 posizioni in classifica
    eg_score = 0 if eg_score >= 0 else 0.1
    otr_score = 0 if otr_score >= 0 else 0.1
    rr_score = 0 if rr_score >= 0 else 0.1
    final_score = 0 if final_score > 0 else 0.2

    warning_score = round((
            vp_score + rd_score + rbu_score + rh_score + v_score + rt_score + vr_score + rl_score + sr_score + r_score + eg_score + otr_score + rr_score + final_score), 1)

    data = {
        'warningScore': warning_score,
        'partialScores': {
            'verifiedPurchase': vp_score,
            'reviewDate': rd_score,
            'reviewByUser': rbu_score,
            'reviewHelpfulness': rh_score,
            'variance': v_score,
            'repeatedTrigrams': rt_score,
            'vineReview': vr_score,
            'reviewLength': rl_score,
            'shortAndRepetitive': sr_score,
            'authorRank': r_score,
            'easyGrader': eg_score,
            'oneTimeReviewer': otr_score,
            'repetitiveReviewer': rr_score
        }
    }
        
    return data


def finalResult(asin):
    review_analisys_data = json.load(open('json'+asin+'/analisi_' + asin + '.json'))
    max_score, min_score = float(0), float(10)
    max_rev, min_rev = "", ""
    # test sulle reviews
    trustable, warning, fake = {}, {}, {}
    for review in review_analisys_data:
        warning_scores = checkReview(review_analisys_data[review])
        warning_score = warning_scores['warningScore']
        if warning_score > max_score:
            max_score = warning_score
            max_rev = review
        if warning_score < min_score:
            min_score = warning_score
            min_rev = review
        data = {
            review: {
                'reviewScores': review_analisys_data[review],
                'warningScore': warning_score,
                'partialWarningScores': warning_scores['partialScores']
            }
        }
        if warning_score < 1:
            trustable = dict(trustable.items() + data.items())
        elif warning_score < 2:
            warning = dict(warning.items() + data.items())
        else:
            fake = dict(fake.items() + data.items())
            
    conclusion = {
        'trustable': {
            'totalCount': len(trustable),
            'reviews': trustable
            },
        'warning': {
            'totalCount': len(warning),
            'reviews': warning
            },
        'fake': {
            'totalCount': len(fake),
            'reviews': fake
            },
        'bestScore': (min_rev + ' with ' + str(min_score)),
        'worstScore': (max_rev + ' with ' + str(max_score))
    }

    return conclusion

