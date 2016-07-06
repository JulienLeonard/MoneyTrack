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

def getallpayees(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return Payee.query(ancestor=dict_key(dict_name))

def getallpayeecategorys(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return PayeeCategory.query(ancestor=dict_key(dict_name))

def getallpayers(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return Payer.query(ancestor=dict_key(dict_name))

def getallpayercategorys(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return PayerCategory.query(ancestor=dict_key(dict_name))

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
    return InvestSum.query(ancestor=dict_key(dict_name)).order(-InvestSum.date,-InvestSum.account)

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
    for klass in [Account,Currency,LiquidityType,AccountType,Payee,PayeeCategory,Payer,PayerCategory,MoneyTransfer,AccountStatus,CurrencyChange,MoneyMove]:
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

