# Sudoku-Solver

## Install Sudoku-Solver
```bash
pip install -r requirements.txt
```


## Run Sudoku-Solver
- conda python
```bash
pythonw SudokuMain.py
```

- python
```bash
python SudokuMain.py
```


## Build app for Mac using PyInstaller

### Install PyInstaller
```bash
pip install pyinstaller
pyinstaller -v
```

### Generate app icon
```bash
iconutil -c icns ./sudoku.iconset/
```

### Build app
```bash
cd sudoku-solver
pyinstaller --clean -i sudoku.icns -w SudokuMain.py
```

### Clean build
```bash
rm -rf build/ dist/
```


## wxPython tutorial
- [Getting started with wxPython](https://wiki.wxpython.org/Getting%20Started#Improving_the_layout_-_Using_Sizers)
- [Demo source code](https://extras.wxpython.org/wxPython4/extras/4.0.1/wxPython-demo-4.0.1.tar.gz)


## PyInstaller
- [PyInstaller Manual](https://pythonhosted.org/PyInstaller/index.html)


## References
- [Exact cover problem](https://en.wikipedia.org/wiki/Exact_cover)
- [Algorithm X algorithm](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X)
- [Dancing Links algorithm](https://en.wikipedia.org/wiki/Dancing_Links)

