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
            ('/listaccountaccountstatus/(.*)',   ListAccountAccountStatus),
            ('/listaccountinvestsum/(.*)',       ListAccountInvestSum),
            ('/addaccount',         AddAccount),
            ('/doaddaccount',       DoAddAccount)]

def addaccount(request,name,description,currencyname,accounttype,liquiditytype):
    dict_name = request.request.get('dict_name', USERDICT)
    oaccount = Account(parent=dict_key(dict_name))
    oaccount.name         = name
    oaccount.description  = description
    oaccount.currencyname = currencyname
    oaccount.accounttype  = accounttype
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
                rows = [[account.name,account.currencyname,account.accounttype,account.liquiditytype,getaccountROI(self,account),buttonformget("/viewaccount/" + account.key.urlsafe(),"View"),buttonformget("/listaccountaccountstatus/" + account.key.urlsafe(),"List Status"),buttonformget("/addaccountstatus/" + account.key.urlsafe(),"Add Status"),buttonformget("/listaccountinvestsum/" + account.key.urlsafe(),"List Invest Sum"),buttonformget("/addinvestsum/" + account.key.urlsafe(),"Add Invest Sum")] for account in getallaccounts(self)]
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

                types = [c.name for c in getallaccounttypes(self)]
                types  = ["<option value=\""+ c + "\">" + c + "</option>" for c in types]
                typehtml  = "\n".join(types)
                
                
                content.append(ADD_ACCOUNT_TEMPLATE.replace("%HTMLCUR%",curhtml).replace("%HTMLACCOUNTTYPE%",typehtml).replace("%HTMLLIQUIDITYTYPE%",liqhtml))
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
        accounttype        = self.request.get('accounttype')
        accountliquiditytype   = self.request.get('accountliquiditytype')
        account = addaccount(self,accountname,accountdescription,accountcurrency,accounttype,accountliquiditytype)
        self.redirect("/listaccounts")
# [END DoAddChiChar]

# [START ListAccountAccountStatus]
class ListAccountAccountStatus(webapp2.RequestHandler):
    def get(self,accountid):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():

                dict_name      = self.request.get('dict_name',USERDICT)
                account_key = ndb.Key(urlsafe=accountid)
                account = account_key.get()
                
                content.append(html("h1","Account Status for account " + account.name))
                content.append("<hr>")
                rows = [[datedumponly(utc2local(accountstatus.date)),accountstatus.value,getcurrencyfromaccountname(accountstatus.account)] for accountstatus in getaccountstatussforaccount(self,account.name)]
                content.append(htmltable(htmlrows(rows)))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/addaccountstatus","Add"),buttonformget("/","Home")])))
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

# [START ListAccountInvestSum]
class ListAccountInvestSum(webapp2.RequestHandler):
    def get(self,accountid):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():

                dict_name      = self.request.get('dict_name',USERDICT)
                account_key = ndb.Key(urlsafe=accountid)
                account = account_key.get()
                
                content.append(html("h1","Account Status for account " + account.name))
                content.append("<hr>")
                rows = [[datedumponly(utc2local(investsum.date)),investsum.value,getcurrencyfromaccountname(investsum.account)] for investsum in getinvestsumsforaccount(self,account.name)]
                content.append(htmltable(htmlrows(rows)))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/addinvestsum","Add"),buttonformget("/","Home")])))
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
