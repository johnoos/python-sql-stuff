# invoke with python3 -m pytest -s py_MyHTMLParser.py

import io
import py_MyHTMLParser  # Replace with the actual name of your python file

def test_MyHTMLParser_output(monkeypatch, capsys):
    # 1. Define the simulated STDIN data from your second image (test case 4/6)
    simulated_input = (
        '52\n'
        '<article class="hentry">\n'
        '<!-- <header>\n'
        '<h1 class="entry-title">But Will It Make You Happy?</h1>\n'
        '<time class="updated" datetime="2010-08-07 11:11:03-0400">08-07-2010</time>\n'
        '<p class="byline author vcard">\n'
        'By <span class="fn">Stephanie Rosenbloom</span>\n'
        '</p>\n'
        '</header> -->\n'
        '\n'
        '<div class="entry-content">\n'
        '<p>...article text...</p>\n'
        '<p>...article text...</p>\n'
        '\n'
        '<figure>\n'
        '<img src="tammy-strobel.jpg" alt="Portrait of Tammy Strobel" />\n'
        '<figcaption>Tammy Strobel in her pared-down, 400sq-ft apt.</figcaption>\n'
        '</figure>\n'
        '\n'
        '<p>...article text...</p>\n'
        '<p>...article text...</p>\n'
        '\n'    
        '<aside>\n'
        '<h2>Share this Article</h2>\n'
        '<ul>\n'
        '  <li>Facebook</li>\n'
        '  <li>Twitter</li>\n'
        '  <li>Etc</li>\n'
        '</ul>\n'
        '</aside>\n'
        '\n'
        '<div class="entry-content-asset">\n'
        '<a href="photo-full.png">\n'
        '  <img src="photo.png" alt="The objects Tammy removed from her life after moving" />\n'
        '</a>\n'
        '</div>\n'
        '\n'
        '<p>...article text...</p>\n'
        '<p>...article text...</p>\n'
        '\n'
        '<a class="entry-unrelated" href="http://fake.site/">Find Great Vacations</a>\n'
        '</div>\n'
        '\n'
        '<footer>\n'
        '<p>\n'
        'A version of this article appeared in print on August 8,\n'
        '2010, on page BU1 of the New York edition.\n'
        '</p>\n'
        '<div class="source-org vcard copyright">\n'
        'Copyright 2010 <span class="org fn">The New York Times Company</span>\n'
        '</div>\n'
        '</footer>\n'
        '</article>\n'
    )

    # 2. Mock STDIN using monkeypatch and StringIO
    monkeypatch.setattr("sys.stdin", io.StringIO(simulated_input))

    # 3. Execute the main function from your script
    py_MyHTMLParser.main()