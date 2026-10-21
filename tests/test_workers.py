from app.core.workers import WorkerQueue, Request


def test_worker_error_is_sanitised_and_queue_recovers(qtbot, monkeypatch):
    from app.core import workers
    queue = WorkerQueue()
    original = workers.count_text
    def broken(text, encoding):
        raise ValueError("sensitive document text must not be reported")
    monkeypatch.setattr(workers, "count_text", broken)
    with qtbot.waitSignal(queue.completed, timeout=3000) as signal:
        queue.submit(Request(1, "o200k_base", "private"))
    assert signal.args[1] is None
    assert "sensitive" not in signal.args[3]
    assert "private" not in signal.args[3]
    monkeypatch.setattr(workers, "count_text", original)
    with qtbot.waitSignal(queue.completed, timeout=10000) as signal:
        queue.submit(Request(2, "o200k_base", "hello"))
    assert signal.args[1].tokens == 1


def test_memory_failure_is_understandable(qtbot, monkeypatch):
    from app.core import workers
    queue = WorkerQueue()
    def exhausted(text, encoding):
        raise MemoryError()
    monkeypatch.setattr(workers, "count_text", exhausted)
    with qtbot.waitSignal(queue.completed, timeout=3000) as signal:
        queue.submit(Request(1, "o200k_base", "text"))
    assert "memory" in signal.args[3]
    assert not queue.active
