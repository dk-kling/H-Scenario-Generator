import rich
custom_theme = rich.Theme({
    "info": "dim cyan",
    "warn": "yellow",
    "error": "bold red"
})
console = rich.Console(theme=custom_theme)


def warn_log(warn_str):
    console.print(warn_str, style="warn")


def error_log(error_str):
    console.print(error_str, style="error")


def info_log(info_str):
    console.print(info_str, style="info")
