ADD_ACCOUNT_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <h1>Add Account</h1>
    <hr>
    <form action="/doaddaccount" method="post">
      <table>
         <tr>
            <td>Name</td>
            <td><div><textarea name="accountname"         rows="1" cols="40"></textarea></div></td>
         </tr>
         <tr>
            <td>Description</td>
            <td><div><textarea name="accountdescription"  rows="1" cols="40"></textarea></div></td>
         </tr>
         <tr>
            <td>Currency</td>
            <td><div><select name="accountcurrency"     >%HTMLCUR%</select></div></td>
         </tr>
      </table>
      <hr>
      <div><input type="submit" value="Add"></div>
    </form>
    <hr>
    <form action="/listaccounts" method="get">
      <div><input type="submit" value="List"></div>
    </form>
"""
