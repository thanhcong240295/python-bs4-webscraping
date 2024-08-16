
#!/bin/sh
command -v pylint >/dev/null 2>&1 || { echo >&2 "Running 'pylint' requires it to be installed."; exit 1; }
echo "Running pylint..."
find . -iname "*.py" -path "./src/*" | xargs pylint --rcfile .pylintrc