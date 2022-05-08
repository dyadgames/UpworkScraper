import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from upwork.spiders.jobs import JobsSpider


process = CrawlerProcess(settings=get_project_settings())
process.crawl(JobsSpider)
process.start()