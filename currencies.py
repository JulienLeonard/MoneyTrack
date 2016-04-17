from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from currencytemplates import *
from mydicts           import *
from myschemas         import *
from modelutils        import *
from htmlutils         import *
from utils             import *
from timeutils         import *
from admin             import *

def currencyhandlers():
    # return [('/listcurrencys',       ListCurrencys),
    #         ('/mylistcurrencys/(.*)',MyListCurrencys),
    #         ('/addcurrency',         AddCurrency),
    #         ('/doaddcurrency',       DoAddCurrency),
    #         ('/mydoaddcurrency/(.*)',MyDoAddCurrency)]
    return [('/listcurrencies',       ListCurrencys),
            ('/addcurrency',         AddCurrency),
            ('/doaddcurrency',       DoAddCurrency)]

def addcurrency(request,name):
    dict_name = request.request.get('dict_name', USERDICT)
    ocurrency = Currency(parent=dict_key(dict_name))
    ocurrency.name         = name
    ocurrency.put()
    return ocurrency
                
    
# [START ListCurrency]
class ListCurrencys(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(html("h1","Currencies"))
                content.append("<hr>")
                rows = [[currency.name,buttonformget("/viewcurrency/" + currency.key.urlsafe(),"View")] for currency in getallcurrencys(self)]
                content.append(htmltable(htmlrows(rows)))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/addcurrency","Add"),buttonformget("/","Home")])))
                content.append("<hr>")
            else:
                content = ['Not Authorized']
                url_linktext = 'Logout'
                content.append(htmllink(url,url_linktext))
        else:
            content = ['You must login']
            url_linktext = 'Login'
            content.append(htmllink(url,url_linktext))
        
        writehtmlresponse(self,content)

# [START AddGeneration]
class AddCurrency(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(ADD_CURRENCY_TEMPLATE)
            else:
                content = ['Not Authorized']
                url_linktext = 'Logout'
                content.append(htmllink(url,url_linktext))
        else:
            content = ['You must login']
            url_linktext = 'Login'
            content.append(htmllink(url,url_linktext))

        writehtmlresponse(self,content)

# [END AddGeneration]

# [START DoAddCurrency]
class DoAddCurrency(webapp2.RequestHandler):
    def post(self):
        currencyname         = self.request.get('currencyname')
        currency = addcurrency(self,currencyname)
        self.redirect("/listcurrencies")
# [END DoAddChiChar]

