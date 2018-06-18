#!/usr/bin/env python


import wx
import wx.grid as gridlib

try:
    from agw import pybusyinfo as PBI
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.pybusyinfo as PBI


no_resize_style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION
block_width = 50


class SudokuBlockGrid(gridlib.Grid):
    def __init__(self, parent, sudoku, blockId, size, log):
        gridlib.Grid.__init__(self, parent, -1, style=no_resize_style)
        self.sudoku = sudoku
        self.log = log
        self.blockId = blockId
        self.rows, self.cols = size
        self.CreateGrid(self.rows, self.cols)

        # self.AutoSize()
        self.SetRowLabelSize(0)
        self.SetColLabelSize(0)
        self.SetMargins(0, 0)

        self.AutoSizeRows(False)
        self.AutoSizeColumns(False)

        self.DisableCellEditControl()
        self.DisableDragGridSize()

        for row in xrange(self.rows):
            for col in xrange(self.cols):
                self.SetSize(row, col, block_width)
                self.SetReadOnly(row, col, True)
                self.SetCellFont(row, col, wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                self.SetCellAlignment(row, col, wx.ALIGN_CENTER, wx.ALIGN_CENTER)
                # self.SetCellValue(row, col, "8")

        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnLeftClick)
        self.SetCellHighlightROPenWidth(0)

    def SetSize(self, row, col, width):
        self.SetRowSize(row, width)
        self.SetColSize(col, width)

    def HighlightRow(self, row, color):
        for c in xrange(self.cols):
            self.SetCellBackgroundColour(row, c, color)

    def HighlightCol(self, col, color):
        for r in xrange(self.rows):
            self.SetCellBackgroundColour(r, col, color)

    def HighlightSelection(self, row, col, color):
        self.HighlightRow(row, color)
        self.HighlightCol(col, color)

    def ClearBgColor(self):
        print 'ClearBgColor: %d' % self.blockId
        for r in xrange(self.rows):
            for c in xrange(self.cols):
                self.SetCellBackgroundColour(r, c, wx.WHITE)
        self.ForceRefresh()

    def OnLeftClick(self, evt):
        print("button OnLeftClick:(%d, %d)" % (evt.GetRow(), evt.GetCol()))
        self.sudoku.ClearSelection(self.blockId, evt.GetRow(), evt.GetCol())
        self.SetCellHighlightROPenWidth(1)
        self.ClearBgColor()

        self.HighlightSelection(evt.GetRow(), evt.GetCol(), wx.LIGHT_GREY)
        self.sudoku.HighlightSelection(self.blockId, evt.GetRow(), evt.GetCol())
        evt.Skip()


class NumberGrid(gridlib.Grid):
    def __init__(self, parent, sudoku, log):
        gridlib.Grid.__init__(self, parent, -1, style=no_resize_style)
        self.sudoku = sudoku
        self.log = log
        self.CreateGrid(1, 9)

        # self.AutoSize()
        self.SetRowLabelSize(0)
        self.SetColLabelSize(0)
        self.SetMargins(0, 0)

        self.AutoSizeRows(False)
        self.AutoSizeColumns(False)

        self.DisableCellEditControl()
        self.DisableDragGridSize()

        self.SetRowSize(0, block_width)
        for col in xrange(9):
            self.SetColSize(col, block_width)
            self.SetReadOnly(0, col, True)
            self.SetCellFont(0, col, wx.Font(30, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            self.SetCellAlignment(0, col, wx.ALIGN_CENTER, wx.ALIGN_CENTER)
            self.SetCellValue(0, col, str(col+1))

        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)

    def OnCellLeftClick(self, evt):
        self.log.write("OnCellLeftClick:(%d, %d)\n" % (evt.GetRow(), evt.GetCol()))
        self.sudoku.SetSelectionValue(evt.GetCol() + 1)
        evt.Skip()


class SudokuFrame(wx.Frame):
    def __init__(self, parent, log):
        wx.Frame.__init__(self, None, wx.ID_ANY, title='Sudoku Solver', style=no_resize_style)
        # Add a panel so it looks correct on all platforms
        self.panel = wx.Panel(self, -1, style=0)
        self.blocks = []
        self.selection = None  # (block_idx, row, col)
        self.data = {}

        topSizer = wx.BoxSizer(wx.VERTICAL)
        gridSizer = wx.GridSizer(rows=3, cols=3, hgap=4, vgap=4)
        numberSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        for idx in xrange(9):
            block = SudokuBlockGrid(self.panel, self, idx, (3, 3), log)
            gridSizer.Add(block, 0, wx.EXPAND)
            self.blocks.append(block)

        numberGrid = NumberGrid(self.panel, self, log)
        numberSizer.Add(numberGrid, 0, wx.ALL, 5)

        bmp_undo = wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_OTHER)
        bmp_erase = wx.ArtProvider.GetBitmap(wx.ART_CUT, wx.ART_OTHER)
        bmp_solve = wx.ArtProvider.GetBitmap(wx.ART_FIND, wx.ART_OTHER)
        bmp_quit = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_OTHER)

        undoBtn = wx.Button(self.panel, wx.ID_ANY, ' Undo ')
        undoBtn.SetBitmap(bmp_undo, wx.LEFT)
        eraseBtn = wx.Button(self.panel, wx.ID_ANY, ' Erase ')
        eraseBtn.SetBitmap(bmp_erase, wx.LEFT)
        solveBtn = wx.Button(self.panel, wx.ID_ANY, ' Solve ')
        solveBtn.SetBitmap(bmp_solve, wx.LEFT)
        quitBtn = wx.Button(self.panel, wx.ID_ANY, ' Quit ')
        quitBtn.SetBitmap(bmp_quit, wx.LEFT)

        btnSizer.Add(undoBtn, 0, wx.ALL, 10)
        btnSizer.Add(eraseBtn, 0, wx.ALL, 10)
        btnSizer.Add(solveBtn, 0, wx.ALL, 10)
        btnSizer.Add(quitBtn, 0, wx.ALL, 10)

        self.Bind(wx.EVT_BUTTON, self.OnUndo, undoBtn)
        self.Bind(wx.EVT_BUTTON, self.OnErase, eraseBtn)
        self.Bind(wx.EVT_BUTTON, self.OnSolve, solveBtn)
        self.Bind(wx.EVT_BUTTON, self.OnClose, quitBtn)

        topSizer.Add(gridSizer, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(numberSizer, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(btnSizer, 0, wx.ALL | wx.CENTER, 5)

        frame_width = block_width * 9
        self.SetSizeHints(frame_width, frame_width, frame_width, frame_width)

        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)

    def ClearSelection(self, blockId, row, col):
        self.selection = (blockId, row, col)
        print 'selection:(%d, %d, %d)' % (blockId, row, col)
        for block in self.blocks:
            if block.blockId == blockId:
                continue
            block.ClearBgColor()

    def HighlightSelection(self, blockId, row, col):
        for block in self.blocks:
            if block.blockId == blockId:
                continue
            if block.blockId % 3 == blockId % 3:
                block.HighlightCol(col, wx.LIGHT_GREY)
            if block.blockId / 3 == blockId / 3:
                block.HighlightRow(row, wx.LIGHT_GREY)

    def SetSelectionValue(self, n):
        if self.selection is None:
            return

        print 'block:%d, row:%d, col:%d' % self.selection

        val = str(n)
        blockId, row, col = self.selection
        for block in self.blocks:
            if block.blockId == blockId:
                block.SetCellValue(row, col, val)

                numberIdx = self.GetValueIndex(blockId, row, col)
                print 'numberIdx:%d' % numberIdx
                if val:
                    self.data[numberIdx] = val
                else:
                    del self.data[numberIdx]
                break

    def EraseSelectionValue(self):
        self.SetSelectionValue("")

    @staticmethod
    def GetValueIndex(blockId, row, col):
        # FIXME:
        return (blockId / 3) * 27 + row * 9 + (blockId % 3) + col

    def Solve(self):
        print "Sudoku input:%s" % self.data
        wx.MilliSleep(3 * 1000)
        # solve sudoku with self.data

    def OnUndo(self, evt):
        print 'OnUndo handler'
        evt.Skip()

    def OnErase(self, evt):
        print 'OnErase handler'
        self.EraseSelectionValue()
        evt.Skip()

    def OnSolve(self, evt):
        print 'OnSolve handler'
        evt.Skip()

        waitSec = 3
        message = "Please wait %d seconds, working..." % waitSec
        bmp = wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK, wx.ART_OTHER)
        busy = PBI.PyBusyInfo(message, parent=None, title="Solving Sudoku...", icon=bmp)
        wx.Yield()

        self.Solve()
        del busy

    def OnClose(self, evt):
        self.Close()


if __name__ == '__main__':
    import sys
    app = wx.App(redirect=0)
    frame = SudokuFrame(None, sys.stdout)
    frame.Show(True)
    app.MainLoop()

