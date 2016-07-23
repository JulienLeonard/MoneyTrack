from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from payeecategorytemplates    import *
from mydicts           import *
from myschemas         import *
from modelutils        import *
from htmlutils         import *
from utils             import *
from timeutils         import *
from admin             import *

def payeecategoryhandlers():
    # return [('/listpayeecategorys',       ListPayeecategorys),
    #         ('/mylistpayeecategorys/(.*)',MyListPayeecategorys),
    #         ('/addpayeecategory',         AddPayeecategory),
    #         ('/doaddpayeecategory',       DoAddPayeecategory),
    #         ('/mydoaddpayeecategory/(.*)',MyDoAddPayeecategory)]
    return [('/listpayeecategorys',       ListPayeeCategorys),
            ('/addpayeecategory',         AddPayeeCategory),
            ('/doaddpayeecategory',       DoAddPayeeCategory)]
                
    
# [START ListPayeecategory]
class ListPayeeCategorys(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(html("h1","Payee Categories"))
                content.append("<hr>")
                rows = [[payeecategory.name,buttonformget("/viewpayeecategory/" + payeecategory.key.urlsafe(),"View")] for payeecategory in getallpayeecategorys(self)]
                content.append(htmltable(htmlrows(rows)))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/addpayeecategory","Add"),buttonformget("/","Home")])))
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
class AddPayeeCategory(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(ADD_PAYEECATEGORY_TEMPLATE)
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

# [START DoAddPayeecategory]
class DoAddPayeeCategory(webapp2.RequestHandler):
    def post(self):
        payeecategoryname         = self.request.get('payeecategoryname')
        payeecategory = addpayeecategory(self,payeecategoryname)
        self.redirect("/listpayeecategorys")
# [END DoAddChiChar]

