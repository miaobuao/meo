from threading import Thread
from collections.abc import Callable, Iterable, Mapping
from typing import Any

class ControlledThread(Thread):
    def __init__(self, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = (), kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._status = True
        self._target = target
        self._args = args
        self._kwargs = {} if kwargs is None else kwargs

    def before_run(self): pass
    
    def after_run(self): pass
    
    def step(self):
        raise Exception("ControlledThread.step must implement.")
    
    @property
    def status(self):
        return self._status
    
    def run(self):
        self._status = True
        if self._target is not None:
            try:
                while self._status:
                    self._target(*self._args, **self._kwargs)
            finally:
                del self._target, self._args, self._kwargs
        else:
            self.before_run()
            while self._status:
                self.step()
            self.after_run()
        
    def stop(self):
        self._status = False

if __name__ == '__main__':
    def p():
        print("hi")
    class __Test(ControlledThread):
        def step(self):
            p()
            
    # t = __Test()
    t = ControlledThread(target=p)
    t.start()
    
    import time
    time.sleep(3)
    t.stop()