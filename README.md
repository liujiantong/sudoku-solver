# sudoku-solver

## install sudoku-solver
```bash
pip install -r requirements.txt
```


## run sudoku-solver
- conda python
```bash
pythonw SudokuMain.py
```

- python
```bash
python SudokuMain.py
```


## build app for Mac using PyInstaller

### install pyinstaller
```bash
pip install pyinstaller
pyinstaller -v
```

### generate app icon
```bash
iconutil -c icns ./sudoku.iconset/
```

### build app
```bash
cd sudoku-solver
pyinstaller --clean -i sudoku.icns -w SudokuMain.py
```

### clean build
```bash
rm -rf build/ dist/ 
```


## wxPython tutorial
[Getting started with wxPython](https://wiki.wxpython.org/Getting%20Started#Improving_the_layout_-_Using_Sizers)

[Demo source code](https://extras.wxpython.org/wxPython4/extras/4.0.1/wxPython-demo-4.0.1.tar.gz)


## PyInstaller
[PyInstaller Manual](https://pythonhosted.org/PyInstaller/index.html)

