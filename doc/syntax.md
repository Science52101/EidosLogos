# Eidos Logos Documentation
## Syntax

In Eidos Logos, there are 6 kinds of tokens:

- **Keywords**: Alphabetic flat case character sequences that work as an _operator_ or specifier. (E.g. `si`, `def`, `non`, `nect`, `aut`)
- **IDs**: Alphanumeric kebab case character sequences that begin with a letter, do not match a keyword and refer to a _stored element_ or a _type_. For non-alphanumeric or keyword-named IDs, a character sequence between backticks (`` ` ``) is used. (E.g. `myId`, `my-id`, `` `my ID` ``, `` `def` ``, `my-id2`)
- **Labels**: Alphanumeric kebab case character sequences that begin with a double quotation mark (`"`), may contain colons (`:`) and refer to a _type_ or an _element label_. (E.g. `"my-label`, `"nummerus`, `"necto:referentia`)
- **Symbols**: Single or contiguous non-alphanumeric characters that work as an _operator_ or delimeter. (E.g. `+`, `::`, `/`, `@`)
- **Braces**: Paired symbols with distinct opening and closing forms that enclose content. (E.g. `(` & `)`, `{` & `}`, `(~` & `~)`)
- **Value literals**: _String_, _number_ or _boolean_ literals.
    - _String_ literals are a sequence of characters between single quotation marks (`'`).
    - _Number_ literals are a sequence of numeric characters with or without a dot (`.`).
    - _Boolean_ literals are `verum` and `falsum` keywords.
    - Examples: `'Lorem ipsum dolor sit amet...'`, `256`, `3.1415`, `.75`, `falsum`, `veritas`.
