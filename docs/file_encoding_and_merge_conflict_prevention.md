# File Encoding and Merge Conflict Prevention

This document provides guidelines for preventing file encoding issues and merge conflicts in the AUTOCLICK project.

## File Encoding

### Guidelines

1. **Always use UTF-8 encoding for all text files**
   - Python files (`.py`)
   - Markdown files (`.md`)
   - JSON files (`.json`)
   - YAML files (`.yml`, `.yaml`)
   - Text files (`.txt`)

2. **Never use UTF-16 or other encodings**
   - UTF-16 introduces null bytes that can cause issues with Git and other tools
   - Other encodings may not be properly supported by all tools and platforms

3. **Check file encoding before committing**
   - Use the pre-commit hook to automatically check file encoding
   - Manually check file encoding if needed: `file -i filename.py`

### Converting File Encoding

If you need to convert a file from another encoding to UTF-8:

#### Using Python:

```python
with open('file.py', 'r', encoding='utf-16') as f:
    content = f.read()

with open('file.py', 'w', encoding='utf-8') as f:
    f.write(content)
```

#### Using iconv (Linux/macOS):

```bash
iconv -f UTF-16 -t UTF-8 file.py > file_utf8.py
mv file_utf8.py file.py
```

#### Using PowerShell (Windows):

```powershell
$content = Get-Content -Path file.py -Encoding Unicode
$content | Set-Content -Path file.py -Encoding UTF8
```

## Merge Conflict Prevention

### Guidelines

1. **Pull changes frequently**
   - Before starting work: `git pull`
   - Before committing: `git pull --rebase`

2. **Work on separate branches**
   - Create a new branch for each feature or bug fix
   - Keep branches focused on a single task
   - Merge or rebase frequently from the main branch

3. **Communicate with team members**
   - Let others know which files you're working on
   - Coordinate changes to shared files

4. **Use smaller, focused commits**
   - Commit related changes together
   - Use descriptive commit messages
   - Avoid large, sweeping changes across many files

### Resolving Merge Conflicts

If you encounter merge conflicts:

1. **Identify the conflicting files**
   - Git will show you which files have conflicts

2. **Open each conflicting file**
   - Look for conflict markers: `<<<<<<< HEAD`, `=======`, `>>>>>>> branch-name`

3. **Resolve the conflicts**
   - Choose which changes to keep
   - Remove the conflict markers
   - Make sure the file is still valid (syntax, logic, etc.)

4. **Test your changes**
   - Make sure the application still works after resolving conflicts

5. **Commit the resolved files**
   - `git add <resolved-files>`
   - `git commit` or `git rebase --continue`

## Tools and Configuration

### .gitattributes

The `.gitattributes` file ensures consistent line endings and file encoding across different platforms.

```
# Set default behavior to automatically normalize line endings
* text=auto

# Explicitly declare text files to be normalized
*.py text eol=lf encoding=utf-8
*.md text eol=lf
*.txt text eol=lf
*.json text eol=lf
```

### .editorconfig

The `.editorconfig` file ensures consistent editor settings across different editors and IDEs.

```
# EditorConfig is awesome: https://EditorConfig.org

# top-most EditorConfig file
root = true

# Unix-style newlines with a newline ending every file
[*]
end_of_line = lf
insert_final_newline = true
charset = utf-8
trim_trailing_whitespace = true
indent_style = space
indent_size = 4
```

### Pre-commit Hook

The pre-commit hook checks for merge conflicts and null bytes before allowing a commit.

To install the pre-commit hook:

```bash
# Copy the hook to the .git/hooks directory
cp .githooks/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit

# Or configure Git to use the hooks directory
git config core.hooksPath .githooks
```

## Troubleshooting

### Common Issues

1. **File appears empty or corrupted**
   - Check the file encoding: `file -i filename.py`
   - Convert to UTF-8 if needed

2. **Null bytes in file**
   - The file may be UTF-16 encoded
   - Convert to UTF-8 using the methods above

3. **Line ending issues**
   - Configure Git to handle line endings: `git config core.autocrlf input`
   - Use the `.gitattributes` file to specify line endings

4. **Editor shows strange characters**
   - Configure your editor to use UTF-8 encoding
   - Check for BOM (Byte Order Mark) and remove if present
