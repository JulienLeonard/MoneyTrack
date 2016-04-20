from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from liquiditytypetemplates    import *
from mydicts           import *
from myschemas         import *
from modelutils        import *
from htmlutils         import *
from utils             import *
from timeutils         import *
from admin             import *

def liquiditytypehandlers():
    # return [('/listliquiditytypes',       ListLiquiditytypes),
    #         ('/mylistliquiditytypes/(.*)',MyListLiquiditytypes),
    #         ('/addliquiditytype',         AddLiquiditytype),
    #         ('/doaddliquiditytype',       DoAddLiquiditytype),
    #         ('/mydoaddliquiditytype/(.*)',MyDoAddLiquiditytype)]
    return [('/listliquiditytypes',       ListLiquidityTypes),
            ('/addliquiditytype',         AddLiquidityType),
            ('/doaddliquiditytype',       DoAddLiquidityType)]

def addliquiditytype(request,name):
    dict_name = request.request.get('dict_name', USERDICT)
    oliquiditytype = LiquidityType(parent=dict_key(dict_name))
    oliquiditytype.name         = name
    oliquiditytype.put()
    return oliquiditytype
                
    
# [START ListLiquiditytype]
class ListLiquidityTypes(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(html("h1","Account Liquidity Types"))
                content.append("<hr>")
                rows = [[liquiditytype.name,buttonformget("/viewliquiditytype/" + liquiditytype.key.urlsafe(),"View")] for liquiditytype in getallliquiditytypes(self)]
                content.append(htmltable(htmlrows(rows)))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/addliquiditytype","Add"),buttonformget("/","Home")])))
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
class AddLiquidityType(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(ADD_LIQUIDITYTYPE_TEMPLATE)
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

# [START DoAddLiquiditytype]
class DoAddLiquidityType(webapp2.RequestHandler):
    def post(self):
        liquiditytypename         = self.request.get('liquiditytypename')
        liquiditytype = addliquiditytype(self,liquiditytypename)
        self.redirect("/listliquiditytypes")
# [END DoAddChiChar]

