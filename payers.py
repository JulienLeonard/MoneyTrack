from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from payertemplates    import *
from mydicts           import *
from myschemas         import *
from modelutils        import *
from htmlutils         import *
from utils             import *
from timeutils         import *
from admin             import *

def payerhandlers():
    # return [('/listpayers',       ListPayers),
    #         ('/mylistpayers/(.*)',MyListPayers),
    #         ('/addpayer',         AddPayer),
    #         ('/doaddpayer',       DoAddPayer),
    #         ('/mydoaddpayer/(.*)',MyDoAddPayer)]
    return [('/listpayers',       ListPayers),
            ('/addpayer',         AddPayer),
            ('/doaddpayer',       DoAddPayer),
            ('/viewpayer/(.*)',   ViewPayer)]

def addpayer(request,name,category):
    dict_name = request.request.get('dict_name', USERDICT)
    opayer = Payer(parent=dict_key(dict_name))
    opayer.name         = name
    opayer.category     = category
    opayer.put()
    return opayer
                
    
# [START ListPayer]
class ListPayers(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(html("h1","Payers"))
                content.append("<hr>")
                rows = [[payer.name,payer.category,buttonformget("/viewpayer/" + payer.key.urlsafe(),"View")] for payer in getallpayers(self)]
                content.append(htmltable(htmlrows(rows)))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/addpayer","Add"),buttonformget("/","Home")])))
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
class AddPayer(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():

                liqs = [c.name for c in getallpayercategorys(self)]
                liqs  = ["<option value=\""+ c + "\">" + c + "</option>" for c in liqs]
                htmlcategories  = "\n".join(liqs)

                content.append(ADD_PAYER_TEMPLATE.replace("%HTMLCATEGORIES%",htmlcategories))
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

# [START DoAddPayer]
class DoAddPayer(webapp2.RequestHandler):
    def post(self):
        payername         = self.request.get('payername')
        payercategory     = self.request.get('payercategory')
        payer = addpayer(self,payername,payercategory)
        self.redirect("/listpayers")
# [END DoAddPayer]

class ViewPayer(webapp2.RequestHandler):
    def get(self,payerid):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                dict_name      = self.request.get('dict_name',USERDICT)
                payer_key = ndb.Key(urlsafe=payerid)
                payer = payer_key.get()
                
                content.append(html("h1","Payer Money Move " + payer.name))
                content.append("<hr>")
                rows = [[datedumponly(utc2local(moneymove.date)),moneymove.value] for moneymove in getmoneymovesforpayer(self,payer.name)]
                content.append(htmltable(htmlrows(rows)))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/","Home")])))
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

