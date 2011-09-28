Most of the GTK stack (and related libraries, like Cairo) use
[gtk-doc][] for their documentation.  Unfortunately, gtk-doc generates
HTML, not manpages (it's arguable the format is wrong), which means it
doesn't integrate well into emacs (where `M-x man` shows the man page
of the word under the cursor).

gtk-doc can also generate [Devhelp][] data files, which are for a
Windows help&ndash;like system.  Devhelp's GUI provides lists of
functions, keywords, etc.

The Python scripts in this repository index the Devhelp data file to
generate a plain text file mapping keywords to docs.  The elisp
code then provides a `M-x devhelp` command which behaves like `man`,
except that it opens the result in a browser.

(If you install the appropriate Emacs packages, `(setq
browse-url-browser-function 'w3m-browse-url)` will make Emacs use the
w3m browser within an Emacs buffer, bringing back the `man`
experience.)

[gtk-doc]: http://www.gtk.org/gtk-doc/
[Devhelp]: http://en.wikipedia.org/wiki/Devhelp
