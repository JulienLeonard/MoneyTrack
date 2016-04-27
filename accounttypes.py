from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from accounttypetemplates    import *
from mydicts           import *
from myschemas         import *
from modelutils        import *
from htmlutils         import *
from utils             import *
from timeutils         import *
from admin             import *

def accounttypehandlers():
    # return [('/listaccounttypes',       ListAccounttypes),
    #         ('/mylistaccounttypes/(.*)',MyListAccounttypes),
    #         ('/addaccounttype',         AddAccounttype),
    #         ('/doaddaccounttype',       DoAddAccounttype),
    #         ('/mydoaddaccounttype/(.*)',MyDoAddAccounttype)]
    return [('/listaccounttypes',       ListAccountTypes),
            ('/addaccounttype',         AddAccountType),
            ('/doaddaccounttype',       DoAddAccountType)]

def addaccounttype(request,name):
    dict_name = request.request.get('dict_name', USERDICT)
    oaccounttype = AccountType(parent=dict_key(dict_name))
    oaccounttype.name         = name
    oaccounttype.put()
    return oaccounttype
                
    
# [START ListAccounttype]
class ListAccountTypes(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(html("h1","Account Account Types"))
                content.append("<hr>")
                rows = [[accounttype.name,buttonformget("/viewaccounttype/" + accounttype.key.urlsafe(),"View")] for accounttype in getallaccounttypes(self)]
                content.append(htmltable(htmlrows(rows)))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/addaccounttype","Add"),buttonformget("/","Home")])))
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
class AddAccountType(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(ADD_ACCOUNTTYPE_TEMPLATE)
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

# [START DoAddAccounttype]
class DoAddAccountType(webapp2.RequestHandler):
    def post(self):
        accounttypename         = self.request.get('accounttypename')
        accounttype = addaccounttype(self,accounttypename)
        self.redirect("/listaccounttypes")
# [END DoAddChiChar]

