from scrapy import cmdline


name = 'ckxxbot'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())