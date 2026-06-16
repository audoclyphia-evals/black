"""An error-handling model influenced by that used by the Rust programming language

See https://doc.rust-lang.org/book/ch09-00-error-handling.html.
"""

from typing import Generic, TypeVar, Union

T = TypeVar("T")
E = TypeVar("E", bound=Exception)


class Ok(Generic[T]):
    def __init__(self, value: T) -> None:
        self._value = value

    def ok(self) -> T:
        return self._value

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False


class Err(Generic[E]):
    def __init__(self, e: E) -> None:
        self._e = e

    def err(self) -> E:
        return self._e

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True


Result = Union[Ok[T], Err[E]]
