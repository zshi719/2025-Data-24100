# More Shell and Environments

- [More Shell and Environments](#more-shell-and-environments)
  - [Basic programming](#basic-programming)
    - [Printing with echo](#printing-with-echo)
    - [Variables](#variables)
    - [Listing Variables](#listing-variables)
    - [Piping output and more/less.](#piping-output-and-moreless)
    - [Searching output with grep](#searching-output-with-grep)
    - [Redirecting to a file](#redirecting-to-a-file)
    - [Print the contents of a file](#print-the-contents-of-a-file)
    - [Example](#example)
    - [head and tail](#head-and-tail)
    - [Counting with wc](#counting-with-wc)
  - [Counting Frankenstein](#counting-frankenstein)
  - [API Key and Security Discussion](#api-key-and-security-discussion)
  - [Environments and PATH](#environments-and-path)
    - [Python and Paths](#python-and-paths)

## Basic programming

### Printing with echo

- We use the `echo` command to print.
- `echo 'Hello World!'` will print `Hello World!` to the terminal.

### Variables

- In unix-y systems there are two types of variables present `shell` and `environment` variables.
- `environment` variables are larger in scope (think of them as global variables) while `shell` variables are set only for the current terminal session. 
- To set a shell variable we use an equal sign: `shell_var=10`
- To set an environment variable we use `export` with our assignment, such as `export env_var=20`.
- **Space Sensitive:** Setting variables in either fashion is space sensitive outside of commands: `shell_var = 10` will return an error!
- If there are special characters in a string then you should use single quotes to denote the string, but if there are no special characters then quotes are not required:
  - `string_var_1='asdf'` and `string_var_1=asdf` return the same thing.
- Special characters include spaces, so if you want to use spaces you need to use single quotes:
  - `string_var_2='aaa bbb cc'` is OK, but `string_var_2_=aaa bbb ccc` will return an error.
- To reference a variable we use a `$`, assume that we have run: `var=10`;
  - `echo $var` will return `10`
  - `echo "$var"` will return `10`
  - `echo '$var'` will return `$var` _This is why we use single quotes because it will not expand the special characters!_
- All variables are treated as strings:
  - `echo $var$var` will return `1010` assuming that `var=10` was set previously.

### Listing Variables
- To see what environment variables are set we use the command `ENV` which returns a list of all environment variables (Note that in many (most?) unix-y variants the `ENV` command is _not case sensitive).
- To list all environment _and_ shell variables we use the `SET` command (like `ENV` in most unix-y variants `SET` is not case sensitive).
- Important: when we use `SET` this lists both types of variables (`shell` and `environment`).

### Piping output and more/less.
- When we type `env` we will get a list of variables which is longer than the screen. 
- To redirect output sent to the terminal we use the _pipe_ operator (`|`) which takes the output from one command and pushes it to another.
- In the case of `env` and `set` we want to make the output scrollable. The commands `more` and `less` (which do much of the same thing).
- We can type `env | more` and then we can scroll.
- When using `more` or `less`:
  - The up and down arrows move, line-by-line through the terminal
  - Space will page through the terminal
  - Typing `q` will quit the command and return to the terminal.
- If we want to just send the contents of a file to the `more` or `less` command we type `more filename` or `less filename` and it will present the file inside a scrollable window.

### Searching output with grep
- To filter specific lines we use the `grep` command. This command takes an input and then only returns lines which pass some [regular expression ("regex")](https://en.wikipedia.org/wiki/Regular_expression) condition.
  - If you are unfamiliar with regex skim through the linked wikipedia article. It is beyond the scope of this class to know any specific regex commands.
- If you pass regex a "normal" string then it matches that string. For example if we run `var_1_2=asdf` in order to set a shell variable called `var_1_2` then:
  - `set | grep var_1` will return all rows which have `var_` _anywhere_ in it, including the variable that we just created.
- In this class there are **two flags with grep that you will be required to know**:
  - `-i` will make the match case insensitive.
  - `-v` _excludes_ rather than matches. It will only return rows which do NOT match the condition.
- Assuming that we still have `var_1_2` set from above we could do the following:
  - `set | grep -i VAR_1` and it would still match the above variable.
  - `set | grep -v var_` will match all rows which do NOT contain `var_`.
- Like other commands we can directly send a file to `grep` by providing that file as an argument. 
  - For example: `grep -i nick list_of_students.txt` will search, line-by-line through the file `list_of_students.txt` and return all rows which have `nick` in them (in a case insensitive manner).

### Redirecting to a file
- If, instead of redirecting terminal output to the screen we want to put it in a file we can use the `>` operator.
- For example: `set > delme.txt` will take the list of shell variables and put them into a file, in the working directory, called `delme.txt`.
- We can use the `>>` operator to append to a file, rather then replace (or create a a new file):
- For example consider doing the following:
  - `set > delme.txt` will create/replace the file `delme.txt`
  - If we run it _again_ this will replace the current `delme.txt` with the same content as before.
  - If, after we run our command, we run `set >> delme.txt` it will _double_ the current `delme.txt` file because it will append the contents to the end of file.

### Print the contents of a file
- If we create a file, such as by typing `env > delme.txt` we can then take that file and print it to the terminal using `cat`
- `cat` allows us to take a file that we have previously created and then print it or use pipes to redirect files to other command line tools.

### Example
- For example the following three options will result in the same output to the screen:
  - `env > delme.txt` followed by `grep some_var delme.txt`
  - `env > delme.txt` followed by `cat delme.txt | grep some_var`
  - `env | grep some_var`
  - In the first two examples, interim output is stored as a file called `delme.txt` while in the third the output is redirected straight to `grep`.

### head and tail
- The command `head` (`tail`) will print the first (last) ten lines of a file or redirected output.
- For example:
  - `env | head` will only return ten lines (the first ten)
  - `end | tail` will only return the last ten lines.
- As with other commands you can supply a filename rather than using a pipe:
  - `env > delme.txt` followed by `head delme.txt` will return the same output as `env | head`.

### Counting with wc
- The command `wc` returns three things:
  - lines, words and characters of what is passed to it.
  - `set | wc` will return the lines, words and characters reported by the `set` command.
- We can also pass it files:
  - `set > delme.txt` followed by `wc delme.txt` will return the same as `set | wc`
- If you run `set | wc` you'll see that the number of lines and words is very close, but probably not equal. Why is that?
  - Look at the output of `set`, it is generally of the form: `var=XXXX` which is a single word.
  - However some variables in your environment may have a space in them. You can find them by running: `set | grep ' ' ` which returns lines with spaces.

## Counting Frankenstein
- The file [frankenstein.txt](../example_data/frankenstein.txt) contains the text of the book Frankenstein.
- We are interested in figuring out how many times certain words and phrases were said in the text. 
- Lets answer the following question:
  - How many lines contain the word `frankenstein`? 
  - How many lines contain the word `monster`?
  - How many lines contain the word `creature`?
- Lets first look at the lines which have `frankenstein`:
  - `grep -i frankenstein.txt` will print all the lines to the screen. We use the `-i` to handle case sensitivity since, if `frankenstein` was mentioned as either a proper noun or at the start of a sentence it will be proper cased.
- To count the number:
  - `cat frankenstein.txt | grep -i frankenstein | wc` will return the count of the number of lines! I see 31 returned when I run it.
  - `monster` returns 33 and creature returns 69!

## API Key and Security Discussion
- One of the important uses for shell variables is for transferring information that we want to remain private.
- A common pattern for handling sensitive data, such as API Keys is to start a process, get an API Key and then put it as a shell variable. 
- This provides an additional level of security.
- Importantly for data scientists, who frequently use things like API Keys or other secrets, you need to become comfortable with these systems as they are quite common.
- In this course we will use the Python `os` module to both set and remove environment and shell variables.

## Environments and PATH

- The most important use of environment variables in `unix-y` environments is setting the `PATH` variable.
- The `PATH` variable determines the order of which directories are searched when a command is called. 
- To understanding this a bit better, consider running the following command: `which grep` which will return something like `/usr/bin/grep`
  - The command `which` returns the location of what file is being run.
  - In this case, the `grep` command is located in the `/usr/bin` directory.

### Python and Paths
- Most users of Python have run into environment management problems, where the system isn't playing well with the installation of Python.
- When you type in `which python` it will display a location for where Python exists. In my case I see:
  - `/Users/nickross/.pyenv/shims/python`
  - If you use `conda` or `virtualenv` or another environment management system you will probably see references to it in this path.
  - This means that when I run Python the command above is executed. 
- So, how does the operating system know that this Python should be run?
  - The environment variable `PATH` tells the operating system the order of directories to look at. When I type `echo $PATH` I see:

```
echo $PATH
/Users/nickross/.pyenv/shims:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/System/Cryptexes/
App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/var/run/com.apple.security.cryptexd/codex.system/
bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/
run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin:/Library/TeX/texbin:/
usr/local/munki:/Users/nickross/.ebcli-virtual-env/executables:/Users/nickross/miniconda3/
condabin:/opt/homebrew/bin:/opt/homebrew/sbin:/Applications/iTerm.app/Contents/Resources/utilities
```

- A few notes:
  - You can see that I have pyenv -- but I also installed `conda` at some point in time!
  - I also have a `homebrew` directory listed, which means that I can also install Python via `brew`.
  - However, since when I type `python` I get the `pyenv` version, this means that while `conda` is on my system it actually isn't running and if I install something via `conda` (or `brew`) it may not be accessible by my Python!

- As an example, when I type `pyenv versions` in my terminal I see multiple versions of Python.
- I can switch between versions using `pyenv global [VERSION]`
- When I execute `python` in different versions the executable command is different -- but when I type `which` the location is the same!
  - This is because the file that `which` is pointing to simply a placeholder file which uses other, `pyenv` specific information to determine which python file to execute.
    - If you want to see the _actual_ location of the `python` file that is executed, type the following in a Python terminal: `import sys; sys.executable` which will return the actual location.
    - You can also see this same phenomena when importing packages by using the `__versions__` or `__file__` on an imported package:

| <pre><code>
>>> import pandas
>>> pandas.__version__
'2.1.3'
>>> pandas.__file__
'/Users/nickross/.pyenv/versions/3.11.4/lib/python3.11/site-packages/pandas/__init__.py'
</pre></code> | 
| --- | 

- Looking at the above you can see that my environment has features that point to these specific versions of the packages.