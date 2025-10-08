## Quiz 1 AK

There were two different versions of the quiz with slightly different naming and file structure. The answer keys for both versions "A" and "B" are provided below.

There were a few common errors / changes:

1. Confusion between `cat` and `ls` - remember `cat` shows file contents, `ls` lists files
2. When starting with relative paths it is unnecessary to add `./` at the start. Just provide the simplified path (e.g. `cp ./docs/file.txt backup` vs. `cp docs/file.txt backup`)
3. Changing directories (using `cd`) rather than just directly executing the command
4. Forgetting the `-i` flag for case-insensitive searches with `grep`
5. Using `>` (overwrite) vs `>>` (append) - for creating a new file, `>` is correct
6. Forgetting to use wildcards (`*.txt`, `*.pdf`) when working with multiple files of the same type
7. Confusion about when to use `-a` with `ls` - use it when you want to include hidden files (those starting with `.`)

---

## Quiz 1A Answers

**Question 1:** Copy all `.txt` files from the `documents` sub-directory to the `backup` directory (from `/home/alice`, using relative paths)

```bash
cp documents/*.txt backup
```

Alternative (if you want to be more explicit):
```bash
cp documents/*.txt backup/
```

---

**Question 2:** Return all lines in `report.txt` in the `projects` subdirectory that have the word `data` in it (case-insensitive, from `/home/alice`)

```bash
Two versions:
grep -i data projects/report.txt
cat projects/report.txt | grep -i data
```

Note: The first version is preferred as it's more concise.

---

**Question 3:** List all `.pdf` files in `/home/alice/documents` using a relative path (from `/home/bob`)

```bash
ls ../alice/documents/*.pdf
```

---

**Question 4:** Create a file `/home/bob/log_list.txt` containing a list of all files (excluding hidden) in `/home/bob/logs` (from `/home/bob`)

```bash
ls logs > log_list.txt
```

Alternative (more explicit with absolute path for output):
```bash
ls logs > /home/bob/log_list.txt
```

Note: Since we're already in `/home/bob`, the first version is simpler. Do NOT use `-a` flag since the question specifically says "excluding hidden".

---

**Question 5:** Print the first ten lines in `projects/data.csv` using an absolute path (from `/home/alice`)

```bash
head /home/alice/projects/data.csv
```

Note: `head` by default shows the first 10 lines, so no flags are needed.

---

## Quiz 1B Answers

**Question 1:** Print the first ten lines in `research/experiment.log` using a relative path (from `/home/maria`)

```bash
head research/experiment.log
```

---

**Question 2:** List all `.pdf` files in `/home/maria/papers` using a relative path (from `/home/john`)

```bash
ls ../maria/papers/*.pdf
```

---

**Question 3:** Copy all `.pdf` files from the `papers` sub-directory to the `archive` directory (from `/home/maria`, using relative paths)

```bash
cp papers/*.pdf archive
```

Alternative (if you want to be more explicit):
```bash
cp papers/*.pdf archive/
```

---

**Question 4:** Create a file `/home/john/temp_list.txt` containing a list of all files (including hidden) in `/home/john/temp` (from `/home/john`)

```bash
ls -a temp > temp_list.txt
```

Alternative (more explicit with absolute path for output):
```bash
ls -a temp > /home/john/temp_list.txt
```

Note: The `-a` flag is required here because the question specifically says "including hidden".

---

**Question 5:** Return all lines in `papers/draft.txt` that have the word `results` in it (case-insensitive, from `/home/maria`)

```bash
Two versions:
grep -i results papers/draft.txt
cat papers/draft.txt | grep -i results
```

Note: The first version is preferred as it's more concise.

