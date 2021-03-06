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
import argparse
from .version           import __version__ as SPACE_VERSION
from .Logger            import Logger
from .                  import Settings
from .                  import Executor

# Main
def main():
    # setup the argument parsing
    parser = argparse.ArgumentParser(description='space is a tool for managing workspaces')
    parser.add_argument(
        '--version',
        help='Displays the version information',
        action='version',
        version=SPACE_VERSION,
    )
    parser.add_argument(
        '--quiet',
        help='Silences all logging output',
        default=False,
        action='store_true',
    )
    parser.add_argument(
        '--verbose',
        help='Adds verbosity to logging output',
        default=False,
        action='store_true',
    )
    parser.add_argument(
        '--no-ansi',
        help='Disables the ANSI color codes as part of the logger',
        default=False,
        action='store_true',
    )
    parser.add_argument(
        '--debug',
        help=argparse.SUPPRESS,
        default=False,
        action='store_true',
    )
    parser.add_argument(
        '--list',
        help='Displays a list of all available subcommands for the current working directory',
        default=False,
        action='store_true',
    )
    parser.add_argument(
        '--edit',
        help='Opens the space.yml file in your EDITOR',
        default=False,
        action='store_true',
    )
    parser.add_argument(
        '--env',
        help='Passes values into the environment you are working in',
        action='store',
        default='',
    )

    initial_arguments, remaining_args = parser.parse_known_args()

    # perform the logging modifications before we do any other operations
    Logger.disableANSI(initial_arguments.no_ansi)
    Logger.enableDebugLogger(initial_arguments.debug)
    Logger.isVerbose(initial_arguments.verbose)
    Logger.isSilent(initial_arguments.quiet)

    Logger.write().info('Loading the configuration for space...')
    configuration = Settings.Configuration()
    
    if initial_arguments.edit is True:
        Logger.write().info('Launching in editor mode...')
        if os.environ.get('EDITOR') is None:
            Logger.write().critical('The value of EDITOR is not set, defaulting to nano...')
        Logger.write().info('Opening the spaces.yml file in the default editor...')
        Executor.Invoke((os.environ.get('EDITOR', 'nano'), configuration.get_preferences_path()))
    else:
        Logger.write().info('Validating configuration file...')
        if configuration.is_valid() is False:
            Logger.write().warning('No configuration setup for this directory!')
            parser.exit(1, '')

        Logger.write().info('Checking arguments...')
        if initial_arguments.list is True:
            message = '%s [-h] {%s}\n' % (parser.prog, '|'.join(configuration.commands()))
            parser.exit(0, message)
    
        Logger.write().info('Creating subcommand parser...')
        subparsers = parser.add_subparsers(title='Subcommands', dest='command')
        subparsers.required = True

        Logger.write().info('Adding subcommands to command line parser...')
        for command_name in configuration.commands():
            Logger.write().debug('Adding command "%s"...' % command_name)
            command_subparser = subparsers.add_parser(command_name)

        Logger.write().info('Parsing remaining command line arguments...')
        command_args = parser.parse_args(remaining_args)

        Logger.write().info('Running subcommand...')
        if configuration.invoke(initial_arguments.env, command_args.command) is False:
            Logger.write().error('Unknown command "%s" was encountered!' % command_args.command)
            parser.exit(1, '')

if __name__ == "__main__": # pragma: no cover
    main()
