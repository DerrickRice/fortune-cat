
%include('htmldocstart')
%include('head', title='All Fortunes')
<body>
%include('topnav', page='all')

<div>
% if error:
ERROR: {{ error }}
% else:
Thank you! Quote added. <a href="/fortune/all">See all quotes.</a>
% end
</div>

</form>
</body>
%include('htmldocend')
