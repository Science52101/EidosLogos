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
- **`necto`**: Connected/related elements.
    - _`referentia`_: _References_ to other elements that act like such. (E.g. `ref x` (assuming that `x` is declared))
- **`collectio`**: Collections/sets/groups of elements.
    - _`vector`_: A 1-d. indexed collection of values with. (E.g. `[2 3 5 7]`, `[2 6 8 4 2 4]`)
    - _`matrix`_: A 2-d. double-indexed collection of values a size for both dimensions, sc., a vector of vectors of a single size. (E.g. `[2 3 5 7; 2 6 8 4]`, `[4, 7, 3, 2, 5; 5, 7, 3, 2, 3; 1, 4, 9, 4, 3]`)
- **`nodus`**: Stored pieces of code.
    - _`moles`_: Blocks of code that can be interpreted (with the `int` keyword). (E.g. `:: { def x ut "numerus 3. x^2 }`, `:: { def j : "numerus. accipio j. i * 2 + j }`)
- **`error`**: Errors or unknown values.
    - _`nihil`_: Null values, that, by default, come with an integer value. (E.g. `x := 3` (assuming that `x` is declared) (returns `"error:nihil 0`, but does not propagate to other expressions since it is a _line-level node_ (for details, q.v. [Syntax](./syntax.md).)))
    - _`indefinitus`_: Undefined values, that, by default, come with an integer value. (E.g. `(int :: { def no-value : "textus. no-value })_1`)
- _**`quilibet`**_: Any type or specifier for matching or deduction.

### Annotating types

Type labels may written in the following formats:

- `"(~ basic type ~)`
- `"(~ basic type ~):(~ specifier ~)`
- `"(~ basic type ~):(~ specifier ~):(~ other specifiers... ~)`

Examples:

- `"numerus:integer`
- `"error:nihil`
- `"collectio` or `"collectio:quilibet`
- `"necto:referentia`
- `"veritas`
- `"nodus` or `"nodus:quilibet`
- `"nodus:moles`
- `"numerus` or `"numerus:quilibet`
- `"quilibet`
- `"error:indefinitus`

Types shall be annotated as types labels; however, the interpreter will use raw type names (E.g. `numerus`, `necto:referentia`, `quilibet`).
