IMPORT_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <h1>IMPORT</h1>
    <hr>
    <form action="/doimport" method="post">
      <table>
         <tr>
            <td>Data</td>
            <td><div><textarea name="importcontent"  rows="10" cols="40"></textarea></div></td>
         </tr>
      </table>
      <div><input type="submit" value="Add"></div>
    </form>
    <hr>
    <table>
    <tr>
    <td>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
    </td>
    <tr>
    </table>
"""

IMPORT_EXPENSE_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <h1>IMPORT EXPENSE</h1>
    <hr>
    <form action="/doimportexpense" method="post">
      <table>
         <tr>
            <td>Name</td>
            <td><div><textarea name="importexpensename"  rows="1" cols="40">JL or YX</textarea></div></td>
         </tr>
         <tr>
            <td>Data</td>
            <td><div><textarea name="importexpensecontent"  rows="10" cols="40"></textarea></div></td>
         </tr>
      </table>
      <div><input type="submit" value="Add"></div>
    </form>
    <hr>
    <table>
    <tr>
    <td>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
    </td>
    <tr>
    </table>
"""
