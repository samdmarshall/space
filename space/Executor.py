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

import sys
import tempfile
import subprocess

try:
    from subprocess import DEVNULL
except ImportError: # pragma: no cover
    import os
    DEVNULL = open(os.devnull, 'wb')

def Invoke(call_args, shell_state=False):
    error = 0
    output = None
    try:
        output = subprocess.check_output(call_args, shell=shell_state, stderr=DEVNULL).decode(sys.stdout.encoding)
    except subprocess.CalledProcessError as exception:
        output = exception.output.decode(sys.stdout.encoding)
        error = exception.returncode
    return (output, error)

def Subshell(env_list,action_list):
    script = '#!/bin/sh \n'
    for env_var in env_list:
        script += env_var + '\n'
    for action in action_list:
        script += action + '\n'
    script_file = tempfile.NamedTemporaryFile('wt')
    script_file.write(script)
    script_file.flush()
    proc = subprocess.Popen(['/bin/bash', script_file.name], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, errors = proc.communicate()
    return stdout, errors;
