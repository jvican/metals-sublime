from LSP.plugin.core.registry import LspTextCommand
from LSP.plugin.core.types import Optional, Dict, Any
from LSP.plugin.core.protocol import Notification

import sublime
import sublime_plugin
import functools

class LspMetalsFocusViewCommand(LspTextCommand):

    session_name = "metals"

    def run(self, edit: sublime.Edit, view_id: int, event: Optional[Dict[str, Any]] = None) -> None:
        view = sublime.View(view_id)
        if not view.is_valid():
            return
        fname = view.file_name()
        if not fname:
            return
        sublime.set_timeout_async(functools.partial(self.run_async, fname))

    def run_async(self, fname: str) -> None:
        session = self.session_by_name()
        if not session:
            return
        uri = session.config.map_client_path_to_server_uri(fname)
        session.send_notification(Notification("metals/didFocusTextDocument", {"uri": uri}))


class ActiveViewListener(sublime_plugin.EventListener):
    def on_activated(self, view: sublime.View) -> None:
        if view.file_name():
            view.run_command("lsp_metals_focus_view", {"view_id": view.id()})
