# Eidos Logos Documentation
## Running

To run Eidos Logos scripts, it is needed to have the software of this repository.
To download it, you can install Git and clone the repository with the following bash command command:

``` bash
git clone https://github.com/Science52101/EidosLogos.git
```

It is also needed to install Python to execute the scripts.
You can check the download [here](https://www.python.org/downloads/).

### The Eidos Logos software

The software include a tokenizer, a parser, an interpreter and a command-line interface to use them in Python scripts.

The interface is the `elog.py` script file at the `src` directory in the repository and can be executed with `python`.
Check the format:

```bash
python <repo>/src/elog.py [commands ...]
```
> [!NOTE]
> Replace `<repo>` with the directory for the Eidos Logos repository.

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
python .\elog.py open .\hello_world.elog run
```
