%include('htmldocstart')
%include('head', title='All Fortunes')
<body>
%include('topnav', page='all')

<form action="/fortune/submit" method="post">
<table>
  <tr>
    <td>Fortune/Quote:<br/>Note: 32 char width tape!</td>
    <td>
      <textarea name="content" style="font-family:monospace; width:32ex;" rows="30"
      placeholder="Never approach a bull from the front, a horse from the rear or a fool from any direction."></textarea>
    </td>
  </tr>
  <tr>
    <td>Author/Source<br/>i.e. the "speaker" of the quote.</td>
    <td>
      <input type="text" name="author" style="font-family:monospace; width:32ex;" placeholder="Confucius"/>
    </td>
  </tr>
  <tr>
    <td>tags<br/>for searching!</td>
    <td>
      <input type="text" name="tags" style="font-family:monospace; width:32ex;" placeholder="#confucius #lol" />
    </td>
  </tr>
  <tr>
    <td>Your unix name<br/>(so we know who contributed the quote)</td>
    <td>
      <input type="text" name="submitter" style="font-family:monospace; width:32ex;" placeholder="unixname" />
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      <button type="submit">Submit</button>
    </td>
  </tr>
</form>
</body>
%include('htmldocend')
