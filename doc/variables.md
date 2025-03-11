# Eidos Logos Documentation
## Variables

Variables represent _storable values_[^1] in the memory.
Each declared variable pushes a mutable value to the memory list and relates its index to its _ID_ (for details, q.v. [Syntax](./syntax.md)) in the ID map to be accessed later.

[^1]: Let an storable value in Eidos Logos be any element that can be held by a single variable.

### Declaring variables

There are two variable declaring statements in Eidos Logos.

The `def :` (aka. 'LeIn', 'define in') statement takes a _tokenized ID_ (i.e. an ID token that is not wrapped in any node) and a type label (for details, q.v. [Types](./types.md)).

The variable will be declared with the given ID and type, but its value in the memory list will be `"error:indefinitus 0`[^2].

Format:
```elog
def (~ ID ~) : (~ type ~).
```

Example: Declaring a variable of ID `num` and type `"numerus:integer` and a variable of ID `lorem-ipsum` and type `"textus`:

```elog
def num : "numerus:integer.
def lorem-ipsum : "textus
```

The `def ut` (aka. 'LeAs', 'define ut') statement takes a tokenized ID, a type label and a storable value (that can be the result of operations, an ID or a literal).

The variable will be declared with the given ID, type and value (if it matched with the given type).

Format:
```elog
def (~ ID ~) ut (~ type ~) (~ value ~).
```

Example: Declaring a variable of ID `num` and type `"numerus:integer` with the value `0` and a variable of ID `lorem-ipsum` and type `"textus` with the value `'Lorem ipsum dolor sit amet...'`:

```elog
def num ut "numerus:integer 0.
def lorem-ipsum ut "textus 'Lorem ipsum dolor sit amet'
```

[^2]: Please note that storable values are usually annotated in the format `(~ type label ~) (~ value ~)`.
