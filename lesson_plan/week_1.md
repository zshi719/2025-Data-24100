# Week #1 Lesson Plan

## Overview
* There is no _quiz_ during week \#1.
* However, on thursday you will need to verify that your computer is set up according to [the preliminary assignment](../assignments/prelims.md). This will be graded as a quiz (but out of 5 points).
* TuTh will both be lectures.

## Day #1: Terminal, Command Line and Shell

### Learning objectives:

* Describe why we use the shell and terminal rather than GUI-based systems.
* Definitions:
  * Prompt
  * Shell
  * File System
  * File Extension
  * Arguments vs. options/flags/switches 
* Navigating the file system
  * `pwd`, `ls` and `cd`
  * Wildcards (`*`)
  * Relative vs. Absolute paths
  * Special Locations (`.`, `..` and `~`)
* File Manipulations:
  * `mkdir`,  `rmdir`
  * `touch`
  * `mv`, `cp`

### Quizable Concepts:

* Create and remove directory
* Copy, move and remove files (with and without wildcards)
* Use `touch` to create an empty file.
* Move to specific locations in the file system using absolute, relative or special location paths.
* Be able to define the concepts mentioned in the definitions above.

<table>
    <thead>
        <tr>
            <th>Quiz Example</th>
        </tr>
    </thead>
    <tbody>
        <tr>
        <td>Consider the following filesystem:
        </td>
            <td>
                <pre><code>
/
├── users
│   ├── nick
│   │   ├── data
│   │   │   ├── text1.txt
│   │   │   ├── text2.txt
│   │   │   ├── pdf1.pdf
│   │   │   └── pdf2.pdf
│   │   └── notes
│   └── tim
└── system
                </code></pre>
        </td>
        <tr>
        <td>
        Write commands which do the following. Assuming your current working directory is <code>/users</code>.
        </td>
        <td>
        <ul>
        <li>Copy all text files (those that end in txt) from the <code>nick/data</code> directory to the <code>nick/notes</code> directory
        </li>
        <li>Assume your current working directory is <code>/users/nick/data</code>. Change directories, using absolute paths to <code>/users/nick</code>.
        </li>
        <li>Do the same with relative paths.
        </ul>
        </td>
        </tr>
        
</table>



