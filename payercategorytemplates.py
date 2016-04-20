ADD_PAYERCATEGORY_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <h1>Add Payer Category</h1>
    <hr>
    <form action="/doaddpayercategory" method="post">
      <table>
      <tr>
      <td>Name</td>
      <td><div><textarea name="payercategoryname"         rows="1" cols="40"></textarea></div></td>
      </tr>
      <tr>
      </table>
      <hr>
      <div><input type="submit" value="Add"></div>
    </form>
    <hr>
    <table>
    <tr>
    <td>
    <form action="/listpayercategorys" method="get">
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
