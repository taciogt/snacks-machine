from typing import Callable, Any, TypeVar


T = TypeVar('T')


def currying_repository(f: Callable[..., T], repository: Any) -> Callable[..., T]:
    def g(*args, **kwargs) -> T:
        return f(repository=repository, *args, **kwargs)
    return g
