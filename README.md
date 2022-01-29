# bwf - Bitwarden CLI, but friendly

## What is it?
This program is just a wrapper on a Bitwarden-CLI. The goal of this
wrapper is to provide more user-friendly interaction with your valet.
The original Bitwarden-CLI is a very powerfool tool, but when you want
to get or create some item in your valet all actions are performed
via json input and output. This wrapper offers a simple user-friendly
text interaction via command line.

## How to install?
You can install this program using pip:
```
pip install -i https://test.pypi.org/simple/ bwfriendly==0.0.2
```
After install you will be able to call a script called `bwf` from
your command line to start a program.

> The wrapper depends on an original Bitwarden-CLI, so you
> need to 
> [install](https://bitwarden.com/help/cli/#download-and-install) it

## How to use?
The tool is self-documented, so just write `bwf -h` or `bwf --help`

There is also an interactive mode (`-i` or `--interactive`)
, that persists a session token. It is very useful when you need to 
perform several operations on your wallet without entering
a password for each command. Subcommands for interactive and classic
modes are absolutely the same, except interactive mode has `exit`
subcommand to exit from interactive cli.

I will just duplicate the usage here:

`show`, `create`, `delete`, `logout` - are subcommands:

### show
show - lists usernames and passwords of items which names
correspond to a search pattern (empty search pattern = all records):

usage:

`show -p pattern` - list only passwords

`show -u pattern` - list only usernames

`show -p` - lists all passwords

`show -u` - lists all usernames

`show` == `show -up` == `show -u -p` - lists all usernames and passwords

### create
create (interactive) - creates a new credentials record in your wallet:

usage:

`create -p item_name` - create only password record 

`create -u item_name` - create only username record 

`create -u -p item_name` == `create -up item name` - create full record

### delete
delete (interactive) - removes a record from your wallet that corresponds
to a search pattern (if multiple items match -> requests user to choose one):

usage:
`delete item_name` - deletes an item

## Contribution
I am very open to criticism and different views, this is my
first project, so I will be happy to see your reviews 
and contributions. Presently, the project has a very limited 
functionality and looks unfinished, so there is staff to do, join)