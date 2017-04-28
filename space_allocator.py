"""
Welcome to the Space allocator.
Usage:
    space_allocator create_room <room_type> <room_name>...
    space_allocator add_person <first_name> <last_name> <person_type> [<wants_accommodation>]
    space_allocator print_room <room_name>
    space_allocator print_allocations [<file_name>] [--table]
    space_allocator print_unallocated [<file_name>]
    space_allocator reallocate_person <person_identifier> <new_room_name>
    space_allocator load_people <file_name>
    space_allocator save_state [<sqlite_database>]
    space_allocator load_state [<sqlite_database>]
    space_allocator (-i | --interactive)
    space_allocator (-h | --help | --version)
Options:
    --version  show program's version number and exit
    --table  Prints out a table on the screen.
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
from docopt import docopt, DocoptExit
import colorful
from src.dojo import Dojo

dojo = Dojo()

def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class SpaceAllocator (cmd.Cmd):
    intro = colorful.bold_green('Welcome to my Space Allocator!\n' \
        + ' (Please type help for a list of commands and guidance.)')
    prompt = '(space_allocator) '
    file = None

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_name>..."""

        for room_name in arg['<room_name>']:
            dojo.create_room(arg['<room_type>'], room_name)

    def default(self, line):
        print(colorful.bold_orange('The command ' + line.lower() + ' is not recognized.' \
            + ' (Please enter another command or type help for list of available commands and their usage.)'))

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> <person_type> [<wants_accommodation>]"""
        if arg['<wants_accommodation>'] is None:
            dojo.add_person(arg['<first_name>'], arg['<last_name>'], arg['<person_type>'])
        else:
            dojo.add_person(arg['<first_name>'], arg['<last_name>'], arg['<person_type>'], arg['<wants_accommodation>'])

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""

        dojo.print_room(arg['<room_name>'])

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [<file_name>] [--table]"""

        if arg['<file_name>'] is not None:
            dojo.print_allocations(arg['<file_name>'])
        else:
            if arg['--table'] is None:
                dojo.print_allocations()
            else:
                dojo.print_allocations(print_table = "Y")

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [<file_name>]"""

        if arg['<file_name>'] is None:
            dojo.print_unallocated()
        else:
            dojo.print_unallocated(arg['<file_name>'])

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <person_identifier> <new_room_name>"""

        dojo.reallocate_person(int(arg['<person_identifier>']), arg['<new_room_name>'])

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people <file_name>"""

        dojo.load_people(arg['<file_name>'])

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [<sqlite_database>]"""

        if arg['<sqlite_database>'] is None:
            dojo.save_state()
        else:
            dojo.save_state(arg['<sqlite_database>'])

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state [<sqlite_database>]"""

        if arg['<sqlite_database>'] is None:
            dojo.load_state()
        else:
            dojo.load_state(arg['<sqlite_database>'])

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    SpaceAllocator().cmdloop()

print(opt)
