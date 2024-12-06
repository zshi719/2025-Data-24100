# Testing

- Testing is the process of systematically evaluating software to:
  1. Verify performance
  2. ID defects and other issues
  3. Validate technical and business requirements
  4. Ensure software components work together as expected.

- Testing can cover both:
  - _functional_ aspects of the code "Does the code work?"
  - _non-functional_ aspects of the code "How _well_ does it work?"

- In general the way testing works is that we specify an action in our code, the expected result and then compare. 

- The following is an example

```python
def sum_two(x,y):
    """Sum Two Functions"""
    return x + y

def test_sum_two():
    """Test for our function"""
    assert sum_two(1,2) == 3
    assert sum_two(-1,1) == 0
```




# JSON Schema Validation

- In testing we want a method to describe data in a light manner for validation purposes. There are a lot of tools for doing this (Pydantic and Cerberus are two others), but we will use [Json Schema](https://json-schema.org/) which is a bit simpler and, IMO, a bit easier to use.
- The basic idea is that you write a JSON object using their language to define the expected data.
- You then run `jsonschema.validate` against the object and it will return any non-conforming code.
- Lets read a few and then go over the specification in a bit more detail.

## Some Examples
```json
// Example 1: List of Strings Schema
{
  "type": "array",
  "items": {
    "type": "string"
  }
}

// Valid data for Example 1:
["apple", "banana", "cherry"]
```

```json
// Example 2: List of Numbers Schema
{
  "type": "array",
  "items": {
    "type": "number"
  }
}

// Valid data for Example 2:
[1, 2.5, 3, 4.7, 5]
```


```json
// Example 3: Dictionary with List of Strings Schema
{
  "type": "object",
  "properties": {
    "fruits": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "count": {
      "type": "integer"
    }
  }
}

// Valid data for Example 3:
{
  "fruits": ["apple", "banana", "cherry"],
  "count": 42
}
```

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "age": { "type": "integer", "minimum": 0 }
  }
}
```

## JSON Schema Types and Their Properties

### string
- **minLength/maxLength**: Control string length
- **pattern**: Regular expression pattern
- **format**: Predefined formats (email, date-time, uri, etc.)
- **enum**: List of allowed values

```json
{
  "type": "string",
  "minLength": 2,
  "maxLength": 100,
  "pattern": "^[A-Za-z]+$",
  "format": "email"
}
```

### number/integer
- **minimum/maximum**: Value range
- **exclusiveMinimum/exclusiveMaximum**: Exclusive range
- **multipleOf**: Number must be multiple of value
- **enum**: List of allowed values

```json
{
  "type": "number",
  "minimum": 0,
  "maximum": 100,
  "multipleOf": 0.5
}
```

### boolean
- Simple true/false validation
- **enum**: Can restrict to specific boolean value

```json
{
  "type": "boolean"
}
```

### array (list)
- **items**: Schema for array items
- **minItems/maxItems**: Array length constraints
- **uniqueItems**: Ensure unique values
- **contains**: Array must contain item matching schema

```json
{
  "type": "array",
  "items": { "type": "string" },
  "minItems": 1,
  "maxItems": 5,
  "uniqueItems": true
}
```

### object
- **properties**: Define object properties
- **required**: List of required properties
- **additionalProperties**: Control extra properties
- **minProperties/maxProperties**: Object size limits
- **dependentRequired**: Property dependencies
- **patternProperties**: Properties matching pattern

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "age": { "type": "integer" }
  },
  "required": ["name"],
  "additionalProperties": false,
  "minProperties": 1
}
```


