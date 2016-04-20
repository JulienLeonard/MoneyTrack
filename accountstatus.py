from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from accountstatustemplates    import *
from mydicts           import *
from myschemas         import *
from modelutils        import *
from htmlutils         import *
from utils             import *
from timeutils         import *
from admin             import *

def accountstatushandlers():
    # return [('/listaccountstatuss',       ListAccountstatuss),
    #         ('/mylistaccountstatuss/(.*)',MyListAccountstatuss),
    #         ('/addaccountstatus',         AddAccountstatus),
    #         ('/doaddaccountstatus',       DoAddAccountstatus),
    #         ('/mydoaddaccountstatus/(.*)',MyDoAddAccountstatus)]
    return [('/listaccountstatuss',       ListAccountStatuss),
            ('/addaccountstatus',         AddAccountStatus),
            ('/doaddaccountstatus',       DoAddAccountStatus)]

def addaccountstatus(request,account,value,date):
    dict_name = request.request.get('dict_name', USERDICT)
    oaccountstatus = AccountStatus(parent=dict_key(dict_name))
    oaccountstatus.account   = account
    oaccountstatus.value     = value
    if not date == None:
        oaccountstatus.date      = date
    oaccountstatus.put()
    return oaccountstatus
                
    
# [START ListAccountstatus]
class ListAccountStatuss(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(html("h1","Account Status"))
                content.append("<hr>")
                rows = [[accountstatus.account,accountstatus.value,date2string(utc2local(accountstatus.date))] for accountstatus in getallaccountstatuss(self)]
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

# [START AddGeneration]
class AddAccountStatus(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                
                curnames      = [c.name for c in getallaccounts(self)]
                curlist       = ["<option value=\""+ c + "\">" + c + "</option>" for c in curnames]
                htmlaccounts  = "\n".join(curlist)

                content.append(ADD_ACCOUNTSTATUS_TEMPLATE.replace("%HTMLACCOUNTS%",htmlaccounts))
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

# [START DoAddAccountstatus]
class DoAddAccountStatus(webapp2.RequestHandler):
    def post(self):
        accountstatusaccount   = self.request.get('accountstatusaccount')
        accountstatusvalue     = self.request.get('accountstatusvalue')
        accountstatus = addaccountstatus(self,accountstatusaccount,accountstatusvalue,None)
        self.redirect("/listaccountstatuss")
# [END DoAddChiChar]

