from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from ownertemplates    import *
from mydicts           import *
from myschemas         import *
from modelutils        import *
from htmlutils         import *
from utils             import *
from timeutils         import *
from admin             import *

def ownerhandlers():
    # return [('/listowners',       ListOwners),
    #         ('/mylistowners/(.*)',MyListOwners),
    #         ('/addowner',         AddOwner),
    #         ('/doaddowner',       DoAddOwner),
    #         ('/mydoaddowner/(.*)',MyDoAddOwner)]
    return [('/listowners',       ListOwners),
            ('/addowner',         AddOwner),
            ('/doaddowner',       DoAddOwner)]

def addowner(request,name):
    dict_name = request.request.get('dict_name', USERDICT)
    oowner = Owner(parent=dict_key(dict_name))
    oowner.name         = name
    oowner.put()
    return oowner
                
    
# [START ListOwner]
class ListOwners(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(html("h1","Account Owners"))
                content.append("<hr>")
                rows = [[owner.name,buttonformget("/viewowner/" + owner.key.urlsafe(),"View")] for owner in getallowners(self)]
                content.append(htmltable(htmlrows(rows)))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/addowner","Add"),buttonformget("/","Home")])))
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
class AddOwner(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(ADD_OWNER_TEMPLATE)
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

# [START DoAddOwner]
class DoAddOwner(webapp2.RequestHandler):
    def post(self):
        ownername         = self.request.get('ownername')
        owner = addowner(self,ownername)
        self.redirect("/listowners")
# [END DoAddChiChar]

