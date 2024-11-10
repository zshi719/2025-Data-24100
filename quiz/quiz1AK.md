## Quiz 1 AK

There were two different versions of the quiz with slightly different naming. The AK to version "A" is below, but is easily adapted to the other versions.

There were a few common errors / changes:

1. Confusion between  `cat` and `ls` 
2. When starting with relatives paths it is unnecessary to add  `./` at the start. Just provide the  simplified path (e.g. `rm ./docs/image2.jpg` vs. `rm docs/image2.jpg`)
3. Changing directories (using `cd`) rather than just directly executing the command.


---


1. Move all `*.pdf` files from one sub-directory to another:

```
mv docs/*.pdf forms
```

2. Return all lines in Moby Dick that have the word `whale` in it.

```
Two versions:
cat docs/MobyDict.txt | grep -i whale
grep -i whale docs/MobyDick.txt
```

3. Using a relative path list all files in a sibling directory

```
ls ../docs/*.jpg
```

4. Create a file containing _all_ file contents of a directory

```
ls -a > dir_list.txt
```

5. Delete a file

```
rm docs/image2.jpg
```

