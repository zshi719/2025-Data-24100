# Terminal, Command Line and Shell

- [Terminal, Command Line and Shell](#terminal-command-line-and-shell)
  - [Motivation and Background](#motivation-and-background)
  - [File systems and paths](#file-systems-and-paths)
  - [Navigating the file system](#navigating-the-file-system)
    - [pwd](#pwd)
  - [ls](#ls)
    - [Wildcards](#wildcards)
    - [Relative vs. Absolute Paths](#relative-vs-absolute-paths)
    - [Special Locations](#special-locations)
  - [cd](#cd)
  - [File \& Directory Manipulations](#file--directory-manipulations)
    - [Directory Manipulations](#directory-manipulations)
    - [File Manipulations](#file-manipulations)
    - [Example Manipulations:](#example-manipulations)
  - [Footnotes](#footnotes)

## Motivation and Background

- Shells and terminals are the fundamental means of interacting with a computer.
- Allow for repeatable, complex and debug-able sessions. 
- They are lightweight and tend to be more stable that "GUI"<a href="#footnote-1">[1]</a>
- Unix-y systems (what we will work on) have a common set of tools and language that allow for users to transfer their knowledge across a wide variety of different environments.
- All OS have a text based interface, though some are different:
  - Windows has Powershell which is based on MS-DOS
  - Underlying modern Macs is a system called BSD, which is is a Unix-y system.
- We use a `terminal` to run a `shell` session which interacts with the underlying operating system. Though many people use these terms non-specifically and interchangeably.  
  - You can think of a `terminal` as the program you run in your GUI to interact with a `shell` which processes commands and reports output.
- There are _lots_ of different unix-y shells:
  - `sh` is the grand-daddy of most shells and is called the `bourne shell`.
  - `bash` is the most common shell used and is an update to `sh`. It stands for `Bourne-Again SHell`
  - `zsh`, called `z shell` is the default shell on modern macs.
  - On Windows we interact with these shells by installing WSL & Ubuntu.
- When we enter a shell we see a `prompt`, such as `bash-3.2$` which allows us to type in `commands`
  - Prompts are incredibly customizable.
  - `commands` are case sensitive (except on modern macs, &#128580;). You should assume that they are case sensitive.

## File systems and paths

- Unix-y systems store information in a hierarchial manner using directories (usually called folders in GUI-based systems) and files.
- We call the collection of folders and directories the `file system`
- The top of the hierarchy is called the `root`.
- We call the name for a file, including the location within the file system the `path` of a file. 
  - For example: `/Users/nickross/clinic_student_list.txt` 
  - This starts at the `root` and is a map two directories deep (`Users` and `nickross`) and then points to a file `clinic_student_lists.txt`
  - We call the end of the file (`.txt` in the example above, the file _extension_). 
    - It is usually good practice to add extensions to files to denote how they should be used. 
    - There is **no** prohibition on directories having extensions. It is usually good practice to have extensions on files and _not_ on directories.


## Navigating the file system

In this section we'll cover a few core commands required to move around the file system.

### pwd 

- When using a shell our prompt is stationed at a `location`, we call this the present working directory or current working directory.
- The command `pwd` or "print working directory" prints the current location of our shell within the file system.
- If you open a terminal and type `pwd` you should see something like: `/Users/nickross`

## ls

- To list files within the file system we use `ls`
- Typing `ls` at the prompt will return a list of files in the current working directory.
- We can also add an `argument` to the command (in this case a `path`) to list files in a specific directory which is not the `pwd`: `ls /Users/`
- Commands also take `options`/`flags`/`switches` which are structured inputs to a command that effect what occurs. They are usually started with a `-`. In the `ls` command there are three of interest:
  - `ls -a` : List _all_ files including hidden and system files.
  - `ls -l` : list files in _long_ format, including the time it was last changed and the file permissions <a href="#footnote-2">[2]</a>.
  - `ls -t` : List all files from most to least recent change.
- You can combine options:
  - `ls -lt` will list files in the long format, sorted by the most to least recent change.
  - Order does not matter when combining arguments.
- You can combine options and arguments. Options usually go first. So to list all files, including hidden files in long format in the `\Users\nickross\clinic` directory you would type:
  - `ls -la \Users\nickross\clinic`

### Wildcards

- `ls` like many commands can accept wildcards.
- For this class we are interested in `*` which expands to match anything.
- Consider the following examples:
  - `ls /Users/nickross/Downloads/*.pdf` : This will match all files which end with `.pdf` in the specified directory
  - `ls /Users/nickross/*/*.pdf` : This will return any `.pdf` file located in any sub-directory of `/Users/nickross`
  - `ls -lt /Users/nickross/*/*.pdf` : This will return any `.pdf` file located in any sub-directory of `/Users/nickross`, printing the results in long format and sorting by time they were last changed.
- Unlike an `ls` command without a wildcard, the `ls` command with wildcards will return an error if no files are found:

```bash
bash-3.2$ ls *.asdf
ls: *.asdf: No such file or directory
```

### Relative vs. Absolute Paths

- Till now we have only been using Absolute paths which specify the path all the way from the root of the file system (such as `/Users/nickross`).
- To simplify our lives when working in the command line we often use relative paths, which start from the current working directory, rather than from the root.
- For example, the following two commands will do the same thing, assuming that our present working directory is `/Users/nickross`:
  - `ls /Users/nickross/Downloads/*.txt`
  - `ls Downloads/*.txt`
- Since we are assuming that we are already in the `/Users/nickross` directory, the second one "builds" on the `pwd` to create the full path.
- We almost always use relative paths when working in a shell (it's way faster!), but it can lead to problems because commands are conditional on the current location.

### Special Locations
There are a few special locations that you should be aware of:

  1. The root (we already spoke of this), which is the head of hte file system, represented by a `/` with nothing to the left.
  2. `.` ("dot") represents the `pwd`
  3. `..` ("double-dot") represents moving "up" the file-system to the parent directory
  4. `~` represents the users "home" directory. The home directory is a unix-y specific location that represents a user's specific space on the system. Unix-y systems are designed for multiple users. The home directory is a space that is carved out for each user. On most unix-y systems the home director takes the form of `/usr/user_name` or `/user/user_name`. On modern Macs it is `/Users/user_name`.

We can use all of these in our paths and can combine them. Consider the following examples:

- `ls ../nickross/Downloads/*.txt`
- `ls ./Downloads/*.txt`
- `ls ~/Downloads/*.txt`

Assuming that are `pwd` is our home directory and our home directory is `/Users/nickross` all of the above will return the same thing!

## cd

- We use the command `cd` to change our present working directory.
- The command takes the form `cd PATH` where `PATH` can be any path that the user has the required permissions to access.
- The command `cd` with no arguments returns the user to the home directory.
- Examples:
  - `cd /Users/nickross/Downloads`
  - `cd ~/Downloads`
  - `cd ../nickross/Downloads` (assuming my working directory is the `nickross` home directory)
  - `cd ./Downloads` (assuming my `pwd` is the `nickross` home directory)
- All three of the above commands will move the working directory to the `Downloads` subfolder of `nickross`'s home directory.

## File & Directory Manipulations

### Directory Manipulations 

- To create a directory we use `mkdir PATH` where `PATH` is the path of our new directory (either relative or absolute)
- To remove an _empty_ directory we use `rmdir PATH`. Importantly if there are files in the directory it will not get removed.

### File Manipulations

- To create a new file we use `touch PATH` which will create a new file on that `PATH`. **NOTE** If a file already exists on this path the `touch` command will update the time that it was last changed, not delete the file.
- The command `rm PATH` removes the file at the specified `PATH`. 
- We use `cp SOURCE_PATH DESTINATION_PATH` to copy files from one location to another.
- To move files, rather than copy we use `mv SOURCE_PATH DESTINATION_PATH`. We can also use the `mv` command to rename files since renaming is the same operation as moving to a new name!
- Note that many of these operations accept wild cards. 

### Example Manipulations:

1. Create two files in the current directory `file1.txt` and `file2.txt`. Delete `file1.txt` and rename `file2.txt` to `file3.txt`.
    - `touch file1.txt`
    - `touch file2.txt`
    - `rm file1.txt`
    - `mv file2.txt file3.txt`

1. Copy all the text files (`*.txt`) from `Downloads` subdirectory of the user's home directory to a new directory, inside the user's home directory called `delme`.

    - We need to first create the new directory inside the user's home directory:
      - `mkdir ~/delme`
    - We then need to copy all the files from the `Downloads` subdirectory of the home directory to the new directory we just created:
      - `cp ~/Downloads/*.txt ~/delme`




## Footnotes
<p id="footnote-1">
   1. <a href="https://en.wikipedia.org/wiki/Graphical_user_interface">Graphical User Interface</a> <a href="#footnote-1-ref">&#8617;</a> 
</p>

<p id="footnote-2">
   1. We will talk about file permissions later in the quarter.<a href="#footnote-2-ref">&#8617;</a> 
</p>