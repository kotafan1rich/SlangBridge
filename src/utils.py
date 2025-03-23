from ai.api import Api


def get_definition(input, model, mode):
    return Api().tarnslate(input, model, not bool(mode))


def split_on_strings(text, max_length=45):
    words = text.split()
    ret = ""
    current_line = ""

    for word in words:
        if len(current_line) + len(word) < max_length:
            current_line += f"{word} "
        else:
            ret += current_line.rstrip() + "\n"
            current_line = f"{word} "

    if current_line:
        ret += current_line.rstrip()

    return ret
