from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from currencychangetemplates    import *
from mydicts           import *
from myschemas         import *
from modelutils        import *
from htmlutils         import *
from utils             import *
from timeutils         import *
from admin             import *

def currencychangehandlers():
    # return [('/listcurrencychanges',       ListCurrencyChanges),
    #         ('/mylistcurrencychanges/(.*)',MyListCurrencyChanges),
    #         ('/addcurrencychange',         AddCurrencyChange),
    #         ('/doaddcurrencychange',       DoAddCurrencyChange),
    #         ('/mydoaddcurrencychange/(.*)',MyDoAddCurrencyChange)]
    return [('/listcurrencychanges',  ListCurrencyChanges),
            ('/addcurrencychange',    AddCurrencyChange),
            ('/doaddcurrencychange',  DoAddCurrencyChange),
            ('/deletecurrencychange/(.*)', DeleteCurrencyChange)]

def addcurrencychange(request,currencyname1,currencyname2,value,date):
    dict_name = request.request.get('dict_name', USERDICT)
    ocurrencychange = CurrencyChange(parent=dict_key(dict_name))
    ocurrencychange.currencyname1 = currencyname1
    ocurrencychange.currencyname2 = currencyname2
    ocurrencychange.value         = value
    if not date == None:
        ocurrencychange.date      = date
    ocurrencychange.put()
    return ocurrencychange
                
    
# [START ListCurrencyChange]
class ListCurrencyChanges(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(html("h1","Currency Changes"))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/addcurrencychange","Add Currency Change"),buttonformget("/","Home")])))
                content.append("<hr>")
                rows = [[currencychange.currencyname1,currencychange.currencyname2,currencychange.value,date2string(utc2local(currencychange.date)),buttonformget("/deletecurrencychange/" + currencychange.key.urlsafe(),"Del")] for currencychange in getallcurrencychanges(self)]
                content.append(htmltable(htmlrows(rows)))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/addcurrencychange","Add Currency Change"),buttonformget("/","Home")])))
                content.append("<hr>")
            else:
                content = ['Not Authorized']
                url_linktext = 'Logout'
                content.append(htmllink(url,url_linktext))
        else:
            content = ['You must login']
            url_linktext = 'Login'
            content.append(htmllink(url,url_linktext))
        
        writehtmlresponse(self,htmlcenter(content))

# [START AddGeneration]
class AddCurrencyChange(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():

                template = ADD_CURRENCY_CHANGE_TEMPLATE
                
                curnames      = [c.name for c in getallcurrencys(self)]
                curlist       = ["<option value=\""+ c + "\">" + c + "</option>" for c in curnames]
                htmlcurrency1  = "\n".join(curlist)

                htmlcurrency2  = "\n".join(curlist)
                
                content.append(template.replace("%HTMLCURRENCY1%",htmlcurrency1).replace("%HTMLCURRENCY2%",htmlcurrency2))
            else:
                content = ['Not Authorized']
                url_linktext = 'Logout'
                content.append(htmllink(url,url_linktext))
        else:
            content = ['You must login']
            url_linktext = 'Login'
            content.append(htmllink(url,url_linktext))

        writehtmlresponse(self,htmlcenter(content))

# [END AddGeneration]

# [START DoAddCurrencyChange]
class DoAddCurrencyChange(webapp2.RequestHandler):
    def post(self):
        currencychangecurrencyname1 = self.request.get('currencychangecurrencyname1')
        currencychangecurrencyname2 = self.request.get('currencychangecurrencyname2')
        currencychangevalue         = self.request.get('currencychangevalue')
        currencychange = addcurrencychange(self,currencychangecurrencyname1,currencychangecurrencyname2,currencychangevalue,None)
        self.redirect("/listcurrencychanges")
# [END DoAddChiChar]


# [START DeleteCurrencyChange]
class DeleteCurrencyChange(webapp2.RequestHandler):
    def get(self,isumid):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                dict_name      = self.request.get('dict_name',USERDICT)
                isum_key = ndb.Key(urlsafe=isumid)
                isum = isum_key.get()
                isum.key.delete()
                
        self.redirect("/listcurrencychanges")
# [END DoAddChiChar]
