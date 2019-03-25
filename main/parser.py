from importlib import import_module

from gherkin.errors import ParserError
from gherkin.parser import Parser

from .errors import DeserializeError, InvalidInput
from .utils import camel_to_snake_case


def get_model_from_type(type_):
    file_name = camel_to_snake_case(type_)
    module_path = f"main.models.{file_name}"

    module = import_module(module_path)

    return getattr(module, type_)


def deserialize(parse_results):
    """
    Deserialize the JSON object returned from gherkin library. The results are
    instances of models defined in main.models. The parse results are deserialized
    recursively.
    """
    if isinstance(parse_results, list):
        return [deserialize(result) for result in parse_results]

    if isinstance(parse_results, dict):
        # Location objects do not have the key `type` in the JSON representation
        if "type" in parse_results:
            type_ = parse_results.pop("type")
        else:
            type_ = "Location"

        model = get_model_from_type(type_)

        deserialized_results = {}
        for key, value in parse_results.items():
            # Note that keys are in camelCase convention, for example, tableHeader,
            # tableBody. Therefore, we need to convert the keys to snake case here.
            deserialized_results[camel_to_snake_case(key)] = deserialize(value)

        return model(**deserialized_results)

    return parse_results


def parse(content):
    """
    Parse the content of a file to a Gherkin document model.
    """
    parser = Parser()

    try:
        parse_result = parser.parse(content)
    except ParserError as e:
        raise InvalidInput(e)

    try:
        result = deserialize(parse_result)
    except Exception as e:
        raise DeserializeError(f"{e.__class__.__name__}:\n{e}")

    return result
