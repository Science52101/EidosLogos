# Eidos Logos Documentation
## Types

In Eidos Logos, there are some basic types with some specifiers. A basic type with one or more specifiers is a specific type.

Check all the basic types (**bold**) and specifiers (_italics_):

- **`numerus`**: Numbers.
    - _`integer`_: Integer numbers. (E.g. `7`, `200 + 56`, `3 * 4`, `7^5`)
    - _`fluctuans`_: Floating-point numbers. (E.g. `2.718281`, `.3333`, `2 / 3`, `1 + 1.5`, `1^(.5)`)
- **`textus`**: Text elements.
    - _`catenarius`_: Strings (i.e. character contiguous sequences). (E.g. `'Lorem ipsum dolor sit amet'`, `'Hello, World!'`)
- **`veritas`**: Booleans (i.e. `verum` (true) or `falsum` (false) values).
- **`nexto`**: Connected/related elements.
    - _`referentia`_: _References_ to other elements that act like such. (E.g. `ref x` (assuming that `x` is declared))
- **`collectio`**: Collections/sets/groups of elements.
    - _`vector`_: A 1-d. indexed collection of values with. (E.g. `[2 3 5 7]`, `[2 6 8 4 2 4]`)
    - _`matrix`_: A 2-d. double-indexed collection of values with distinct sizes for each dimension, sc., a vector of vectors of the a size. (E.g. `[2 3 5 7; 2 6 8 4]`)
- **`nodus`**: Stored pieces of code.
    - _`moles`_: Blocks of code that can be interpreted (with the `int` keyword). (E.g. `:: { def x ut "numerus 3. x^2 }`, `:: { def j : "numerus. accipio j. i * 2 + j }`)
- **`error`**: Errors or unknown values.
    - _`nihil`_: Null values, that, by default, come with an integer value. (E.g. `x := 3` (assuming that `x` is declared) (returns `"nihil 0`, but can't be used))
    - _`indefinitus`_: Undefined values, that, by default, come with an integer value. (E.g. `(int :: { def no-value : "textus. no-value })_1`)
- _**`quilibet`**_
