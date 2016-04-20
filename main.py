#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from utils           import *
from htmlutils       import *
from modelutils      import *
from timeutils       import *
from admin           import *
from accounts        import *
from currencies      import *
from payees          import *
from payercategories import *
from payers          import *
from payeecategories import *
from liquiditytypes  import *
from accountstatus   import *
from moneymoves      import *
from google.appengine.ext import db
from maintemplates   import *

class MainHandler(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()

        content = []
        url = users.create_login_url(self.request.uri)
        if not user:
            url_linktext = 'Login'
            content.append(htmllink(url,url_linktext))
        else:
            if not user.email() in myemails():
                content.append(html("h1","Not Authorized"))
            else:
                content.append(html("h1","Money Track"))
                content.append("Now is " + date2string(localnow()))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/addmoneymove/expense","-Expense")])))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/addaccountstatus","+Account Status")])))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/addmoneymove/credit","+Credit"),])))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/listaccounts","Accounts")])))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/listpayees","Payees"),buttonformget("/listpayeecategorys","Payee Categories")])))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/listpayers","Payers"),buttonformget("/listpayercategorys","Payer Categories")])))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/listcurrencies","Currencies"),buttonformget("/listliquiditytypes","Liquidity Types")])))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/clear","Clear"),buttonformget("/logs","Logs"),buttonformget("/import","Import"),buttonformget("/export","Export")])))
                
            content.append("<hr>")
            url_linktext = 'Logout'
            content.append(htmllink(url,url_linktext))
        
        content = htmlcenter(content)
        writehtmlresponse(self,content)

class ClearHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        content = []
        url = users.create_login_url(self.request.uri)
        if not user:
            url_linktext = 'Login'
            content.append(htmllink(url,url_linktext))
        else:
            if not user.email() in myemails():
                content.append(html("h1","Not Authorized"))
            else:
                for klass in [Account,AccountStatus,Currency,LiquidityType,CurrencyChange,MoneyMove,Payee,PayeeCategory,Payer,PayerCategory,MoneyTransfer]:
                    for instance in klass.query():
                        instance.key.delete()
                self.redirect("/")

class ExportHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        url = users.create_login_url(self.request.uri)
        if not user:
            url_linktext = 'Login'
            content.append(htmllink(url,url_linktext))
        else:
            if not user.email() in myemails():
                content.append(html("h1","Not Authorized"))
            else:
                self.response.write(datastring())

class ImportHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        content = []
        url = users.create_login_url(self.request.uri)
        if not user:
            url_linktext = 'Login'
            content.append(htmllink(url,url_linktext))
        else:
            if not user.email() in myemails():
                content.append(html("h1","Not Authorized"))
            else:
                self.response.write(IMPORT_TEMPLATE)
        

# [START DoImport]
class DoImport(webapp2.RequestHandler):
    def post(self):
        datastring         = self.request.get('importcontent')
        parse_string(self,datastring)
        self.redirect("/")
# [END DoImport]


        
        
app = webapp2.WSGIApplication([('/', MainHandler),('/clear', ClearHandler),('/export', ExportHandler),('/import', ImportHandler),('/doimport', DoImport)] + currencyhandlers() + accounthandlers() + liquiditytypehandlers() + payeehandlers() + payeecategoryhandlers() + payerhandlers() + payercategoryhandlers() + accountstatushandlers() + moneymovehandlers(), debug=True)
