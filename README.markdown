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

(If you install the appropriate Emacs packages, `(setq
browse-url-browser-function 'w3m-browse-url)` will make Emacs use the
w3m browser within an Emacs buffer, bringing back the `man`
experience.)

[cppreference.com]: http://cppreference.com
[gtk-doc]: http://www.gtk.org/gtk-doc/
[Devhelp]: http://en.wikipedia.org/wiki/Devhelp
