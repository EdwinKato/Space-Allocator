"""space_allocator.py

Usage:
    create_room <room_type> <room_name>
        Create rooms in the dojo
    add_person <person_name> <FELLOW|STAFF> [wants_accommodation]
        Adds and allocate space to a person in the dojo
    print_room <room_name>
        Prints the names of all the people in room_name on the screen.
    print_allocations [-o=filename]
        Prints a list of allocations onto the screen
    space_allocator.py --version
        Shows the program's version number and exits
    space_allocator.py (-h | --help)
        Show this help message and exit
    print_unallocated [-o=filename]
        Prints a list of unallocated people to the screen
    reallocate_person <person_identifier> <new_room_name>
        Reallocate the person with person_identifier to new_room_name
    load_people [-o=filename]
        Adds people to rooms from a txt file. See Appendix 1A for text input format
    save_state [--db=sqlite_database]
        Persists all the data stored in the app to an SQLite database
    load_state <sqlite_database>
        Loads data from a database into the application.

Options:
  -h --help     Show this screen.
  --version     Show version. 

"""
from docopt import docopt
from src.dojo import Dojo


if __name__ == '__main__':
    # arguments = docopt(__doc__, version='Space allocator 1.0')
    dojo = Dojo()
    dojo.create_room("office", "blue")
    print(dojo)
