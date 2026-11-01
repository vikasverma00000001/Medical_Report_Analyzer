import re


def clean_text(text):

    if not text:
        return ""

    # Unicode normalize
    text = text.encode(
        "utf-8",
        "ignore"
    ).decode("utf-8")

    # Tabs remove
    text = text.replace("\t", " ")

    # Multiple spaces
    text = re.sub(
        r" +",
        " ",
        text
    )

    # Blank lines remove
    text = re.sub(
        r"\n\s*\n",
        "\n",
        text
    )

    # Line trim
    lines = []

    for line in text.split("\n"):

        line = line.strip()

        if line != "":
            lines.append(line)

    text = "\n".join(lines)

    return text.strip()