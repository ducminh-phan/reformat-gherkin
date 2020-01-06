from attr import dataclass


def prepare(cls=None, slots=True, frozen=True, eq=False):
    """
    A common class decorator to decorate AST node classes. We can either use `@prepare`
    with default parameters, or `@prepare(...)` to override the default values of the
    parameters. By default, `eq=False` makes the objects hashable, and the hash is an
    object's id. Therefore, every AST node is unique, even if they have identical
    attributes (think of two identical rows or steps at two different places in a
    document).
    """
    wrapper = dataclass(slots=slots, frozen=frozen, eq=eq)

    if cls is None:
        return wrapper

    return wrapper(cls)
