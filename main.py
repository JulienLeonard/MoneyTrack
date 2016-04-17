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
from utils         import *
from htmlutils     import *
from modelutils    import *
from timeutils     import *
from admin         import *
from accounts      import *
from currencies    import *
from owners          import *
from payees          import *
from payeecategories import *

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
                content.append(htmltable(htmlrow([buttonformget("/addexpense","New Expense")])))
                content.append("<hr>")
                content.append(htmltable(htmlrow([buttonformget("/listpayeecategorys","Payee Categories"),buttonformget("/listpayees","Payees"),buttonformget("/listowners","Owners"),buttonformget("/listcurrencies","Currencies"),buttonformget("/listaccounts","Accounts"),buttonformget("/logs","Logs"),buttonformget("/export","Exports")])))
                
            content.append("<hr>")
            url_linktext = 'Logout'
            content.append(htmllink(url,url_linktext))
        
        content = htmlcenter(content)
        writehtmlresponse(self,content)

        
app = webapp2.WSGIApplication([('/', MainHandler)] + currencyhandlers() + accounthandlers() + ownerhandlers() + payeehandlers() + payeecategoryhandlers(), debug=True)
