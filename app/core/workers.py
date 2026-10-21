"""One active task and one latest pending task; no unsafe interruption."""
from dataclasses import dataclass
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot
from app.core.counter import count_text
from app.services.files import read_text, FileImportError


@dataclass(frozen=True)
class Request:
    generation: int
    encoding: str
    text: str = ""
    path: str | None = None
    file_only: bool = False


class Signals(QObject):
    finished = Signal(object, object, object, str)


class Task(QRunnable):
    def __init__(self, request, signals):
        super().__init__()
        self.request, self.signals = request, signals

    def run(self):
        request = self.request
        try:
            text = read_text(request.path) if request.path else request.text
            result = count_text(text, request.encoding)
            self.signals.finished.emit(request, result,
                                       text if request.path and not request.file_only else None, "")
        except MemoryError:
            self.signals.finished.emit(request, None, None,
                                       "Not enough memory. Try a smaller document or Count file.")
        except FileImportError as exc:
            self.signals.finished.emit(request, None, None, str(exc))
        except Exception:
            # Never expose text or arbitrary exception messages in diagnostics.
            self.signals.finished.emit(request, None, None,
                                       "Counting failed. Check the local tokeniser assets or restart Tokentra.")


class WorkerQueue(QObject):
    completed = Signal(object, object, object, str)
    idle = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pool = QThreadPool(self)
        self.pool.setMaxThreadCount(1)
        self.signals = Signals(self)
        self.signals.finished.connect(self._finished)
        self.active = False
        self.pending = None
        self.stopping = False

    def submit(self, request):
        if self.stopping:
            return
        if self.active:
            self.pending = request
        else:
            self.active = True
            self.pool.start(Task(request, self.signals))

    def discard_pending(self):
        self.pending = None

    def stop(self):
        self.stopping = True
        self.discard_pending()

    @Slot(object, object, object, str)
    def _finished(self, request, result, text, error):
        self.active = False
        if not self.stopping:
            self.completed.emit(request, result, text, error)
        if self.pending is not None and not self.stopping:
            pending, self.pending = self.pending, None
            self.submit(pending)
        if not self.active:
            self.idle.emit()
