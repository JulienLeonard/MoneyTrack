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

def getallowners(request):
    dict_name = request.request.get('dict_name', USERDICT)
    return Owner.query(ancestor=dict_key(dict_name))
