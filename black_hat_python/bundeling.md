Using pyinstaller everything can be bundled into one portable executable. If a file, e.g. `target_file.py` should be compiled to a single executable use the following command:

```bash
pyinstaller  target_file.py --onefile
```

Note that cross-compilation is not possible as far as I am aware. Hence if Windows is the target it also has to be compiled on windows.