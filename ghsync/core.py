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
from clint import args
from clint.textui import puts, colored, indent
import requests
import json
from github2.client import Github

try:
    # check_output is new in 2.7.
    from subprocess import check_output
    def cmd(command):
        return check_output(command, shell=True).strip()
except ImportError:
    # commands is deprecated and doesn't work on Windows
    from commands import getoutput as cmd


__author__ = 'Kenneth Reitz'
__license__ = 'ISC'
__copyright__ = '2011 Kenneth REitz'
__version__ = '0.3.1'

# GitHub configurations
GITHUB_USER = cmd('git config github.user')
GITHUB_TOKEN = cmd('git config github.token')

GHSYNC_DIR = os.environ.get('GHSYNC_DIR', '.')



def run():

    # cli flags
    upstream_on = args.flags.contains('--upstream')
    only_type = args.grouped.get('--only', False)
    organization = args[0]

    os.chdir(GHSYNC_DIR)

    # API Object
    github = Github(username=GITHUB_USER, api_token=GITHUB_TOKEN)


    # repo slots
    repos = {}

    if not organization:
        repos['watched'] = [r for r in github.repos.watching(GITHUB_USER)]
    repos['private'] = []
    repos['mirrors'] = []
    repos['public'] = []
    repos['forks'] = []

    # Collect GitHub repos via API
    for repo in github.repos.list(organization):

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
            is_private = (org in ('private', 'forks', 'mirror', 'public'))
            is_fork = (org == 'forks')

            if is_fork:
                _url = 'http://github.com/api/v2/json/repos/show/{repo.owner}/{repo.name}'.format(repo=repo)
                repo.parent = json.loads(requests.get(_url, ).content)['repository'].get('parent')


            if not only_type or (org in only_type):

                # just `git pull` if it's already there
                if os.path.exists(repo.name):

                    os.chdir(repo.name)
                    puts(colored.red('Updating repo: {repo.name}'.format(repo=repo)))
                    os.system('git pull')

                    if is_fork and upstream_on:
                        print repo.__dict__
                        puts(colored.red('Adding upstream: {repo.parent}'.format(repo=repo)))
                        os.system('git remote add upstream git@github.com:{repo.parent}.git'.format(repo=repo))

                    os.chdir('..')

                else:
                    if is_private:
                        puts(colored.red('Cloning private repo: {repo.name}'.format(repo=repo)))
                        os.system('git clone git@github.com:{repo.owner}/{repo.name}.git'.format(repo=repo))
                        print ('git clone git@github.com:%s/%s.git' % (repo.owner, repo.name))

                        if is_fork and upstream_on:
                            os.chdir(repo.name)
                            puts(colored.red('Adding upstream: {repo.parent}'.format(repo=repo)))
                            os.system('git remote add upstream git@github.com:{repo.parent}.git'.format(repo=repo))
                            os.chdir('..')


                    else:
                        puts(colored.red('Cloning repo: {repo.name}'.format(repo=repo)))
                        os.system('git clone git://github.com/%s/%s.git' % (repo.owner, repo.name))
                        print ('git clone git://github.com/%s/%s.git' % (repo.owner, repo.name))

            # return to base
            os.chdir('..')

if __name__ == '__main__':
    run()
