#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright: (c) 2016, [Daniel Dye (https://gist.github.com/dandye/dfe0870a6a1151c89ed9)]
# Copyright: (c) 2021, [Jean Claveau (https://gist.github.com/jclaveau/af2271b9fdf05f7f1983f492af5592f8)]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import sys
import os
import json
import re
import subprocess

# """
# This script replaces vars written between brackets like "{{ remote.origin.url }}" by their values.
# Used as a pre-commit hook[2] to update the README.md file's and have badges matching the current branch
#
# [1] http://stackoverflow.com/questions/18673694/referencing-current-branch-in-github-readme-md
# [2] http://www.git-scm.com/book/en/v2/Customizing-Git-Git-Hooks
# [4] https://gist.github.com/dandye/dfe0870a6a1151c89ed9
# """

argv = sys.argv
if len(argv) < 3:
    print(os.path.basename(__file__) + " [input_file] [ouput_file] [-v]")
    quit()

input_file = argv[1]
output_file = argv[2]
verbose = len(argv) == 4 and argv[3] == '-v'

if verbose:
    print("Starting replacing vars in " + input_file + " to generate " + output_file)

git_vars = {}

# retrieve git config
config = subprocess.check_output([
    "git",
    "config",
    "--list",
]).strip().decode('utf-8').split('\n')

for config_rule in config:
    parts = config_rule.split('=')
    git_vars[parts[0]] = parts[1]

# Get the name
git_vars['repository.name'] = re.findall("([^:]+)\.git$", git_vars['remote.origin.url'])[0]

# retrieve current branch name
git_vars['current.branch'] = subprocess.check_output([
    "git",
    "rev-parse",
    "--abbrev-ref",
    "HEAD",
]).strip().decode('utf-8')

# retrieve current commit hash
git_vars['current.commit'] = subprocess.check_output([
    "git",
    "rev-parse",
    "HEAD",
]).strip().decode('utf-8')

# retrieve tags and current version
git_vars['tags'] = subprocess.check_output([
    "git",
    "tag",
    "--list",
]).strip().decode('utf-8')
git_vars['current.version'] = git_vars['tags'][0] if len(git_vars['tags']) else None

if verbose:
    print(json.dumps(git_vars, indent=4))

lines = open(input_file).readlines()
changed = False
with open(output_file, "w") as fh:
    fh.write('<!---\n')  # https://stackoverflow.com/a/4829998/2714285
    fh.write("This file is auto-generate by a github hook please modify " + input_file + " if you don't want to loose your work\n")
    fh.write('-->\n')
    for line in lines:
        new_line = line
        for entry in git_vars:
            pattern = '{{\s*' + entry + '\s*}}'
            if len(re.findall(pattern, new_line)):
                new_line = re.sub(pattern, git_vars[entry], new_line)
                if verbose:
                    print("Found {{ " + entry + " }} in:\n   " + line + "=> " + new_line)
                changed = True
        fh.write(new_line)

if not changed and verbose:
    print("No variable found in " + output_file)

subprocess.check_output(["git", "add", output_file])

# If output_file and input_file are the same only the replacement will be added for commit
with open(input_file, "w") as fh:
    for line in lines:
        fh.write(line)

if verbose:
    print(output_file + " variables replaced")
