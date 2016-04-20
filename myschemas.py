from google.appengine.api import users
from google.appengine.ext import ndb
from timeutils import *
import datetime, time
import logging

class Account(ndb.Model):
    """A main model for representing an account."""
    name          = ndb.StringProperty(indexed=True)
    description   = ndb.StringProperty(indexed=False)
    currencyname  = ndb.StringProperty(indexed=True)
    liquiditytype = ndb.StringProperty(indexed=True)
    def string(self):
        return ",".join([self.name,self.description,self.currencyname,self.liquiditytype])
    def load(self,params):
        self.name          = params[0]
        self.description   = params[1]
        self.currencyname  = params[2]
        self.liquiditytype = params[3]
        
class AccountStatus(ndb.Model):
    """A main model for representing an account status."""
    account   = ndb.StringProperty(indexed=True)
    value         = ndb.StringProperty(indexed=False)
    date          = ndb.DateTimeProperty(auto_now_add=True)
    def string(self):
        return ",".join([self.account,self.value,datedump(self.date)])
    def load(self,params):
        logging.info("AccountStatus params" + str(params))
        self.account = params[0]
        self.value   = params[1]
        self.date    = dateload(params[2])
    
class Currency(ndb.Model):
    """A main model for representing a currency."""
    name   = ndb.StringProperty(indexed=True)
    def string(self):
        return ",".join([self.name])
    def load(self,params):
        self.name = params[0]

class LiquidityType(ndb.Model):
    """A main model for representing a liquidity."""
    name   = ndb.StringProperty(indexed=True)
    def string(self):
        return ",".join([self.name])
    def load(self,params):
        self.name = params[0]
    
class CurrencyChange(ndb.Model):
    """A main model for representing a currency change."""
    currencyname1   = ndb.StringProperty(indexed=True)
    currencyname2   = ndb.StringProperty(indexed=True)
    value           = ndb.StringProperty(indexed=False)
    date            = ndb.DateTimeProperty(auto_now_add=True)
    def string(self):
        return ",".join([self.currencyname1,self.currencyname2,self.value,datedump(self.date)])
    def load(self,params):
        self.currencyname1 = params[0]
        self.currencyname2 = params[1]
        self.value = params[2]
        self.date = dateload(params[3])

class MoneyMove(ndb.Model):
    """A main model for representing an account update."""
    account       = ndb.StringProperty(indexed=True)
    payee         = ndb.StringProperty(indexed=True)
    value         = ndb.StringProperty(indexed=False)
    date          = ndb.DateTimeProperty(auto_now_add=True)
    def string(self):
        return ",".join([self.account,self.payee,self.value,datedump(self.date)])
    def load(self,params):
        self.account = params[0]
        self.payee = params[1]
        self.value = params[2]
        self.date = dateload(params[3])
    

class PayeeCategory(ndb.Model):
    """A main model for representing a payee category"""
    name   = ndb.StringProperty(indexed=True)
    def string(self):
        return ",".join([self.name])
    def load(self,params):
        self.name = params[0]

class Payee(ndb.Model):
    """A main model for representing a payee."""
    name       = ndb.StringProperty(indexed=True)
    category   = ndb.StringProperty(indexed=True)
    def string(self):
        return ",".join([self.name,self.category])
    def load(self,params):
        self.name = params[0]
        self.category = params[1]

class PayerCategory(ndb.Model):
    """A main model for representing a payer category."""
    name   = ndb.StringProperty(indexed=True)
    def string(self):
        return ",".join([self.name])
    def load(self,params):
        self.name = params[0]

class Payer(ndb.Model):
    """A main model for representing a payer."""
    name       = ndb.StringProperty(indexed=True)
    category   = ndb.StringProperty(indexed=True)
    def string(self):
        return ",".join([self.name,self.category])
    def load(self,params):
        self.name = params[0]
        self.category = params[1]

    
class MoneyTransfer(ndb.Model):
    """A main model for representing a transfer money."""
    accountname1  = ndb.StringProperty(indexed=True)
    accountname2  = ndb.StringProperty(indexed=True)
    value         = ndb.StringProperty(indexed=False)
    date          = ndb.DateTimeProperty(auto_now_add=True)
    def string(self):
        return ",".join([self.accountname1,self.accountname2,self.value,datedump(self.date)])
    def load(self,params):
        self.accountname1 = params[0]
        self.accountname2 = params[0]
        self.value    = params[2]
        self.date     = dateload(params[3])
    
