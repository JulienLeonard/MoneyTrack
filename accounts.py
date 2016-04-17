from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from mydicts          import *
from myschemas        import *
from modelutils       import *
from htmlutils        import *
from utils            import *
from timeutils        import *
from admin            import *

def accounthandlers():
    # return [('/listaccounts',       ListAccounts),
    #         ('/mylistaccounts/(.*)',MyListAccounts),
    #         ('/addaccount',         AddAccount),
    #         ('/doaddaccount',       DoAddAccount),
    #         ('/mydoaddaccount/(.*)',MyDoAddAccount)]
    return [('/listaccounts',       ListAccounts),
            ('/addaccount',         AddAccount),
            ('/doaddaccount',       DoAddAccount)]

def addaccount(request,name,description,currencyname):
    if email:
        dict_name = request.request.get('dict_name', USERDICT)
        oaccount = Account(parent=dict_key(dict_name))
        oaccount.name         = name
        oaccount.description  = description
        oaccount.currencyname = currencyname
        oaccount.put()
    return oaccount
                
    
# [START ListAccount]
class ListAccounts(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(html("h1","Accounts"))
                content.append("<hr>")
                rows = [[account.name,account.description,account.currencyname,buttonformget("/viewaccount/" + account.key.urlsafe(),"View")] for account in getallaccounts(self)]
                content.append(htmltable(htmlrows(rows)))
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
class AddAccount(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(html("h1","Add Account"))
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

# [START DoAddAccount]
class DoAddAccount(webapp2.RequestHandler):
    def post(self):
        accountname         = self.request.get('accountname')
        accountdescription  = self.request.get('accountdescription')
        accountcurrency     = self.request.get('accountcurrency')
        account = addaccount(self,accountname,accountdescription,accountcurrency)
        self.redirect("/listaccounts")
# [END DoAddChiChar]

