import pytest

from json_placeholder.parser.parser import (
    _handle_array,
    _handle_float,
    _handle_int,
    _handle_string,
    _handle_object,
    parse_yaml
)

@pytest.mark.unit_tests
def test__handle_string_with_values():
    fake_obj = {
        "type": "string",
        "values": ["a"]
    }

    value = _handle_string(fake_obj)
    assert value == "a"
    assert isinstance(value, str)


@pytest.mark.unit_tests
def test__handle_string_without_values():
    fake_obj = {
        "type": "string"
    }

    value = _handle_string(fake_obj)
    assert value in ["a", "b", "c"]
    assert isinstance(value, str)


@pytest.mark.unit_tests
def test__handle_int_with_min_max():
    fake_obj = {
        "type": "int",
        "min": 10,
        "max": 100
    }

    value = _handle_int(fake_obj)
    assert 10 <= value <= 100
    assert isinstance(value, int)


@pytest.mark.unit_tests
def test__handle_int_without_min_max():
    fake_obj = {
        "type": "int",
    }

    value = _handle_int(fake_obj)
    assert 0 <= value <= 10
    assert isinstance(value, int)


@pytest.mark.unit_tests
def test__handle_float_with_min_max():
    fake_obj = {
        "type": "float",
        "min": 10,
        "max": 100
    }

    value = _handle_float(fake_obj)
    assert 10.0 <= value <= 100.0
    assert isinstance(value, float)


@pytest.mark.unit_tests
def test__handle_float_without_min_max():
    fake_obj = {
        "type": "float",
    }

    value = _handle_float(fake_obj)
    assert 0.0 <= value <= 1.0
    assert isinstance(value, float)


@pytest.mark.unit_tests
def test__handle_object_without_fields():
    fake_obj = {
        "type": "object",
    }

    value = _handle_object(fake_obj)
    assert value == {}
    assert isinstance(value, dict)


@pytest.mark.unit_tests
def test__handle_object_skips_fields_without_key():
    fake_obj = {
        "type": "object",
        "fields": [
            {
                "type": "string"
            }
        ]
    }

    value = _handle_object(fake_obj)
    assert value == {}
    assert isinstance(value, dict)


@pytest.mark.unit_tests
def test__handle_object_skips_fields_without_type():
    fake_obj = {
        "type": "object",
        "fields": [
            {
                "key": "foo"
            }
        ]
    }

    value = _handle_object(fake_obj)
    assert value == {}
    assert isinstance(value, dict)


@pytest.mark.unit_tests
def test__handle_object_with_fields():
    fake_obj = {
        "type": "object",
        "fields": [
            {
                "key": "foo",
                "type": "string"
            }
        ]
    }

    value = _handle_object(fake_obj)
    assert "foo" in value
    assert isinstance(value["foo"], str)
    assert isinstance(value, dict)


@pytest.mark.unit_tests
def test__handle_array_without_array_field():
    fake_obj = {
        "type": "array",
    }

    value = _handle_array(fake_obj)
    assert len(value) == 0
    assert isinstance(value, list)


@pytest.mark.unit_tests
def test__handle_array_with_array_field_without_type_field():
    fake_obj = {
        "type": "array",
        "array": {
            "values": [ "hello", "world", "doh" ]
        }
    }

    value = _handle_array(fake_obj)
    assert len(value) == 0
    assert isinstance(value, list)


@pytest.mark.unit_tests
def test__handle_array_with_array_field_with_type_field():
    fake_obj = {
        "type": "array",
        "array": {
            "type": "string",
            "values": [ "hello", "world", "doh" ]
        },
        "min": 1,
        "max": 1
    }

    value = _handle_array(fake_obj)
    assert len(value) == 1
    assert isinstance(value, list)
    assert isinstance(value[0], str)
    assert value[0] in ("hello", "world", "doh")


@pytest.mark.unit_tests
def test__handle_array_with_array_field_with_type_field_and_min_max():
    fake_obj = {
        "type": "array",
        "array": {
            "type": "string",
            "values": [ "hello", "world", "doh" ]
        },
        "min": 5,
        "max": 10
    }

    value = _handle_array(fake_obj)
    assert 5 <= len(value) <= 10
    assert isinstance(value, list)
    for _value in value:
        assert isinstance(_value, str)
        assert _value in ("hello", "world", "doh")


@pytest.mark.unit_tests
def test_parse_yaml():
    fake_obj = {
        "string": {
            "type": "string"
        },
        "int": {
            "type": "int"
        },
        "float": {
            "type": "float"
        },
        "array": {
            "type": "array",
            "array": {
                "type": "string",
                "values": [ "hello", "world" ]
            },
            "min": 5,
            "max": 10
        },
        "object": {
            "type": "object",
            "fields": [
                {
                    "key": "object_string",
                    "type": "string"
                },
                {
                    "key": "object_int",
                    "type": "int"
                },
                {
                    "key": "object_float",
                    "type": "float"
                },
                {
                    "key": "object_array",
                    "type": "array",
                    "array": {
                        "type": "string",
                        "values": [ "hello", "world" ]
                    },
                },
                {
                    "key": "object_object",
                    "type": "object",
                },
            ]
        }
    }

    value = parse_yaml(fake_obj)
    
    assert "int" in value
    assert isinstance(value["int"], int)
    assert "float" in value
    assert isinstance(value["float"], float)
    assert "string" in value
    assert isinstance(value["string"], str)
    assert "array" in value
    assert isinstance(value["array"], list)
    assert "object" in value
    assert isinstance(value["object"], dict)

    sub_obj = value.get("object", None)
    assert "object_int" in sub_obj
    assert isinstance(sub_obj["object_int"], int)
    assert "object_float" in sub_obj
    assert isinstance(sub_obj["object_float"], float)
    assert "object_string" in sub_obj
    assert isinstance(sub_obj["object_string"], str)
    assert "object_array" in sub_obj
    assert isinstance(sub_obj["object_array"], list)
    assert "object_object" in sub_obj
    assert isinstance(sub_obj["object_object"], dict)


@pytest.mark.unit_tests
def test_parse_yaml_skips_items_without_type():
    fake_obj = {
        "string": {
            "values": [ "hello", "world" ]
        }
    }

    value = parse_yaml(fake_obj)
    
    assert "string" not in value
    assert isinstance(value, dict)
