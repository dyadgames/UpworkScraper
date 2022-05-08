import re

def make_url(key_words, page):
    url = f"https://www.upwork.com/search/jobs/t/1/?page={page}&q="
    key_words = key_words.title()
    key_words = list(key_words.split())
    if len(key_words) == 0:
        url = f"https://www.upwork.com/search/jobs/t/1/?page={page}&sort=recency"
        return url
    for i in range(len(key_words)):
        if i == len(key_words) - 1:
            url += key_words[i]
            url += "&sort=recency"
        else:
            url += key_words[i]
            url += "+"
    return url

def extract_num(job_budget):
    return int(re.sub("[^0-9]", "", job_budget))

def make_valid_csv(job_name):
    return re.sub(",", "", job_name)

def find_num_pages(total_num_jobs):
    num_pages = int(extract_num(total_num_jobs))//10
    if num_pages > 500:
        num_pages = 500
    return num_pages


def extract_time_posted(job_time_posted):
    if "minut" in job_time_posted:
        job_time_posted = -1
    elif "hour" in job_time_posted:
        job_time_posted = -1
    elif "day" in job_time_posted:
        job_time_posted = extract_num(job_time_posted)
    elif "month" in job_time_posted:
        job_time_posted = 30 * extract_num(job_time_posted)
    elif "year" in job_time_posted:
        job_time_posted = 365 * 30 * extract_num(job_time_posted)
    return job_time_posted
