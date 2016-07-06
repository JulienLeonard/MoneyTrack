ADD_CURRENCY_CHANGE_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <h1>Add Currency Change</h1>
    <hr>
    <form action="/doaddcurrencychange" method="post">
      <table>
         <tr>
            <td>Currency1</td>
            <td><div><select name="currencychangecurrencyname1"     >%HTMLCURRENCY1%</select></div></td>
         </tr>
         <tr>
            <td>Currency2</td>
            <td><div><select name="currencychangecurrencyname2"     >%HTMLCURRENCY2%</select></div></td>
         </tr>
         <tr>
            <td>Value</td>
            <td><div><textarea name="currencychangevalue"  rows="1" cols="40"></textarea></div></td>
         </tr>
      </table>
      <div><input type="submit" value="Add"></div>
    </form>
    <hr>
    <table>
    <tr>
    <td>
    <form action="/listcurrencychanges" method="get">
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
