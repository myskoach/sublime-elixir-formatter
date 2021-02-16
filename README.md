# sublime-ex-formatter

Sublime Text 3 plugin for formatting Elixir files on save via `mix format`.

1. Formats the file on save using test env
2. Maintains position in buffer
3. Goes to line on syntax error
4. Considers project configs

## Caveat Emptor

This code is a fork from [this gist](https://gist.github.com/Fire-Dragon-DoL/df4d33a6f836fc295451d94991fcbaf5) which, in turn, is a fork from [this unmantained repo](https://github.com/karolsluszniak/elixir-formatter-sublime). It is currently "maintained" by non-python devs.

Use with care.

## Installation

### 1. Package Control

Look for ExFormatter.

### 2. Through git

1. Go to your packages folder (in Sublime: Preferences > Browse Packages...).
2. Clone the repo `git clone https://github.com/myskoach/sublime-ex-formatter.git`

### 3. Manually

Download this repo as an ExFormatter folder and save it into your packages (in Sublime: Preferences > Browse Packages...).

## Contributing

We need:

1. Tests
2. Some config (specifically, which env to use on `mix format`)

PRs welcome.
