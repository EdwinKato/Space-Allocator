[![Build Status](https://travis-ci.org/EdwinKato/Space-Allocator.svg?branch=master)](https://travis-ci.org/EdwinKato/Space-Allocator)

# Space Allocator

A simple python command line application to manage and allocate office and living space to new people joining the
Dojo

## Features
* Creation of new rooms
* Adding a new person
* Prints all the people in a room
* Prints allocations on the screen
* Prints the list of unallocated people to the string
* Reallocation of a person from one room to another
* Loads people from a file into the system
* Persists all the data stored in the app to an sqlite database
* Loads data from an sqlite database into the app


## Installation

Just clone the repository and remove the `.git` folder:

```sh
$ git clone https://github.com/EdwinKato/Space-Allocator.git
$ cd my-app
$ rm -rf .git
$ pip install -r requirements.txt
```

## Commands, their usage and examples

### create_room

This command is responsible for creation of a new room. It takes room_type and room_name
as parameters where by room_name can be one or more values.

```
create_room <room_type> <room_name>

create_room office first_test_office
```

### add_person

This command is used to create and assign a person to a room
```
add_person <first_name> <last_name> <person_type> [<wants_accommodation>]

add_person Eden Hazard fellow Y
```

### print_room

Prints out the people in the room to the screen
```
print_room <room_name>
print_room first_test_office

```

### print_allocations

Prints a list of allocations onto the screen.
Specifying the file_name here outputs the registered allocations to a txt file.

```
print_allocations [<file_name>]
print_allocations file.txt

```

### print_unallocated

Prints a list of unallocated people to the screen.
Specifying the file_name here outputs the information to the txt file provided.

```
print_unallocated [<file_name>]
print_unallocated file.txt

```

### reallocate_person

Reallocate the person with person_identifier to new_room_name .

```
reallocate_person <person_identifier> <new_room_name>
reallocate_person 1 test_office

```

### load_people

Adds people to rooms from a txt file.

```
load_people [<file_name>]
load_people file.txt
```

### save_state

Persists all the data stored in the app to an SQLite database.

```
save_state [<sqlite_database>]
save_state sqlite_database.db
```

### load_state

Loads data from a database into the application.

```
load_state [<sqlite_database>]
load_state sqlite_database.db
```

## Tests

Enables you to run tests on the different parts of the application to ensure that they are running as intended.

### Running tests
Open the terminal and type in the command below to run tests on the program.
Please remember to use the correct python installation on your system. Replace with ```python3``` if need be.
```
python3 -m unittest tests/test_dojo.py
```

### Gather test coverage data
Determine the percentage of code tested.
Test coverage is done using coverage.py and is adapted from http://nedbatchelder.com/code/coverage/
Follow the link to find out more about installation and usage.

```
coverage run -m unittest discover -s tests/
```
### Print / Output test coverage report

#### Command-line report
Use the commands below to print out a simple command-line report

```
coverage report -m
```

#### HTML report

To print a fancier HTML report:

```
coverage html
open htmlcov/index.html
```

## Dependencies

* docopt *Version 0.6.2*
* colorama *Version 0.3.9*
* colorful *Version 0.3.8*
* prettytable *Version 0.7.2*
