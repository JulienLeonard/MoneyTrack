from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from payercategorytemplates    import *
from mydicts           import *
from myschemas         import *
from modelutils        import *
from htmlutils         import *
from utils             import *
from timeutils         import *
from admin             import *

def payercategoryhandlers():
    # return [('/listpayercategorys',       ListPayercategorys),
    #         ('/mylistpayercategorys/(.*)',MyListPayercategorys),
    #         ('/addpayercategory',         AddPayercategory),
    #         ('/doaddpayercategory',       DoAddPayercategory),
    #         ('/mydoaddpayercategory/(.*)',MyDoAddPayercategory)]
    return [('/listpayercategorys',       ListPayerCategorys),
            ('/addpayercategory',         AddPayerCategory),
            ('/doaddpayercategory',       DoAddPayerCategory)]

def addpayercategory(request,name):
    dict_name = request.request.get('dict_name', USERDICT)
    opayercategory = PayerCategory(parent=dict_key(dict_name))
    opayercategory.name         = name
    opayercategory.put()
    return opayercategory
                
    
# [START ListPayercategory]
class ListPayerCategorys(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(html("h1","Payer Categories"))
                content.append("<hr>")
                rows = [[payercategory.name,buttonformget("/viewpayercategory/" + payercategory.key.urlsafe(),"View")] for payercategory in getallpayercategorys(self)]
                content.append(htmltable(htmlrows(rows)))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/addpayercategory","Add"),buttonformget("/","Home")])))
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
class AddPayerCategory(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(ADD_PAYERCATEGORY_TEMPLATE)
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

# [START DoAddPayercategory]
class DoAddPayerCategory(webapp2.RequestHandler):
    def post(self):
        payercategoryname         = self.request.get('payercategoryname')
        payercategory = addpayercategory(self,payercategoryname)
        self.redirect("/listpayercategorys")
# [END DoAddChiChar]

