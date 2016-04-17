from google.appengine.api import users
from google.appengine.ext import ndb

class Account(ndb.Model):
    """A main model for representing an account."""
    name          = ndb.StringProperty(indexed=True)
    description   = ndb.StringProperty(indexed=False)
    currencyname  = ndb.StringProperty(indexed=True)

class AccountStatus(ndb.Model):
    """A main model for representing an account status."""
    accountname   = ndb.StringProperty(indexed=True)
    value         = ndb.StringProperty(indexed=False)
    date          = ndb.DateTimeProperty(auto_now_add=True)

class Currency(ndb.Model):
    """A main model for representing a currency."""
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
    categoryname  = ndb.StringProperty(indexed=True)
    value         = ndb.StringProperty(indexed=False)
    date          = ndb.DateTimeProperty(auto_now_add=True)

class MoneyMoveCategory(ndb.Model):
    """A main model for representing a money move category."""
    name   = ndb.StringProperty(indexed=True)
    
    
    
    

    

