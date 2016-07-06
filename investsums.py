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
            ('/deleteinvestsum/(.*)',  DeleteInvestSum)]

def addinvestsum(request,account,value,date):
    dict_name = request.request.get('dict_name', USERDICT)
    oinvestsum = InvestSum(parent=dict_key(dict_name))
    oinvestsum.account   = account
    oinvestsum.value     = value
    if not date == None:
        oinvestsum.date      = date
    oinvestsum.put()
    return oinvestsum

    
# [START ListInvestSum]
class ListInvestSums(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(html("h1","Invest Sum"))
                content.append("<hr>")
                rows = [[investsum.account,investsum.value,getcurrencyfromaccountname(investsum.account),datedumponly(utc2local(investsum.date)),buttonformget("/deleteinvestsum/" + investsum.key.urlsafe(),"Del")] for investsum in getallinvestsums(self)]
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

# [START AddGeneration]
class AddInvestSum(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                
                curnames      = [c.name for c in getallaccounts(self)]
                curlist       = ["<option value=\""+ c + "\">" + c + "</option>" for c in curnames]
                htmlaccounts  = "\n".join(curlist)

                content.append(ADD_INVESTSUM_TEMPLATE.replace("%HTMLACCOUNTS%",htmlaccounts))
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

# [START DoAddInvestSum]
class DoAddInvestSum(webapp2.RequestHandler):
    def post(self):
        investsumaccount   = self.request.get('investsumaccount')
        investsumvalue     = self.request.get('investsumvalue')
        investsum = addinvestsum(self,investsumaccount,investsumvalue,None)
        self.redirect("/listinvestsums")
# [END DoAddChiChar]

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
# [END DoAddChiChar]

