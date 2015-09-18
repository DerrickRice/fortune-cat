%include('htmldocstart')
%include('head', title='All Fortunes')
<body>
%include('topnav', page='all')
<table>
<tr>
  <th>ID</th>
  <th>Fortune/Quote</th>
  <th>Autror</th>
  <th>Submitted By</th>
  <th>Submit TS</th>
  <th>Tags</th>
</tr>
% for x in fortunes:
<tr>
  <td>{{x.id}}</td>
  <td><pre>{{x.quote}}</pre></td>
  <td>{{x.author}}</td>
  <td>{{x.submitter}}</td>
  <td>{{x.created}}</td>
  <td>{{x.tags}}</td>
</tr>
% end
</table>
</body>
%include('htmldocend')
