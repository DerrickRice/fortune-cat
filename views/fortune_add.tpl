%include('htmldocstart')
%include('head', title='All Fortunes')
<body>
%include('topnav', page='all')

<form action="/fortune/submit" method="post">
    <div>
        <label for="name">Fortune/Quote:</label>
        <textarea name="content"></textarea>
    </div>
    <div>
        <label for="mail">Author/Source:</label>
        <input type="text" name="author" />
    </div>
    <div>
        <label for="msg">Your unix name:</label>
        <input type="text" name="submitter" />
    </div>

    <div class="button">
        <button type="submit">Submit</button>
    </div>
</form>
</body>
%include('htmldocend')
