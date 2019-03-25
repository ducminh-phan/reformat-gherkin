import re

_first_cap_re = re.compile(r"(.)([A-Z][a-z]+)")
_all_cap_re = re.compile(r"([a-z0-9])([A-Z])")


def camel_to_snake_case(name):
    """
    Convert camelCase to snake_case.
    Taken from https://stackoverflow.com/a/1176023/2585762.
    """
    s1 = _first_cap_re.sub(r"\1_\2", name)
    return _all_cap_re.sub(r"\1_\2", s1).lower()
