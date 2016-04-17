ADD_PAYEE_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <h1>Add Payee</h1>
    <hr>
    <form action="/doaddpayee" method="post">
      <table>
      <tr>
      <td>Name</td>
      <td><div><textarea name="payeename"         rows="1" cols="40"></textarea></div></td>
      </tr>
      <tr>
      <td>Category</td>
      <td><div><select name="payeecategory"         >%HTMLCATEGORIES%</select></div></td>
      </tr>
      </table>
      <hr>
      <div><input type="submit" value="Add"></div>
    </form>
    <hr>
    <table>
    <tr>
    <td>
    <form action="/listpayees" method="get">
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
