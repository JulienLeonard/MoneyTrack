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
         <tr>
            <td>Account Type</td>
            <td><div><select name="accounttype"     >%HTMLACCOUNTTYPE%</select></div></td>
         </tr>
         <tr>
            <td>Liquidity Type</td>
            <td><div><select name="accountliquiditytype"     >%HTMLLIQUIDITYTYPE%</select></div></td>
         </tr>
      </table>
      <div><input type="submit" value="Add"></div>
    </form>
    <hr>
    <table>
    <tr>
    <td>
    <form action="/listaccounts" method="get">
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
