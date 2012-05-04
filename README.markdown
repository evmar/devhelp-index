Some useful API documentation is not available as man pages but in
some other format:

* GTK stack, including related libraries like Cairo, uses gtk-doc;
* the excellent C++ reference available at [cppreference.com][] is HTML.

If they were man pages they'd integrate well into emacs (where `M-x
man` shows the man page of the word under the cursor).  But both are
available [Devhelp][] data files, which are for a Windows
help&ndash;like system.  Devhelp's GUI provides lists of functions,
keywords, etc.

The Python scripts in this repository index the Devhelp data file to
generate a plain text file mapping keywords to docs.  The elisp
code then provides a `M-x devhelp` command which behaves like `man`,
except that it opens the result in a browser.


[cppreference.com]: http://cppreference.com
[gtk-doc]: http://www.gtk.org/gtk-doc/
[Devhelp]: http://en.wikipedia.org/wiki/Devhelp

## Setup

For gtk-doc based packages like Cairo, `apt-get install libcairo2-doc`.
For the C++ reference, install from the [PPA][].

Now run `./devhelp-index.py`.  It will crawl those documentation
directories and create an index in `~/.cache`.

Finally, symlink `devhelp-query.py` into your PATH somewhere.  You can
now call it:

    $ devhelp-query equal_range
    /usr/share/cppreference/doc/en/html/en.cppreference.com/w/cpp/algorithm/equal_rangehtml.html

In Emacs, install `devhelp.el` and call it via `M-x devhelp`.  (If you
install the appropriate Emacs packages, `(setq
browse-url-browser-function 'w3m-browse-url)` will make Emacs use the
w3m browser within an Emacs buffer, bringing back the `man`
experience.)

[PPA]: https://launchpad.net/~p12/+archive/ppa
