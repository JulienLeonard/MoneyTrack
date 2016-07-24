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
            ('/doaddaccountstatus',       DoAddAccountStatus),
            ('/deleteaccountstatus/(.*)',  DeleteAccountStatus)]
    
# [START ListAccountstatus]
class ListAccountStatuss(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(html("h1","Account Status"))
                content.append("<hr>")
                rows = [[accountstatus.account,accountstatus.value,getcurrencyfromaccountname(accountstatus.account),datedumponly(utc2local(accountstatus.date)),buttonformget("/deleteaccountstatus/" + accountstatus.key.urlsafe(),"Del")] for accountstatus in getallaccountstatuss(self)]
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

                content.append(ADD_ACCOUNTSTATUS_TEMPLATE.replace("%HTMLACCOUNTS%",htmlaccounts).replace("%NOW%",datedumponly(localnow())))
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
        accountstatusdate      = self.request.get('accountstatusdate')
        accountstatus = addaccountstatus(self,accountstatusaccount,accountstatusvalue,accountstatusdate)
        self.redirect("/listaccountstatuss")
# [END DoAddChiChar]

# [START DeleteAccountStatus]
class DeleteAccountStatus(webapp2.RequestHandler):
    def get(self,isumid):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                dict_name      = self.request.get('dict_name',USERDICT)
                isum_key = ndb.Key(urlsafe=isumid)
                isum = isum_key.get()
                isum.key.delete()
                
        self.redirect("/listaccountstatuss")
# [END DoAddChiChar]

