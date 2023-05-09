import ctypes

from objc_util import ObjCClass
import ui

import pdbg

WKWebView = ObjCClass('WKWebView')
pdbg.state(WKWebView)


class PyWKWebView():

  def __init__():
    pass


class View(ui.View):

  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 0.5


if __name__ == "__main__":
  view = View()
  view.present(style="fullscreen", orientations=["portrait"])

