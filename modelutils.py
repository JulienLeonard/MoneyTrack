from utils     import *
from myschemas import *
from mydicts   import *
from timeutils import *

def getallaccounts(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return Account.query(ancestor=dict_key(dict_name))

def getallcurrencys(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return Currency.query(ancestor=dict_key(dict_name))

def getallliquiditytypes(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return LiquidityType.query(ancestor=dict_key(dict_name))

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
    return MoneyMove.query(ancestor=dict_key(dict_name))

def getallaccountstatuss(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return AccountStatus.query(ancestor=dict_key(dict_name))

def datastring():
    content = []
    for klass in [Account,AccountStatus,Currency,LiquidityType,CurrencyChange,MoneyMove,Payee,PayeeCategory,Payer,PayerCategory,MoneyTransfer]:
        content.append(klass.__name__)
        for instance in klass.query():
            content.append("--- " + instance.string())
    return "<br>".join(content)

def parse_string(request,datastring):
    Klass = None
    for line in datastring.split("\n"):
        if len(line.split(" ")) == 1:
            # this is a klass
            Klass = globals()[line.strip()]
        else:
            instancedata = [s.strip() for s in (" ".join(line.split(" ")[1:])).split(",")]
            dict_name    = request.request.get('dict_name', USERDICT)
            instance = Klass(parent=dict_key(dict_name))
            instance.load(instancedata)
            instance.put()

            

            




            


