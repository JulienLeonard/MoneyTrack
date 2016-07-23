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
            ('/doaddmoneymove',       DoAddMoneyMove),
            ('/deletemoneymove/(.*)',    DeleteMoneyMove),
            ('/editmoneymove/(.*)',    EditMoneyMove),
            ('/doeditmoneymove/(.*)',    DoEditMoneyMove)]
                
    
# [START ListMoneymove]
class ListMoneyMoves(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                content.append(html("h1","Account Money Moves"))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/addmoneymove/expense","Add Expense"),buttonformget("/addmoneymove/credit","Add Credit"),buttonformget("/","Home")])))
                content.append("<hr>")
                rows = [[moneymove.account,moneymove.payee,moneymove.value,date2string(utc2local(moneymove.date)),buttonformget("/editmoneymove/" + moneymove.key.urlsafe(),"Edit"),buttonformget("/deletemoneymove/" + moneymove.key.urlsafe(),"Del")] for moneymove in getallmoneymoves(self)]
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
                
                content.append(template.replace("%HTMLACCOUNTS%",htmlaccounts).replace("%HTMLPAYEES%",htmlpayees).replace("%NOW%",datedumponly(localnow())))
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
        moneymovedate         = self.request.get('moneymovedate')
        moneymove = addmoneymove(self,moneymoveaccount,moneymovepayee,moneymovevalue,moneymovedate)
        self.redirect("/listmoneymoves")
# [END DoAddChiChar]

# [START DeleteMoneyMove]
class DeleteMoneyMove(webapp2.RequestHandler):
    def get(self,isumid):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                dict_name      = self.request.get('dict_name',USERDICT)
                isum_key = ndb.Key(urlsafe=isumid)
                isum = isum_key.get()
                isum.key.delete()
                
        self.redirect("/listmoneymoves")
# [END DoAddChiChar]

# [START EditMoneyMove]
class EditMoneyMove(webapp2.RequestHandler):
    def get(self,isumid):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():

                dict_name      = self.request.get('dict_name',USERDICT)
                isum_key = ndb.Key(urlsafe=isumid)
                moneymove = isum_key.get()

                v = float(moneymove.value)
                
                accountnames = [c.name for c in getexpenseaccounts(self)]
                aselect  = {c: "" for c in accountnames}
                aselect[moneymove.account] = "selected"
                
                acclist       = ["<option value=\""+ c  + "\" " + aselect[c] + ">" + c + "</option>" for c in accountnames]
                htmlaccounts  = "\n".join(acclist)

                payee = moneymove.payee
                allpayees = [c.name for c in getallpayees(self)]
                isexpense = False
                if payee in allpayees:
                    isexpense = True
                
                if isexpense:
                    paylistf = getallpayees
                    template = EDIT_EXPENSE_TEMPLATE
                else:
                    paylistf = getallpayers
                    template = EDIT_CREDIT_TEMPLATE
                    
                liqs        = [c.name for c in paylistf(self)]
                pselect     = {c: "" for c in liqs}
                pselect[moneymove.payee] = "selected"
                liqs        = ["<option value=\""+ c + "\" " + pselect[c] + ">" + c + "</option>" for c in liqs]
                htmlpayees  = "\n".join(liqs)
                
                content.append(template.replace("%MMID%",moneymove.key.urlsafe()).replace("%VALUE%",moneymove.value).replace("%HTMLACCOUNTS%",htmlaccounts).replace("%HTMLPAYEES%",htmlpayees).replace("%NOW%",datedumponly(moneymove.date)))
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
class DoEditMoneyMove(webapp2.RequestHandler):
    def post(self,isumid):
        user = users.get_current_user()
        content = []
        if user:
            if user.email() in myemails():
                dict_name      = self.request.get('dict_name',USERDICT)
                isum_key = ndb.Key(urlsafe=isumid)
                moneymove = isum_key.get()
                moneymove.account      = self.request.get('moneymoveaccount')
                moneymove.payee        = self.request.get('moneymovepayee')
                moneymove.value        = self.request.get('moneymovevalue')
                moneymove.date         = dayload(self.request.get('moneymovedate'))
                moneymove.put()
        self.redirect("/listmoneymoves")
# [END DoAddChiChar]
