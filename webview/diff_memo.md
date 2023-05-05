# 差分のメモ

基本的に、3.4 にて情報が増えている状況。情報が減ったとすると、`on_main_thread` をコメントアウトしているくらいか？

## 差分場所と簡単な行数

メモを入れたりして、行数は変化してしまうためあくまでも目安で。

```python
# 61あたり
dummy = self.dummy_webview()
del dummy
```

なぞに、`dummy` を生み出している

```python
# 128あたり
@on_main_thread
def dummy_webview(self):
    dummy1 = WKWebView.WKWebView.alloc().initWithFrame_(((0, 0), (100, 100))).autorelease()

```

事前に、謎の`dummy` でView を生成

```python
# 184, 188

# @on_main_thread
def _eval_js_sync_callback(self, value):
self.eval_js_queue.put(value)

# @on_main_thread
def eval_js_async(self, js, callback=None):
    if self.log_js_evals:
        self.console.message({'level': 'code', 'content': js})
        handler = functools.partial(WKWebView._handle_completion, callback, self)
        block = ObjCBlock(handler,
                          restype=None,
                          argtypes=[c_void_p, c_void_p, c_void_p])
    retain_global(block)
    self.webview.evaluateJavaScript_completionHandler_(js, block)
```

`@on_main_thread` のコメントアウト

```python
# 199 あたり
@ui.in_background
def clear_cache(self, completion_handler=None):
    store = WKWebView.WKWebsiteDataStore.defaultDataStore()
    data_types = WKWebView.WKWebsiteDataStore.allWebsiteDataTypes()
    from_start = WKWebView.NSDate.dateWithTimeIntervalSince1970_(0)

    def dummy_completion_handler():
        pass

    store.removeDataOfTypes_modifiedSince_completionHandler_(data_types, from_start, completion_handler or dummy_completion_handler)

```

`@ui.in_background` がついた
