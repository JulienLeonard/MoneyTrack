ADD_EXPENSE_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <h1>Add Expense</h1>
    <hr>
    <form action="/doaddmoneymove" method="post">
      <table>
         <tr>
            <td>Account</td>
            <td><div><select name="moneymoveaccount"     >%HTMLACCOUNTS%</select></div></td>
         </tr>
         <tr>
            <td>Payee</td>
            <td><div><select name="moneymovepayee"     >%HTMLPAYEES%</select></div></td>
         </tr>
         <tr>
            <td>Value</td>
            <td><div><textarea name="moneymovevalue"  rows="1" cols="40"></textarea></div></td>
         </tr>
      </table>
      <div><input type="submit" value="Add"></div>
    </form>
    <hr>
    <table>
    <tr>
    <td>
    <form action="/listmoneymoves" method="get">
      <div><input type="submit" value="List"></div>
    </form>
    </td>
    <td>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
    </td>
    <tr>
    </table>
"""

ADD_CREDIT_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <h1>Add Credit</h1>
    <hr>
    <form action="/doaddmoneymove" method="post">
      <table>
         <tr>
            <td>Account</td>
            <td><div><select name="moneymoveaccount"     >%HTMLACCOUNTS%</select></div></td>
         </tr>
         <tr>
            <td>Payer</td>
            <td><div><select name="moneymovepayee"     >%HTMLPAYEES%</select></div></td>
         </tr>
         <tr>
            <td>Value</td>
            <td><div><textarea name="moneymovevalue"  rows="1" cols="40"></textarea></div></td>
         </tr>
      </table>
      <div><input type="submit" value="Add"></div>
    </form>
    <hr>
    <table>
    <tr>
    <td>
    <form action="/listmoneymoves" method="get">
      <div><input type="submit" value="List"></div>
    </form>
    </td>
    <td>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
    </td>
    <tr>
    </table>
"""
