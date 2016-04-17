from google.appengine.api import users
from google.appengine.ext import ndb

class Account(ndb.Model):
    """A main model for representing an account."""
    name          = ndb.StringProperty(indexed=True)
    description   = ndb.StringProperty(indexed=False)
    currencyname  = ndb.StringProperty(indexed=True)
    ownername     = ndb.StringProperty(indexed=True)
    liquiditytype = ndb.StringProperty(indexed=True)

class AccountStatus(ndb.Model):
    """A main model for representing an account status."""
    accountname   = ndb.StringProperty(indexed=True)
    value         = ndb.StringProperty(indexed=False)
    date          = ndb.DateTimeProperty(auto_now_add=True)

class Currency(ndb.Model):
    """A main model for representing a currency."""
    name   = ndb.StringProperty(indexed=True)

class Owner(ndb.Model):
    """A main model for representing a owner."""
    name   = ndb.StringProperty(indexed=True)

class LiquidityType(ndb.Model):
    """A main model for representing a liquidity."""
    name   = ndb.StringProperty(indexed=True)
    
class CurrencyChange(ndb.Model):
    """A main model for representing a currency change."""
    currencyname1   = ndb.StringProperty(indexed=True)
    currencyname2   = ndb.StringProperty(indexed=True)
    value           = ndb.StringProperty(indexed=False)
    date            = ndb.DateTimeProperty(auto_now_add=True)

class MoneyMove(ndb.Model):
    """A main model for representing an account update."""
    accountname   = ndb.StringProperty(indexed=True)
    payee         = ndb.StringProperty(indexed=True)
    value         = ndb.StringProperty(indexed=False)
    date          = ndb.DateTimeProperty(auto_now_add=True)

class Payee(ndb.Model):
    """A main model for representing a payee."""
    name       = ndb.StringProperty(indexed=True)
    category   = ndb.StringProperty(indexed=True)
    
class MoneyTransfer(ndb.Model):
    """A main model for representing a transfer money."""
    accountname1  = ndb.StringProperty(indexed=True)
    accountname2  = ndb.StringProperty(indexed=True)
    value         = ndb.StringProperty(indexed=False)
    date          = ndb.DateTimeProperty(auto_now_add=True)
    
class PayeeCategory(ndb.Model):
    """A main model for representing a money move category, for example Health or Shelter."""
    name   = ndb.StringProperty(indexed=True)
    
    
    
    

    

