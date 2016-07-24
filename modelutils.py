from utils     import *
from myschemas import *
from mydicts   import *
from timeutils import *

def getcurrencyfromaccountname(account):
    refcur = {"AUS":"AUD",
              "FR":"EUR",
              "SGP":"SGD"}
    return refcur[account.split(" ")[0].strip()]

def getallaccounts(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return Account.query(ancestor=dict_key(dict_name)).order(-Account.name)

def addaccount(request,name,description,currencyname,accounttype,liquiditytype):
    dict_name = request.request.get('dict_name', USERDICT)
    oaccount = Account(parent=dict_key(dict_name))
    oaccount.name         = name
    oaccount.description  = description
    oaccount.currencyname = currencyname
    oaccount.accounttype  = accounttype
    oaccount.liquiditytype = liquiditytype
    oaccount.put()
    return oaccount

def addinvestsum(request,account,value,date):
    dict_name = request.request.get('dict_name', USERDICT)
    oinvestsum = InvestSum(parent=dict_key(dict_name))
    oinvestsum.account   = account
    oinvestsum.value     = value
    if not date == None:
        oinvestsum.date      = dayload(date)
    oinvestsum.put()
    return oinvestsum

def addaccountstatus(request,account,value,date):
    dict_name = request.request.get('dict_name', USERDICT)
    oaccountstatus = AccountStatus(parent=dict_key(dict_name))
    oaccountstatus.account   = account
    oaccountstatus.value     = value
    if not date == None:
        oaccountstatus.date      = dayload(date)
    oaccountstatus.put()
    return oaccountstatus


def getallactiveaccounts(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return Account.query(ancestor=dict_key(dict_name)).filter(Account.accounttype == "Active").order(-Account.name)


def getexpenseaccounts(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return Account.query(ancestor=dict_key(dict_name)).filter(Account.accounttype == "Active").filter(Account.liquiditytype == "Liquid").order(-Account.name)

def getcreditaccounts(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return Account.query(ancestor=dict_key(dict_name)).filter(Account.accounttype == "Active").filter(Account.liquiditytype == "Liquid").order(-Account.name)

def getallcurrencys(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return Currency.query(ancestor=dict_key(dict_name))

def getallliquiditytypes(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return LiquidityType.query(ancestor=dict_key(dict_name))

def getallaccounttypes(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return AccountType.query(ancestor=dict_key(dict_name))

def addpayee(request,name,category):
    dict_name = request.request.get('dict_name', USERDICT)
    opayee = Payee(parent=dict_key(dict_name))
    opayee.name         = name
    opayee.category     = category
    opayee.put()
    return opayee

def getallpayees(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return Payee.query(ancestor=dict_key(dict_name))

def addpayeecategory(request,name):
    dict_name = request.request.get('dict_name', USERDICT)
    opayeecategory = PayeeCategory(parent=dict_key(dict_name))
    opayeecategory.name         = name
    opayeecategory.put()
    return opayeecategory


def getallpayeecategorys(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return PayeeCategory.query(ancestor=dict_key(dict_name))

def getallpayers(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return Payer.query(ancestor=dict_key(dict_name))

def getallpayercategorys(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return PayerCategory.query(ancestor=dict_key(dict_name))

def addmoneymove(request,account,payee,value,date):
    dict_name = request.request.get('dict_name', USERDICT)
    omoneymove = MoneyMove(parent=dict_key(dict_name))
    omoneymove.account     = account
    omoneymove.payee       = payee
    omoneymove.value       = value
    if not date == None:
        omoneymove.date        = dayload(date)
    omoneymove.put()
    return omoneymove

def getmoneymovesforpayer(request,payername):
    dict_name = request.request.get('dict_name', USERDICT)
    return MoneyMove.query(ancestor=dict_key(dict_name)).filter(MoneyMove.payee == payername).order(-MoneyMove.date)


def getallmoneymoves(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return MoneyMove.query(ancestor=dict_key(dict_name)).order(-MoneyMove.date)

def getallaccountstatuss(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return AccountStatus.query(ancestor=dict_key(dict_name)).order(-AccountStatus.date,-AccountStatus.account)

def getaccountstatussforaccount(request,accountname):
    dict_name = request.request.get('dict_name', USERDICT)
    return AccountStatus.query(ancestor=dict_key(dict_name)).filter(AccountStatus.account == accountname).order(-AccountStatus.date)

def getallinvestsums(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return InvestSum.query(ancestor=dict_key(dict_name)).order(-InvestSum.date)

def getinvestsumsforaccount(request,accountname):
    dict_name = request.request.get('dict_name', USERDICT)
    return InvestSum.query(ancestor=dict_key(dict_name)).filter(InvestSum.account == accountname).order(-InvestSum.date)

def getallcurrencychanges(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return CurrencyChange.query(ancestor=dict_key(dict_name)).order(-CurrencyChange.date)

def getlastcurrencychange(request,currency1,currency2):
    for cchange in getallcurrencychanges(request):
        if cchange.currencyname1 == currency1 and cchange.currencyname2 == currency2:
            return float(cchange.value)
        else:
            if cchange.currencyname1 == currency2 and cchange.currencyname2 == currency1:
                return 1.0/float(cchange.value)

def datastring():
    content = []
    for klass in [Account,Currency,LiquidityType,AccountType,Payee,PayeeCategory,Payer,PayerCategory,MoneyTransfer,AccountStatus,CurrencyChange,MoneyMove,InvestSum]:
        content.append(klass.__name__)
        for instance in klass.query():
            content.append("--- " + instance.string())
    return "<br>".join(content)

def parse_string(request,datastring):
    Klass = None
    for line in datastring.split("\n"):
        logging.info("line to import " + line)
        if len(line.split(" ")) == 1:
            # this is a klass
            Klass = globals()[line.strip()]
        else:
            instancedata = [s.strip() for s in (" ".join(line.split(" ")[1:])).split(",")]
            dict_name    = request.request.get('dict_name', USERDICT)
            instance = Klass(parent=dict_key(dict_name))
            instance.load(instancedata)
            instance.put()

def mypayees(dbpayees):
    result = {}
    for dbpayee in dbpayees:
        mypayee = MyPayee(dbpayee)
        result[mypayee.ID()] = mypayee
    return result
            
def mypayeecategorys(dbpayeecategorys):
    result = {}
    for dbpayeecategory in dbpayeecategorys:
        mypayeecategory = MyPayeeCategory(dbpayeecategory)
        result[mypayeecategory.ID()] = mypayeecategory
    return result
    

def mymoneymoves(dbmoneymoves):
    result = {}
    for dbmoneymove in dbmoneymoves:
        mymoneymove = MyMoneyMove(dbmoneymove)
        result[mymoneymove.ID()] = mymoneymove
    return result

def myaccounts(dbaccounts):
    result = {}
    for dbaccount in dbaccounts:
        myaccount = MyAccount(dbaccount)
        result[myaccount.ID()] = myaccount
    return result

def myaccountstatuss(dbaccountstatuss):
    result = {}
    for dbaccountstatus in dbaccountsstatuss:
        myaccountstatus = MyAccountStatus(dbaccountstatus)
        result[myaccountstatus.ID()] = myaccountstatus
    return result

def parse_expense_string(request,name,datastring):
    
    dict_name    = request.request.get('dict_name', USERDICT)

    payees         = mypayees(getallpayees(request))
    payeecategorys = mypayeecategorys(getallpayeecategorys(request))
    moneymoves     = mymoneymoves(getallmoneymoves(request))
    accounts       = myaccounts(getallaccounts(request))
    
    for line in datastring.split("\n")[2:]:
        logging.info("line to import " + line)
        items = line.split(",")
        if len(items) == 14:
            (Id,Currency,Amount,Category,SubCategory,Date,Expense,Income,Note,Periodic,Project,PayeePayer,uid,Time) = items

            Id       = Id.strip().strip("\"")
            Currency = Currency.strip().strip("\"")
            Amount   = Amount.strip().strip("\"")
            Category = Category.strip().strip("\"")
            SubCategory = SubCategory.strip().strip("\"")
            Date  = Date.strip().strip("\"")
            Expense = Expense.strip().strip("\"")
            
            if len(Expense) > 0:
                expenseaccount = "SGP " + name + " " + Expense
                
                if not expenseaccount in accounts:
                    newaccount = MyAccount(addaccount(request,expenseaccount,expenseaccount,"SGP","Active","Liquid"))
                    accounts[newaccount.ID()] = newaccount

                if not Category in payeecategorys:
                    newcat = MyPayeeCategory(addpayeecategory(request,Category))
                    payeecategorys[newcat.ID()] = newcat
                    
                if not SubCategory in payees:
                    newpayee = MyPayee(addpayee(request,SubCategory,Category))
                    payees[newpayee.ID()] = newpayee
                    
                expenseid = expenseaccount + SubCategory + "-" + Amount + Date

                expenseid1 = "SGP " + "JL" + " " + Expense + SubCategory + "-" + Amount + Date
                expenseid2 = "SGP " + "YX" + " " + Expense + SubCategory + "-" + Amount + Date
                
                if not expenseid1 in moneymoves and not expenseid2 in moneymoves:
                    year  = Date[0:4]
                    month = Date[4:6]
                    day   = Date[6:]
                    ndate = datedumponly(dateloadonlyandroid(day + " " + month + " " + year))
                    
                    addmoneymove(request,expenseaccount,SubCategory,"-" + Amount,ndate)
    
            
def getaccountROI(request,account):
    qresult = getaccountstatussforaccount(request,account.name).fetch(1)
    if not len(qresult) > 0:
        return "NA"
    lastaccountstatus = float(qresult[0].value)
    sum = 0.0
    for isum in getinvestsumsforaccount(request,account.name):
        sum += float(isum.value)
    if sum == 0.0:
        return "NA"
    return float(int(((lastaccountstatus - sum)/sum * 10000.0)))/100.0

def getaccountROIdays(request,account):
    qresult = getaccountstatussforaccount(request,account.name).fetch(1)
    if not len(qresult) > 0:
        return "NA"
    lastaccountstatus = float(qresult[0].value)

    now = utcnow()

    sum = 0.0
    for isum in getinvestsumsforaccount(request,account.name):
        sum += float(isum.value)
    if sum == 0.0:
        return "NA"

    incall = (lastaccountstatus - sum)
    incs = 0.0
    sortlist = []
    for isum in getinvestsumsforaccount(request,account.name):
        deltadays = (now - isum.date).days
        sortlist.append((deltadays,float(isum.value)))
    sortlist = sorted(sortlist)

    longestdays = sortlist[-1][0]
    ssum = 0.0
    for (deltadays,isum) in sortlist:
        ssum += (deltadays/longestdays) * isum

    return float(int((365.0/longestdays) * (incall / ssum) * 10000.0))/100.0

def getlastchanges(request):
    changes         = {}
                
    totalcurrencies = getallcurrencys(request)
    for currency1 in totalcurrencies:
        for currency2 in totalcurrencies:
            if currency1.name == currency2.name:
                changes[(currency1.name,currency2.name)] = 1.0
            else:
                if (currency2.name,currency1.name) in changes:
                    changes[(currency1.name,currency2.name)] = 1/changes[(currency2.name,currency1.name)]
                else:
                    # get last corresponding currencychange available
                    changes[(currency1.name,currency2.name)] = getlastcurrencychange(request,currency1.name,currency2.name)
    return changes
