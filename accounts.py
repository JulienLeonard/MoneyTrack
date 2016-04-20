from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from accounttemplates import *
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

def addaccount(request,name,description,currencyname,liquiditytype):
    dict_name = request.request.get('dict_name', USERDICT)
    oaccount = Account(parent=dict_key(dict_name))
    oaccount.name         = name
    oaccount.description  = description
    oaccount.currencyname = currencyname
    oaccount.liquiditytype = liquiditytype
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
                rows = [[account.name,account.currencyname,account.liquiditytype,buttonformget("/viewaccount/" + account.key.urlsafe(),"View"),buttonformget("/addaccountstatus/" + account.key.urlsafe(),"+Status")] for account in getallaccounts(self)]
                content.append(htmltable(htmlrows(rows)))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/addaccount","Add"),buttonformget("/","Home")])))
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
class AddAccount(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():

                curnames = [c.name for c in getallcurrencys(self)]
                curlist  = ["<option value=\""+ c + "\">" + c + "</option>" for c in curnames]
                curhtml  = "\n".join(curlist)

                liqs = [c.name for c in getallliquiditytypes(self)]
                liqs  = ["<option value=\""+ c + "\">" + c + "</option>" for c in liqs]
                liqhtml  = "\n".join(liqs)
                
                content.append(ADD_ACCOUNT_TEMPLATE.replace("%HTMLCUR%",curhtml).replace("%HTMLLIQUIDITYTYPE%",liqhtml))
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

# [START DoAddAccount]
class DoAddAccount(webapp2.RequestHandler):
    def post(self):
        accountname         = self.request.get('accountname')
        accountdescription  = self.request.get('accountdescription')
        accountcurrency     = self.request.get('accountcurrency')
        accountliquiditytype   = self.request.get('accountliquiditytype')
        account = addaccount(self,accountname,accountdescription,accountcurrency,accountliquiditytype)
        self.redirect("/listaccounts")
# [END DoAddChiChar]

