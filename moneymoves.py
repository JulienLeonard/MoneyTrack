from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from moneymovetemplates    import *
from mydicts           import *
from myschemas         import *
from modelutils        import *
from htmlutils         import *
from utils             import *
from timeutils         import *
from admin             import *

def moneymovehandlers():
    # return [('/listmoneymoves',       ListMoneymoves),
    #         ('/mylistmoneymoves/(.*)',MyListMoneymoves),
    #         ('/addmoneymove',         AddMoneymove),
    #         ('/doaddmoneymove',       DoAddMoneymove),
    #         ('/mydoaddmoneymove/(.*)',MyDoAddMoneymove)]
    return [('/listmoneymoves',       ListMoneyMoves),
            ('/addmoneymove/(.*)',    AddMoneyMove),
            ('/doaddmoneymove',       DoAddMoneyMove)]

def addmoneymove(request,account,payee,value,date):
    dict_name = request.request.get('dict_name', USERDICT)
    omoneymove = MoneyMove(parent=dict_key(dict_name))
    omoneymove.account     = account
    omoneymove.payee       = payee
    omoneymove.value       = value
    if not date == None:
        omoneymove.date        = date
    omoneymove.put()
    return omoneymove
                
    
# [START ListMoneymove]
class ListMoneyMoves(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(html("h1","Account Money Moves"))
                content.append("<hr>")
                rows = [[moneymove.account,moneymove.payee,moneymove.value,date2string(utc2local(moneymove.date))] for moneymove in getallmoneymoves(self)]
                content.append(htmltable(htmlrows(rows)))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/addmoneymove/expense","Add Expense"),buttonformget("/addmoneymove/credit","Add Credit"),buttonformget("/","Home")])))
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
class AddMoneyMove(webapp2.RequestHandler):
    def get(self,movetype):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():

                curnames      = [c.name for c in getexpenseaccounts(self)]
                curlist       = ["<option value=\""+ c + "\">" + c + "</option>" for c in curnames]
                htmlaccounts  = "\n".join(curlist)

                if movetype == "expense":
                    paylistf = getallpayees
                    template = ADD_EXPENSE_TEMPLATE
                else:
                    paylistf = getallpayers
                    template = ADD_CREDIT_TEMPLATE

                    
                liqs        = [c.name for c in paylistf(self)]
                liqs        = ["<option value=\""+ c + "\">" + c + "</option>" for c in liqs]
                htmlpayees  = "\n".join(liqs)
                
                content.append(template.replace("%HTMLACCOUNTS%",htmlaccounts).replace("%HTMLPAYEES%",htmlpayees))
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

# [START DoAddMoneymove]
class DoAddMoneyMove(webapp2.RequestHandler):
    def post(self):
        moneymoveaccount      = self.request.get('moneymoveaccount')
        moneymovepayee        = self.request.get('moneymovepayee')
        moneymovevalue        = self.request.get('moneymovevalue')
        moneymove = addmoneymove(self,moneymoveaccount,moneymovepayee,moneymovevalue,None)
        self.redirect("/listmoneymoves")
# [END DoAddChiChar]

