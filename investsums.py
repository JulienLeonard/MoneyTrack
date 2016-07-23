from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from investsumtemplates    import *
from mydicts           import *
from myschemas         import *
from modelutils        import *
from htmlutils         import *
from utils             import *
from timeutils         import *
from admin             import *

def investsumhandlers():
    # return [('/listinvestsums',       ListInvestSums),
    #         ('/mylistinvestsums/(.*)',MyListInvestSums),
    #         ('/addinvestsum',         AddInvestSum),
    #         ('/doaddinvestsum',       DoAddInvestSum),
    #         ('/mydoaddinvestsum/(.*)',MyDoAddInvestSum)]
    return [('/listinvestsums',       ListInvestSums),
            ('/addinvestsum',         AddInvestSum),
            ('/doaddinvestsum',       DoAddInvestSum),
            ('/deleteinvestsum/(.*)',  DeleteInvestSum),
            ('/editinvestsum/(.*)',    EditInvestSum),
            ('/doeditinvestsum/(.*)',    DoEditInvestSum)]
    
# [START ListInvestSum]
class ListInvestSums(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(html("h1","Invest Sum"))
                content.append("<hr>")
                rows = [[investsum.account,investsum.value,getcurrencyfromaccountname(investsum.account),datedumponly(utc2local(investsum.date)),buttonformget("/editinvestsum/" + investsum.key.urlsafe(),"Edit"),buttonformget("/deleteinvestsum/" + investsum.key.urlsafe(),"Del")] for investsum in getallinvestsums(self)]
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
# [END ListInvestSum]
        
# [START AddInvestSum]
class AddInvestSum(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                
                curnames      = [c.name for c in getallaccounts(self)]
                curlist       = ["<option value=\""+ c + "\">" + c + "</option>" for c in curnames]
                htmlaccounts  = "\n".join(curlist)

                content.append(ADD_INVESTSUM_TEMPLATE.replace("%HTMLACCOUNTS%",htmlaccounts).replace("%NOW%",datedumponly(localnow())))
            else:
                content = ['Not Authorized']
                url_linktext = 'Logout'
                content.append(htmllink(url,url_linktext))
        else:
            content = ['You must login']
            url_linktext = 'Login'
            content.append(htmllink(url,url_linktext))

        writehtmlresponse(self,htmlcenter(content))
# [END AddInvestSum]

# [START DoAddInvestSum]
class DoAddInvestSum(webapp2.RequestHandler):
    def post(self):
        investsumaccount   = self.request.get('investsumaccount')
        investsumvalue     = self.request.get('investsumvalue')
        investsumdate      = self.request.get('investsumdate')
        investsum = addinvestsum(self,investsumaccount,investsumvalue,investsumdate)
        self.redirect("/listinvestsums")
# [END DoAddInvestSum]

# [START DeleteInvestSum]
class DeleteInvestSum(webapp2.RequestHandler):
    def get(self,isumid):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                dict_name      = self.request.get('dict_name',USERDICT)
                isum_key = ndb.Key(urlsafe=isumid)
                isum = isum_key.get()
                isum.key.delete()
                
        self.redirect("/listinvestsums")
# [END DeleteInvestSum]

# [START EditInvestSum]
class EditInvestSum(webapp2.RequestHandler):
    def get(self,isumid):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():

                dict_name      = self.request.get('dict_name',USERDICT)
                isum_key = ndb.Key(urlsafe=isumid)
                investsum = isum_key.get()

                v = float(investsum.value)
                
                accountnames = [c.name for c in getallaccounts(self)]
                aselect  = {c: "" for c in accountnames}
                aselect[investsum.account] = "selected"
                
                acclist       = ["<option value=\""+ c  + "\" " + aselect[c] + ">" + c + "</option>" for c in accountnames]
                htmlaccounts  = "\n".join(acclist)

                template = EDIT_INVESTSUM_TEMPLATE
                
                content.append(template.replace("%MMID%",investsum.key.urlsafe()).replace("%VALUE%",investsum.value).replace("%HTMLACCOUNTS%",htmlaccounts).replace("%NOW%",datedumponly(investsum.date)))
            else:
                content = ['Not Authorized']
                url_linktext = 'Logout'
                content.append(htmllink(url,url_linktext))
        else:
            content = ['You must login']
            url_linktext = 'Login'
            content.append(htmllink(url,url_linktext))

        writehtmlresponse(self,htmlcenter(content))
# [END EditInvestSum]

# [START DoEditInvestSum]
class DoEditInvestSum(webapp2.RequestHandler):
    def post(self,isumid):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                dict_name      = self.request.get('dict_name',USERDICT)
                isum_key = ndb.Key(urlsafe=isumid)
                investsum = isum_key.get()
                investsum.account      = self.request.get('investsumaccount')
                investsum.value        = self.request.get('investsumvalue')
                investsum.date         = dayload(self.request.get('investsumdate'))
                investsum.put()
        self.redirect("/listinvestsums")
# [END DoEditInvestSum]
