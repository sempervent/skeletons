# SKELETONS - bare-bones templates for the lazy

`skeletons` is a python package that helps you create template-able projects quickly.

This repo was created based off of a gist I wrote one day
regarding a skeleton bash script. I had in my `.bashrc` a 
function that would pull down the script and rename it the 
argument to that function. I have expanded the templates to 
include both R and Python skeletons.

# Installation
`pip install .`

# Installation (deprecated but still supported for OGs)

Simply run the `./install` script located in the directory.
You can feel free to modify the script as desired (e.g., 
redirect installation path, etc.

# Usage
Call `skeletons help` for basic usage instructions. Generally `-h|--help` is supported for instructions.

# Specific Skeletons

## Bash Skeleton
The bash_skeleton.sh in the `templates`
```PROJECT=\<project name\> \
PROJECT_DESCRIPTION="something very long and boring" \ 
make_bash_script <name_of_\script>
```

## Python Skeleton
