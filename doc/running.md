# Eidos Logos Documentation
## Running

To run Eidos Logos scripts, it is needed to have the software of this repository.

You can install [Git](https://git-scm.com), clone the repository and set it up by yourself ([Python 3](https://www.python.org) is also needed to run the scripts) or fetch it as `EidosLogos` with [`spac`](https://github.com/Science52101/spac):

```sh
spac fetch https://github.com/Science52101/EidosLogos.git
spac inst EidosLogos
```

> [!NOTE]
> Using `spac` may require special permissions for some systems.

You can run it with `spac` with the `elog` command:

```sh
spac r elog [commands ...]
```

The `elog` command in `EidosLogos` for `spac` will be used for this tutorial.
The `spac r` prefix will be removed, so please make sure to write `elog open f.elog run` as `spac r elog open f.elog run` when using `spac`.

### The Eidos Logos software

The software includes a tokenizer, a parser, an interpreter and a command-line interface to use them in Python scripts.

The interface is the `elog.py` script file at the `src` directory in the repository and can be executed with `python`.
Check the format:

```sh
python <repo>/src/elog.py [commands ...]
```

> [!NOTE]
> Replace `<repo>` with the directory for the Eidos Logos repository.

With the `elog` commadn for `spac`, it becomes easier:

```sh
elog [commands ...]
```

`[commands ...]` must be replaced with an ordered list of commands separated by whitespaces.
Check the list of commands below:

- **`no-latin`**: Uses English Eidos Logos instead of default/Latin Eidos Logos for the tokenizer and the interpreter.
- **`open`:** Opens a file with the path string that succeeds the command's name and reads its content to the code string.
- **`init_tokenizer`:** Initializes the tokenizer.
- **`tokenize`:** Executes the initialized tokenizer with the code string, generating the tokens (for details, q.v. [Syntax](./syntax.md)).
- **`print_tokens`:** Prints the tokens.
- **`init_parser`:** Initializes the parser with the tokens.
- **`parse`:** Executes the initializes parser, generating the nodes.
- **`print_nodes`:** Prints the nodes.
- **`init_interpreter`:** Initializes the interpreter with the nodes.
- **`interpret`:** Executes the initialized interpreter and prints the returned values.
- **`run`:** Adds `init_tokenizer`, `tokenize`, `print_tokens`, `init_parser`, `parse`, `print_nodes`, `init_interpreter` and `interpret` to the command list automatically.

Example: A common usage:
```bash
elog open hello_world.elog run
```
