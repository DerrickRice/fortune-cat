%include('htmldocstart')
%include('head', title='All Fortunes')
<body>
%include('topnav', page='all')
<table>
<tr>
  <th>Fortune/Quote</th>
  <th>Autror</th>
  <th>Submitted By</th>
  <th>Submit TS</th>
</tr>
% for x in fortunes:
<tr>
  <td>{{x.quote}}</td>
  <td>{{x.author}}</td>
  <td>{{x.submitter}}</td>
  <td>{{x.created}}</td>
</tr>
% end
</table>
</body>
%include('htmldocend')
