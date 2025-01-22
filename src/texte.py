def set_prompt(sub):
    chaine = ""
    for col in sub.values():
        for key, value in col.items():
            chaine += f"{value},"
    return chaine