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
from accounttypes    import *
from accountstatus   import *
from investsums      import *
from moneymoves      import *
from currencychanges import *
from google.appengine.ext import db
from maintemplates   import *
from chartemplate   import *

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
                content.append(htmltable(htmlrow([buttonformget("/addinvestsum","+InvestSum")])))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/addmoneymove/credit","+Income"),])))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/capital","Capital"),buttonformget("/capitalchart","Capital History")])))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/listmoneymoves","MoneyMoves"),])))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/listaccounts","Accounts"),buttonformget("/listaccountstatuss","AccountStatuses"),buttonformget("/listinvestsums","InvestSums"),buttonformget("/listaccounttypes","AccountTypes")])))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/listpayees","Payees"),buttonformget("/listpayeecategorys","Payee Categories")])))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/listpayers","Payers"),buttonformget("/listpayercategorys","Payer Categories")])))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/listcurrencychanges","Currency Changes"),buttonformget("/listcurrencies","Currencies"),buttonformget("/listliquiditytypes","Liquidity Types")])))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/clear","Clear"),buttonformget("/logs","Logs"),buttonformget("/import","Import"),buttonformget("/export","Export")])))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/importexpense","Import Expenses")])))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/reportexpensemonth","Monthly Expenses"),buttonformget("/reportexpensecategorymonth","Monthly Expenses per Category")])))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/reportincomemonth","Monthly Income"),buttonformget("/reportpassiveincomemonth","Passive Monthly Income")])))
                
                
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

class MyExportHandler(webapp2.RequestHandler):
    def get(self,email):
        if not email in myemails():
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


class ImportExpenseHandler(webapp2.RequestHandler):
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
                self.response.write(IMPORT_EXPENSE_TEMPLATE)
        
# [START DoImport]
class DoImportExpense(webapp2.RequestHandler):
    def post(self):
        datastring         = self.request.get('importexpensecontent')
        name               = self.request.get('importexpensename')
        parse_expense_string(self,name,datastring)
        self.redirect("/")
# [END DoImport]


class ReportExpenseMonthHandler(webapp2.RequestHandler):
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
                content.append(html("h1","Expense Month Report"))

                moneymoves     = mymoneymoves(getallmoneymoves(self))

                months = {}
                for mm in moneymoves.values():
                    puts("mm",mm.maccount)
                    if float(mm.mvalue) < 0.0:
                        smonth = dateloadandroid(mm.mdate).strftime("%Y %m")
                        if not smonth in  months:
                            months[smonth] = 0.0
                        months[smonth] += float(mm.mvalue)

                content.append(htmltable(htmlrows([["Month","Expenses"]] + [[smonth, months[smonth]] for smonth in sorted(months.keys())])))
                content.append("<hr>")

                smonths = ["\"" + smonth + "\"" for smonth in sorted(months.keys())]
                values = [str(-months[smonth]) for smonth in sorted(months.keys())]

                CONTAINER = "expenses"
                TITLE = "Expenses"
                CATEGORIES = ",".join(smonths)
                YAXIS = "SGD"
                NAME = "Expenses"
                DATA = ",".join(values)
                content.append(charttemplate.replace('%CONTAINER%',CONTAINER).replace('%TITLE%',TITLE).replace('%CATEGORIES%',CATEGORIES).replace('%YAXIS%',YAXIS).replace('%NAME%',NAME).replace('%DATA%',DATA))

                content.append("<hr>")

                
                
        content = htmlcenter(content)
        writehtmlresponse(self,content)


class ReportIncomeMonthHandler(webapp2.RequestHandler):
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
                content.append(html("h1","Income Month Report"))

                moneymoves     = mymoneymoves(getallmoneymoves(self))

                months = {}
                for mm in moneymoves.values():
                    puts("mm",mm.maccount)
                    if float(mm.mvalue) > 0.0:
                        smonth = dateloadandroid(mm.mdate).strftime("%Y %m")
                        if not smonth in  months:
                            months[smonth] = 0.0
                        months[smonth] += float(mm.mvalue)

                content.append(htmltable(htmlrows([["Month","Expenses"]] + [[smonth, months[smonth]] for smonth in sorted(months.keys())])))
                content.append("<hr>")

                smonths = ["\"" + smonth + "\"" for smonth in sorted(months.keys())]
                values = [str(months[smonth]) for smonth in sorted(months.keys())]

                CONTAINER = "income"
                TITLE = "Income"
                CATEGORIES = ",".join(smonths)
                YAXIS = "SGD"
                NAME = "Income"
                DATA = ",".join(values)
                content.append(charttemplate.replace('%CONTAINER%',CONTAINER).replace('%TITLE%',TITLE).replace('%CATEGORIES%',CATEGORIES).replace('%YAXIS%',YAXIS).replace('%NAME%',NAME).replace('%DATA%',DATA))

                content.append("<hr>")
                
        content = htmlcenter(content)
        writehtmlresponse(self,content)

class ReportPassiveIncomeMonthHandler(webapp2.RequestHandler):
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
                content.append(html("h1","Passive Income Month Report"))

                moneymoves     = mymoneymoves(getallmoneymoves(self))

                months = {}
                for mm in moneymoves.values():
                    puts("mm",mm.maccount)
                    if float(mm.mvalue) > 0.0 and "nterest" in mm.mpayee:
                        smonth = dateloadandroid(mm.mdate).strftime("%Y %m")
                        if not smonth in  months:
                            months[smonth] = 0.0
                        months[smonth] += float(mm.mvalue)

                content.append(htmltable(htmlrows([["Month","Passive Income"]] + [[smonth, months[smonth]] for smonth in sorted(months.keys())])))
                content.append("<hr>")

                smonths = ["\"" + smonth + "\"" for smonth in sorted(months.keys())]
                values = [str(months[smonth]) for smonth in sorted(months.keys())]

                CONTAINER = "income"
                TITLE = "Income"
                CATEGORIES = ",".join(smonths)
                YAXIS = "SGD"
                NAME = "Income"
                DATA = ",".join(values)
                content.append(charttemplate.replace('%CONTAINER%',CONTAINER).replace('%TITLE%',TITLE).replace('%CATEGORIES%',CATEGORIES).replace('%YAXIS%',YAXIS).replace('%NAME%',NAME).replace('%DATA%',DATA))

                content.append("<hr>")
                
        content = htmlcenter(content)
        writehtmlresponse(self,content)

        
        
class ReportExpenseCategoryMonthHandler(webapp2.RequestHandler):
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
                content.append(html("h1","Expense Month Report"))

                moneymoves     = mymoneymoves(getallmoneymoves(self))
                payees         = mypayees(getallpayees(self))
                
                categorymonths = {}
                categorys = []
                months = []
                for mm in moneymoves.values():
                    puts("mm",mm.maccount)
                    if float(mm.mvalue) < 0.0:
                        smonth   = dateloadandroid(mm.mdate).strftime("%m %Y")
                        category = payees[mm.mpayee].mcategory

                        key = category + "." + smonth
                        if not category in categorys:
                            categorys.append(category)
                        if not smonth in months:
                            months.append(smonth)
                        if not key in  categorymonths:
                            categorymonths[key] = 0.0
                        categorymonths[key] += float(mm.mvalue)


                months = sorted(months)
                firstrow = [""] + months
                rows = [firstrow]
                for category in categorys:
                    data = []
                    for smonth in months:
                        key = category + "." + smonth
                        if not key in categorymonths:
                            value = "0.0"
                        else:
                            value = str(categorymonths[key])
                        data.append(value)
                    rows.append([category] + data)

                # total
                tmonths = {}
                for tmonth in months:
                    tmonths[tmonth] = 0.0
                    for category in categorys:
                        key = category + "." + tmonth
                        if key in categorymonths:
                            tmonths[tmonth] += float(categorymonths[key])
                rows.append(["Total"] + [str(tmonths[tmonth]) for tmonth in months])
                content.append(htmltable(htmlrows(rows)))
                content.append("<hr>")
                
                
        content = htmlcenter(content)
        writehtmlresponse(self,content)

        

class CapitalHandler(webapp2.RequestHandler):
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
                totalcurrencies = {}
                aaccounts = []
                changes = {}
                
                for currency in getallcurrencys(self):
                    totalcurrencies[currency.name] = 0.0

                    for currency1 in totalcurrencies:
                        for currency2 in totalcurrencies:
                            if currency1 == currency2:
                                changes[(currency1,currency2)] = 1.0
                            else:
                                if (currency2,currency1) in changes:
                                    changes[(currency1,currency2)] = 1/changes[(currency2,currency1)]
                                else:
                                    # get last corresponding currencychange available
                                    changes[(currency1,currency2)] = getlastcurrencychange(self,currency1,currency2)
                    
                                
                for account in getallactiveaccounts(self):
                    currency = getcurrencyfromaccountname(account.name)
                    accountstatuss = getaccountstatussforaccount(self,account.name).fetch(1)
                    if accountstatuss and len(accountstatuss) > 0:
                        lastaccountstatus = accountstatuss[0]
                        aaccounts.append([account.name,lastaccountstatus.value,currency,datedumponly(lastaccountstatus.date)])
                        totalcurrencies[currency] += float(lastaccountstatus.value)

                totals = {}
                for currency1 in totalcurrencies:
                    ctotal = 0.0
                    for currency2 in totalcurrencies:
                        ctotal +=  totalcurrencies[currency2] /changes[(currency1,currency2)]
                    totals[currency1] = ctotal
                    
                    
                content.append(html("h1","Current Capital"))
                content.append("<hr>")
                content.append(html("h2","Currency Capitals"))
                content.append(htmltable(htmlrows([[totalcurrencies[currency],currency] for currency in totalcurrencies])))
                content.append("<hr>")
                content.append(html("h2","Total per currency"))
                content.append(htmltable(htmlrows([[totals[currency],currency] for currency in totalcurrencies])))
                content.append("<hr>")
                content.append(html("h2","Active account status"))
                content.append(htmltable(htmlrows(aaccounts)))
                content.append("<hr>")

                
        content = htmlcenter(content)
        writehtmlresponse(self,content)

class MyCapitalHandler(webapp2.RequestHandler):
    def get(self,email):
        content = []
        if not email in myemails():
            content.append(html("h1","Not Authorized"))
        else:
            totalcurrencies = {}
            aaccounts = []
            changes = {}
                
            for currency in getallcurrencys(self):
                totalcurrencies[currency.name] = 0.0

                for currency1 in totalcurrencies:
                    for currency2 in totalcurrencies:
                        if currency1 == currency2:
                            changes[(currency1,currency2)] = 1.0
                        else:
                            if (currency2,currency1) in changes:
                                changes[(currency1,currency2)] = 1/changes[(currency2,currency1)]
                            else:
                                # get last corresponding currencychange available
                                changes[(currency1,currency2)] = getlastcurrencychange(self,currency1,currency2)
                    
                                
            for account in getallactiveaccounts(self):
                currency = getcurrencyfromaccountname(account.name)
                lastaccountstatus = getaccountstatussforaccount(self,account.name).fetch(1)[0]
                aaccounts.append([account.name,lastaccountstatus.value,currency,datedumponly(lastaccountstatus.date)])
                totalcurrencies[currency] += float(lastaccountstatus.value)

            totals = {}
            for currency1 in totalcurrencies:
                ctotal = 0.0
                for currency2 in totalcurrencies:
                    ctotal +=  totalcurrencies[currency2] /changes[(currency1,currency2)]
                totals[currency1] = ctotal
                    
                    
            content.append(html("h1","Current Capital"))
            content.append("<hr>")
            content.append(html("h2","Currency Capitals"))
            content.append(htmltable(htmlrows([[totalcurrencies[currency],currency] for currency in totalcurrencies])))
            content.append("<hr>")
            content.append(html("h2","Total per currency"))
            content.append(htmltable(htmlrows([[totals[currency],currency] for currency in totalcurrencies])))
            content.append("<hr>")
            content.append(html("h2","Active account status"))
            content.append(htmltable(htmlrows(aaccounts)))
            content.append("<hr>")

                
        content = htmlcenter(content)
        writehtmlresponse(self,content)

class CapitalChartHandler(webapp2.RequestHandler):
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
                totalcurrencies = {}
                aaccounts       = []
                changes         = getlastchanges(self)
                
                for currency in getallcurrencys(self):
                    totalcurrencies[currency.name] = 0.0

                smonths = {}
                accounts = {}    
                    
                for account in getallaccounts(self):
                    ccurrency       = getcurrencyfromaccountname(account.name)
                    accountstatuss  = getaccountstatussforaccount(self,account.name)
                    accounts[account.name] = account
                    
                    for accountstatus in accountstatuss:
                        smonth  = accountstatus.date.strftime("%Y%m")
                        if not smonth in smonths:
                            smonths[smonth] = {}
                        if not account.name in smonths[smonth]:
                            smonths[smonth][account.name] = []
                        smonths[smonth][account.name].append((accountstatus.date.strftime("%Y%m%d"),float(accountstatus.value) * changes[ccurrency,"SGD"]))

                lastaccountvalues = {}
                for smonth in sorted(smonths.keys()):
                    for account in smonths[smonth]:
                        # smonths[smonth][account] = float(sum(smonths[smonth][account]))/float(len(smonths[smonth][account]))
                        smonths[smonth][account] = sorted(smonths[smonth][account])[-1][-1]
                        lastaccountvalues[account] = smonths[smonth][account]
                    for account in lastaccountvalues:
                        if not account in smonths[smonth]:
                            if accounts[account].accounttype == "Closed":
                                smonths[smonth][account] = 0.0
                            else:
                                smonths[smonth][account] = lastaccountvalues[account]

                values = {}
                for smonth in sorted(smonths.keys()):
                    values[smonth] = sum([smonths[smonth][account] for account in smonths[smonth]])
                    
                content.append(html("h1","Capital History"))
                content.append("<hr>")

                ssmonths = ["\"" + smonth + "\"" for smonth in sorted(smonths.keys())]
                values = [str(values[smonth]) for smonth in sorted(smonths.keys())]

                CONTAINER = "capital"
                TITLE = "Capital Histoy"
                CATEGORIES = ",".join(ssmonths)
                YAXIS = "SGD"
                NAME = "Capital"
                DATA = ",".join(values)
                content.append(charttemplate.replace('%CONTAINER%',CONTAINER).replace('%TITLE%',TITLE).replace('%CATEGORIES%',CATEGORIES).replace('%YAXIS%',YAXIS).replace('%NAME%',NAME).replace('%DATA%',DATA))

                content.append("<hr>")
                
        content = htmlcenter(content)
        writehtmlresponse(self,content)



        
app = webapp2.WSGIApplication([('/', MainHandler),('/capitalchart', CapitalChartHandler),('/clear', ClearHandler),('/export', ExportHandler),('/myexport/(.*)', MyExportHandler),('/capital', CapitalHandler),('/mycapital/(.*)', MyCapitalHandler),('/reportexpensemonth', ReportExpenseMonthHandler),('/reportincomemonth', ReportIncomeMonthHandler),('/reportpassiveincomemonth', ReportPassiveIncomeMonthHandler),('/reportexpensecategorymonth', ReportExpenseCategoryMonthHandler),('/import', ImportHandler),('/doimport', DoImport),('/importexpense', ImportExpenseHandler),('/doimportexpense', DoImportExpense)] + currencyhandlers() + accounthandlers() + liquiditytypehandlers() + accounttypehandlers() + payeehandlers() + payeecategoryhandlers() + payerhandlers() + payercategoryhandlers() + accountstatushandlers() + moneymovehandlers() + investsumhandlers() + currencychangehandlers(),  debug=True)
