# Sublime FormatX

ForamtX helps you format your code with whatever program you specify.

Let's format!

## Usage

FormatX registers a `formatx_format` command, you can bind it to a shortcut like this.

```json
{
  "keys": ["ctrl+;"],
  "command": "formatx_format",
}
```

By default, there is no formatter configured, so nothing will happen if you run the `formatx_format` command.

Let's say you want to format your Go code with `goimports`,

- click the top left "Sublime Text" menu -> Preferences -> Package Settings -> FormatX -> Settings.
- type this

```json
{
  "scope": {
    "source.go": ["~/Documents/Go/bin/goimports"],
  }
}
```

You need to use an array to hold the command and its args, FormatX will expand `~` to `$file` for you.

All formatters must receive input from `stdin` and print output to `stdout`.

If something error happens, FormatX will show the error in the bottom status bar.

Sublime use `scope` to identify every programming language, you can use `super/ctrl + alt + p` to get the scope of current file.

It would be tedious to manually run the command every time. ForamtX supports a config called `auto_format_dirs`. When you save a file, if it belongs to any of these directories (including the sub directory), FormatX will do the format automatically.

## Sample Config

This is my person config.

```json
{
  "scope": {
    "source.go": ["~/Documents/Go/bin/goimports"],
    "source.c": ["/usr/local/bin/clang-format", "--assume-filename=/Users/cj/test.c"],
    "source.js": ["~/.fnm/aliases/default/bin/prettier_d", "--stdin", "--stdin-path", "$file"],
    "source.ts": ["~/.fnm/aliases/default/bin/prettier_d", "--stdin", "--stdin-path", "$file"],
  },
  "auto_format_dirs": [
    "~/Desktop/Lab",
  ],
}
```

I use [prettier_d](https://github.com/cj1128/prettier_d) to format JS code because it's fast (under 100ms).

## Change Log

### 0.1.0

First version.


