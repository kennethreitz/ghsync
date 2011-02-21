#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Kenneth Reitz's GitHub Syncer

This script uses the GitHub API to get a list of all forked, mirrored, public, and 
private repos in your GitHub account. If the repo already exists locally, it will 
update it via git-pull. Otherwise, it will properly clone the repo.

It will organize your repos into the following directory structure:

+ repos
  ├── forks    (public fork repos)
  ├── mirrors  (public mirror repos)
  ├── private  (private repos)
  ├── public   (public repos)
  └── watched  (public watched repos)

Requires Ask Solem's github2 (http://pypi.python.org/pypi/github2).

Inspired by Gisty (http://github.com/swdyh/gisty). 
"""

import os
import sys
from commands import getoutput as cmd

from github2.client import Github


__author__ = 'Kenneth Reitz'
__license__ = 'ISC'
__copyright__ = '2011 Kenneth REitz'
__version__ = '0.2.2'

# GitHub configurations
GITHUB_USER = cmd('git config github.user')
GITHUB_TOKEN = cmd('git config github.token')

GHSYNC_DIR = os.environ.get('GHSYNC_DIR', '.')



def run():

    os.chdir(GHSYNC_DIR)

    # API Object
    github = Github(username=GITHUB_USER, api_token=GITHUB_TOKEN)


    # repo slots
    repos = {}

    repos['watched'] = [r for r in github.repos.watching(GITHUB_USER)]
    repos['private'] = []
    repos['mirrors'] = []
    repos['public'] = []
    repos['forks'] = []

    # Collect GitHub repos via API
    for repo in github.repos.list():

        if repo.private:
            repos['private'].append(repo)
        elif repo.fork:
            repos['forks'].append(repo)
        elif 'mirror' in repo.description.lower():
            # mirrors owned by self if mirror in description...
            repos['mirrors'].append(repo)
        else:
            repos['public'].append(repo)


    for org, repos in repos.iteritems():
        for repo in repos:
        
            # create org directory (safely)
            try:
                os.makedirs(org)
            except OSError:
                pass
        
            # enter org dir
            os.chdir(org)
        
            # I own the repo
            private = True if org in ('private', 'fork', 'mirror', 'public') else False

            # just `git pull` if it's already there
            if os.path.exists(repo.name):
                os.chdir(repo.name)
                print('Updating repo: %s' % (repo.name))
                os.system('git pull')
                os.chdir('..')
            else:
                if private:
                    print('Cloning private repo: %s' % (repo.name))
                    os.system('git clone git@github.com:%s/%s.git' % (repo.owner, repo.name))
                else:
                    print('Cloning repo: %s' % (repo.name))
                    os.system('git clone git://github.com/%s/%s.git' % (repo.owner, repo.name))
        
            # return to base
            os.chdir('..')
            print

if __name__ == '__main__':
    run()
