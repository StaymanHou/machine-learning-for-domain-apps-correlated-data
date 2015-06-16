from peewee import *
import json
from Wappalyzer import Wappalyzer, WebPage

db = SqliteDatabase('domain.db')
wappalyzer = Wappalyzer.latest()


class Domain(Model):
    name = CharField()
    categories = CharField()  # JSON str
    subdomains = TextField()  # JSON str
    apps = TextField()  # JSON str

    class Meta:
        database = db  # This model uses the "people.db" database.

counter = 0
total = Domain.select().count()

for domain in Domain.select().iterator():
    counter += 1
    if counter % 100 == 0:
        print counter, '/', total
    if len(json.loads(domain.apps)) > 0:
        continue
    try:
        webpage = WebPage.new_from_url('http://'+domain.name)
    except Exception, e:
        continue
    domain.apps = json.dumps(list(wappalyzer.analyze(webpage)))
    domain.save()

######################## create db
# db.create_tables([Domain])

# org_data = json.loads(open('../alexa.json').read())

# cats_data = {}
# for org_datum in org_data:
#     domain = org_datum[0]
#     cat = org_datum[1]
#     if not cat in cats_data:
#         cats_data[cat] = []
#     cats_data[cat].append(org_datum)

# counter = 0

# for cat_name in cats_data.keys():
#     alexa_scanned_data = json.loads(open('alexa_sub_'+cat_name+'.json').read())
#     for alexa_scanned_datum in alexa_scanned_data:
#         counter += 1
#         if counter % 100 == 0:
#             print counter
#         domain_name = alexa_scanned_datum['domain']
#         try:
#             domain = Domain.get(Domain.name == domain_name)
#         except Domain.DoesNotExist:
#             categories = [alexa_scanned_datum['category']]
#             del alexa_scanned_datum['domain']
#             del alexa_scanned_datum['category']
#             subdomains = []
#             for subdomain, flag in alexa_scanned_datum.iteritems():
#                 if flag:
#                     subdomains.append(subdomain)
#             apps = []
#             Domain.create(name=domain_name, categories=json.dumps(categories), subdomains=json.dumps(subdomains), apps=json.dumps(apps))
#         else:
#             categories = json.loads(domain.categories)
#             if not alexa_scanned_datum['category'] in categories:
#                 categories.append(alexa_scanned_datum['category'])
#                 domain.categories = json.dumps(categories)
#                 domain.save()
