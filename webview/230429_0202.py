import ui


class View(ui.View):

  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.wb = ui.WebView()
    self.add_subview(self.wb)


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

