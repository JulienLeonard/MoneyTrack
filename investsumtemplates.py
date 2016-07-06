ADD_INVESTSUM_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <h1>Add Invest Sum</h1>
    <hr>
    <form action="/doaddinvestsum" method="post">
      <table>
         <tr>
            <td>Account</td>
            <td><div><select name="investsumaccount"     >%HTMLACCOUNTS%</select></div></td>
         </tr>
         <tr>
            <td>Value</td>
            <td><div><textarea name="investsumvalue"  rows="1" cols="40"></textarea></div></td>
         </tr>
      </table>
      <hr>
      <div><input type="submit" value="Add"></div>
    </form>
    <hr>
    <table>
    <tr>
    <td>
    <form action="/listinvestsums" method="get">
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
