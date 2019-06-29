class BaseError(Exception):
    pass


class InvalidInput(BaseError):
    """
    Raised when the input file cannot be parsed.
    """


class DeserializeError(BaseError):
    """
    Raised when the parse result cannot be deserialized to an AST.
    """


class InternalError(BaseError):
    """
    Raised when something happens anomaly in the process of reformatting.
    """


class EquivalentError(InternalError):
    """
    Raised when the reformatted document is not equivalent to the original one.
    """


class StableError(InternalError):
    """
    Raised when we obtain a different document after reformatting the second time.
    """


class EmptySources(BaseError):
    """
    Raised when there is no file to reformat.
    """


class BaseWarning(Warning):
    pass


class MissingExamplesWarning(BaseWarning):
    """
    Raised when examples are missing in ScenarioOutline
    """


class EmptyExamplesWarning(BaseWarning):
    """
    Raised when an examples table is empty
    """


class NothingChanged(BaseWarning):
    """
    Raised when reformatted code is the same as source.
    """
