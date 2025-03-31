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

### Comments

It is important to note that anything enclosed into `(~` & `~)`, called 'comment braces', is a _comment_.

Comments are not interpreted or parsed. They are excluded from the token list while tokenizing, so comments do not affect code in any way.
However, comments are used in this documentation and other codes to provide useful information, clarification or to indicate whenever something has to be inserted in a pattern.

Example: A code with excessive comments:

```elog
def x ut "numerus 5. (~ The x variable is defined as a number 5. ~)

def y : (~ may be read as 'in' ~) "necto:referentia. (~ The y variable is defined as a reference. ~)

y := nect (~ `nect` makes a reference ~) x (~ The y variable is now a reference to the x variable. ~)
```

To understand what a comment means in some provided code is important to comprehend it well.

### The period

In Eidos Logos, each statement is made in a _line of content_.
These aren't textual lines, delimited by new line characters, but a continuous complete sequence of characters ended by a period (`.`) where the statement continues.

Please take a look at how each line ends in the previous example, without as many comments:

```elog
def x ut "numerus 5. (~ ends with period ~)

def y : "necto:referentia. (~ ends with period ~)

y := nect x (~ ends with EOF ~)
```

When a line ends at the end of the file, it is not ended with a period.
Periods only serve as an indicator to start a new line when the last line ends, making it clear where a line ends and other starts.

### Parenthesis and precedence

Like periods, parenthesis (`(` & `)`) and other braces are also really important for separating content.
For these beginning the syntax concepts, only the parenthesis will be explained. Other braces will be explained later.

Parenthesis change the precedence of operations.

In Eidos Logos, any operation/node in has its level of precedence setted by the parser.
Please check each level:

1. **Line wrapper level**: `pro`;
2. **Line level**: `def :`, `def ut`, `assere` & `:=`;
3. **Structure level**: `lbd :` & `si ... aliter`;
4. **Boolean generator level**: `=`, `aeq`, `/=`, `aut`, `>`, `<`, `>=`, `<=`, `et`, `vel` & `in`;
5. **Addition level**: `+`, `-`;
6. **Factor level**: `*`, `/` & `mod`;
7. **Power level**: `^`;
8. **Pre-value level**: `_`, `(...)` (function);
9. **Value level**: `(` & `)`, `{` & `}`, `[` & `]`, `nect`, `int`, `:: { ... }`, `-` (unary), `non` & `+`.

Higher-level operations are evaluated first and affect the result of the ones of lower-level.

Please note that the parenthesis are a level 9 node. It means that anything enclosed in parenthesis has to be operated first and its result is used for lower-level operations.
