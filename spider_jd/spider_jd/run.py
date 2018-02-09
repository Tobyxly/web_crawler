from scrapy import cmdline


name = 'jdbot'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())