from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from payeetemplates    import *
from mydicts           import *
from myschemas         import *
from modelutils        import *
from htmlutils         import *
from utils             import *
from timeutils         import *
from admin             import *

def payeehandlers():
    # return [('/listpayees',       ListPayees),
    #         ('/mylistpayees/(.*)',MyListPayees),
    #         ('/addpayee',         AddPayee),
    #         ('/doaddpayee',       DoAddPayee),
    #         ('/mydoaddpayee/(.*)',MyDoAddPayee)]
    return [('/listpayees',       ListPayees),
            ('/addpayee',         AddPayee),
            ('/doaddpayee',       DoAddPayee)]

def addpayee(request,name,category):
    dict_name = request.request.get('dict_name', USERDICT)
    opayee = Payee(parent=dict_key(dict_name))
    opayee.name         = name
    opayee.category     = category
    opayee.put()
    return opayee
                
    
# [START ListPayee]
class ListPayees(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(html("h1","Payees"))
                content.append("<hr>")
                rows = [[payee.name,payee.category,buttonformget("/viewpayee/" + payee.key.urlsafe(),"View")] for payee in getallpayees(self)]
                content.append(htmltable(htmlrows(rows)))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/addpayee","Add"),buttonformget("/","Home")])))
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
class AddPayee(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                htmlcategories = 'TODO'
                content.append(ADD_PAYEE_TEMPLATE.replace("%HTMLCATEGORIES%",htmlcategories))
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

# [START DoAddPayee]
class DoAddPayee(webapp2.RequestHandler):
    def post(self):
        payeename         = self.request.get('payeename')
        payeecategory     = self.request.get('payeecategory')
        payee = addpayee(self,payeename,payeecategory)
        self.redirect("/listpayees")
# [END DoAddChiChar]

