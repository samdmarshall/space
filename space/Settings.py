# Copyright (c) 2017, Samantha Marshall (http://pewpewthespells.com)
# All rights reserved.
#
# https://github.com/samdmarshall/space
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# 3. Neither the name of Samantha Marshall nor the names of its contributors may
# be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import yaml
import shlex
from .          import Executor

class Configuration(object):
    def __init__(self):
        # exec evaluation
        self.__prefs_path = os.path.expanduser('~/.config/space/spaces.yml')
        if os.environ.get('SPACE_CONFIG') is not None:
            self.__prefs_path = os.path.expanduser(os.environ.get('SPACE_CONFIG'))
        if os.path.exists(self.__prefs_path) is False:
            print('space cannot find a configuration file! configuration file "spaces.yml" is expected at "~/.config/space/spaces.yml" or at a custom path defined by "SPACE_CONFIG" environment variable')
        
        # load the prefs file
        fd = open(self.__prefs_path, 'r')
        prefs_raw_data = fd.read()
        fd.close()

        # interpret the yaml
        self.__prefs_data = None
        try:
            self.__prefs_data = yaml.safe_load(prefs_raw_data)
        except yaml.YAMLError as exc:
            print('Error in configuration file:', exc)
        if self.__prefs_data is None:
            print('unable to load configuration file! valid yaml file required')

    def is_valid(self):
        working_path = os.path.abspath(os.curdir)
        keys = list() if self.__prefs_data is None else self.__prefs_data.keys()
        applicable_paths = [path for path in keys if os.path.expanduser(path) == working_path]
        return (len(applicable_paths) > 0)

    def commands(self):
        working_path = os.path.abspath(os.curdir)
        applicable_paths = list()
        for space_path in self.__prefs_data.keys():
            full_space_path = os.path.expanduser(space_path)
            shared_path = os.path.commonprefix([full_space_path, working_path])
            if os.path.exists(shared_path) is True and len(full_space_path) <= len(working_path):
                applicable_paths.append(space_path)
        applicable_paths.sort(key=len, reverse=True)
        if len(applicable_paths) > 0:
            closest_directory = applicable_paths[0]
            self.__commands = self.__prefs_data[closest_directory]
        else:
            self.__comands = {}
        return list(self.__commands.keys())

    def invoke(self, command):
        found_command = command in self.__commands.keys()
        if found_command is True:
            exec_commands = [cmd for cmd in self.__commands[command] if cmd is not None]
            for exec_line in exec_commands:
                output, error = Executor.Invoke(shlex.split(exec_line))
                if error:
                    print(error)
                    break
                sys.stdout.write(output)
                sys.stdout.flush()
        return found_command
            
