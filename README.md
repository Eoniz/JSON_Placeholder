# JSON Placeholder

(Future) API in order to generate JSON Placeholder given a yaml config

## Example

**input:**
```yaml
string:
  type: string
string_array:
  type: array
  array:
    type: string
string_with_values:
  type: string
  values:
    - "hello"
    - "world"
    - "doh"
string_array_with_values:
  type: array
  array:
    type: string
    values:
      - "hello"
      - "world"
      - "doh"
  min: 3
  max: 8
int:
  type: int
float:
  type: float
int_with_min_max:
  type: int
  min: 10
  max: 100
float_with_min_max:
  type: float
  min: 10
  max: 100
int_array:
  type: array
  array:
    type: int
float_array:
  type: array
  array:
    type: float
object:
  type: object
  fields:
    - key: object_string
      type: string
    - key: object_int
      type: int
    - key: object_float
      type: float
    - key: object_string_with_values
      type: string
      values:
        - hello
        - world
    - key: object_int_with_min_max
      type: int
      min: 10
      max: 100
    - key: object_float_with_min_max
      type: float
      min: 5.0
      max: 9.0
    - key: object_string_array
      type: array
      array:
        type: string
    - key: object_object
      type: object
      fields:
        - key: foobar_foo
          type: string
        - key: foobar_bar
          type: int
      
```

**output:**
```json
{
    "float": 0.9004249467842805,
    "float_array": [
        0.10737083692611893,
        0.5946585923059131
    ],
    "float_with_min_max": 83.57179648020244,
    "int": 4,
    "int_array": [
        4,
        8,
        9,
        10,
        1,
        5,
        8
    ],
    "int_with_min_max": 44,
    "object": {
        "object_float": 0.750742652893234,
        "object_float_with_min_max": 8.305381509364492,
        "object_int": 7,
        "object_int_with_min_max": 61,
        "object_object": {
            "foobar_bar": 0,
            "foobar_foo": "b"
        },
        "object_string": "b",
        "object_string_array": [],
        "object_string_with_values": "world"
    },
    "string": "c",
    "string_array": [
        "c"
    ],
    "string_array_with_values": [
        "hello",
        "hello",
        "hello",
        "hello",
        "doh",
        "doh"
    ],
    "string_with_values": "world"
}
```

## Installation

```bash
$ pip install -r requirements.txt
```

## Usage

```bash
$ python app.py --path my_file.yaml
```
