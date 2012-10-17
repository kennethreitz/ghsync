ghsync: GitHub Repo Syncer
==========================

This script uses the GitHub API to get a list of all forked, mirrored,
public, and private repos in your GitHub account. If the repo already
exists locally, it will update it via git-pull. Otherwise, it will
properly clone the repo.

It will organize your repos into the following directory structure: ::

    + repos
    \ +-- forks    (public fork repos)
      +-- mirrors  (public mirror repos)
      +-- private  (private repos)
      +-- public   (public repos)
      +-- watched  (public watched repos)


Requires Ian Cordasco's github3.py (http://pypi.python.org/pypi/github3.py).

Inspired by Gisty (http://github.com/swdyh/gisty).


Install
-------

To install ghsync, simply run: ::

    $ pip install ghsync

The command ``ghsync`` will then be available to you from the command
line. Beware, unless you set the ``GHSYNC_DIR`` environment variable, it
will add all the repos to your current directory.::

    $ export GHSYNC_DIR='~/repos/'

Options
-------

If the ``--upsteam`` argument is passed, all forked repos will have an
**upstream** remote added, pointing to their parent repo on GitHub.

You can also selectively sync certian types of repos with ``--only``. If
you'd like to only sync forked repositories, for example::

    $ ghsync --only forks


Contribute
----------

If you'd like to contribute, simply fork `the repository`_, commit your
changes to the **develop** branch (or branch off of it), and send a pull
request.


.. _`the repository`: http://github.com/kennethreitz/ghsync
