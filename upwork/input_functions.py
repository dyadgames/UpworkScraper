def key_words_f(key_words):
    key_words = key_words.title()
    if key_words == "":
        key_words = []
    else:
        key_words = key_words.split(",")
    return key_words

def numeric_data_f(est_budget, lim_num_results, max_post_date):
    if est_budget == "":
        est_budget = 0
    else:
        est_budget = int(est_budget)
    
    if lim_num_results == "":
        lim_num_results = -1
    else:
        lim_num_results = int(lim_num_results)
    
    if max_post_date == "":
        max_post_date = None
    else:
        max_post_date = int(max_post_date)
    return est_budget, lim_num_results, max_post_date