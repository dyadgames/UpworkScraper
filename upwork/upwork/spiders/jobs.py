# -*- coding: utf-8 -*-
import scrapy
from helping_functions import make_url, extract_num, make_valid_csv, find_num_pages, extract_time_posted
from input_functions import key_words_f, numeric_data_f
import csv
from scrapy import signals

key_words = input("Enter keywords: ")
est_budget = input("Enter min budget: ")
max_post_date = input("Enter max post date in days: ")
lim_num_results = input("Enter max number of results: ")
est_budget, lim_num_results, max_post_date = numeric_data_f(est_budget, lim_num_results, max_post_date)


key_words = key_words_f(key_words)
page = 1
num_jobs_counter = 0
flag_continue = True
num_of_pair = 0
KEY_WORDS = key_words[num_of_pair]
ALL_JOBS = set()


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['upwork.com']
    start_urls = [make_url(KEY_WORDS, 1)]

    def parse(self, response):
        global page, num_jobs_counter, flag_continue, num_of_pair, KEY_WORDS, ALL_JOBS
        total_num_jobs = response.xpath("normalize-space(/html/body/div[1]/div[2]/div/div[2]/div[2]/section/div/strong)").get()
        num_pages = find_num_pages(total_num_jobs)
        jobs = response.xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/div/div/section")
        for job in jobs:
            job_name = job.xpath(".//div[1]/div[1]/h4/a/up-c-line-clamp/text()").get()
            if job_name == None:
                continue
            l = len(ALL_JOBS)
            ALL_JOBS.add(job_name)
            if l == len(ALL_JOBS):
                continue
            job_budget = job.xpath("normalize-space(.//div[2]/div[1]/strong/span/text())").get()
            job_budget = extract_num(job_budget)
            if job_budget >= est_budget:
                num_jobs_counter += 1
                job_url = "https://www.upwork.com" + str(job.xpath(".//div[1]/div[1]/h4/a/@href").get())
                yield response.follow(url=job_url, callback = self.parse_job, meta = {"job_name": make_valid_csv(job_name), "job_budget": str(job_budget), "job_url": job_url})

                if num_jobs_counter == lim_num_results:
                    flag_continue = False
                    break
        page += 1
        if page <= num_pages and flag_continue:
            yield scrapy.Request(url = make_url(KEY_WORDS, page), callback=self.parse)
        else:
            if num_of_pair < len(key_words) - 1:
                num_of_pair += 1
                page = 1
                num_jobs_counter = 0
                flag_continue = True
                KEY_WORDS = key_words[num_of_pair]
                yield scrapy.Request(url = make_url(KEY_WORDS, page), callback=self.parse)

        
    def parse_job(self, response):
        global flag_continue
        job_time_posted = response.xpath("/html/body/div/div[2]/div/visitor-job-details/div/div/div/section[1]/div/span/text()").get()
        job_name = response.xpath("/html/body/div/div[2]/div/visitor-job-details/div[1]/div/div/header/h2/text()").get()
        job_time_posted = extract_time_posted(job_time_posted)
        if max_post_date == None:
            yield {
                "job name": make_valid_csv(job_name),
                "job budget": response.request.meta["job_budget"],
                "job url": response.request.meta["job_url"]
            }
        elif job_time_posted < max_post_date:
            yield {
                "job name": make_valid_csv(job_name),
                "job budget": response.request.meta["job_budget"],
                "job url": response.request.meta["job_url"]
            }
        else:
            flag_continue = False
