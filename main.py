import math
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

class ExprExtension(Extension):

  def __init__(self):
    super(ExprExtension, self).__init__()
    self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):

  def on_event(self, event, extension):
    items = []
    expression = event.get_argument()
    if len(expression) < 1:
        return RenderResultListAction(items)
    try:
      result = str(eval(expression, { '__builtins__': None, 'math': math }))

      items.append(ExtensionResultItem(icon='images/icon.png',
        highlightable=False,
        name=f'{expression} = {result}',
        description='Press \'enter\' to copy to clipboard.',
        on_enter=CopyToClipboardAction(result)
      ))
    except Exception as errorMessage:
      items.append(ExtensionResultItem(icon='images/icon.png',
        highlightable=False,
        name= f'Error: {errorMessage}',
        description='Expression has Error.',
        on_enter=CopyToClipboardAction(errorMessage)
      ))

    return RenderResultListAction(items)

if __name__ == '__main__':
   ExprExtension().run()
