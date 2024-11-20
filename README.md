<h1 align="Center">
<img src="https://raw.githubusercontent.com/Science52101/EidosLogos/refs/heads/main/ars/img/elog_logo.png" alt="ε Log" width="128" heigth="128"/><br>
ε Log
</h1>
<h3 align="center">(Eidos Logos)</h3>

<br><br>

<table align="center">
<tr>
<td>

<h2 align="center">Using:</h3>
<p align="center">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" alt="Python" width="32" heigth="32"/>
</p>

</td>
<td>

<h2 align="center">Planned using:</h3>
<p align="center">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/rust/rust-original.svg" alt="Rust" width="32" heigth="32"/>
</p>

</td>
</tr>
</table>

<br><br>

<h2 align="center">About the project</h3>

This is an experimental programming language test for future script making with mathematical syntax.

Any contribuitions or suggestions from unknown/anonymous people aren't accepted for this project.

If the project branches out into different distribuitions, the community will be able to participate in the project's aim and directly in specific distribuitions.

<br><br>

<h2 align="center">Design preview</h3>

Here are some designed scripts that will work eventually:

```
let v in Integers. [~ v is an integer ~]

v := 0. [~ v is now 0 ~]

v := 1. [~ v is now 1 ~]


let `Is v zero?` in Booleans. [~ `Is v zero?` is a boolean ~]

`Is v zero?` := true if v = 0, [~ `Is v zero` is true if v = 0 ~]
                else false.    [~ `Is v zero is false if v /= 0` ~]
```

```
let v in Integers. [~ v is an integer ~]

v := [~ Put some value in v ~].

let w in Integers. [~ w is an integer ~]

w := 0 if v < 0,
     1 if (v >= 0) and (v < 5),
     2 if (v >= 5) and (v < 10),
     else 3.
[~ w is 0 is v < 0, 1 if 0 <= v < 5, 2 if 5 <= v < 10 and 3 is v > 0 ~]
```

```
let ispair in Functions. [~ ispair is a function ~]

ispair(x) := x mod 2 = 0.
[~ is the same as ~]
ispair := lbd x : x mod 2 = 0.
```

<br><br>

<h2 align="center">Instalation and use</h2>

The instalation process is unavailable, but the software can be experimented by cloning the repository with git: 
```
git clone https://github.com/Science52101/EidosLogos.git
```

For interpreting some code, use the script `elog.py` at `src` like
```
cd <EidosLogos path>/src
python ./elog.py open <ELog file path> fulldebug
```
Where `<EidosLogos path>` is the path for the repo's directory and `<ELog file path>` is the path for the file with the code to interpret.
