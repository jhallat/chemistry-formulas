

def composition(value):
    tokens = []
    current_token = ''
    for char in value:
        if char.isdigit() and current_token.isdigit():
            current_token += char
        elif char == char.upper() and len(current_token) > 0:
            tokens += [current_token]
            current_token = char
        else:
            current_token += char
    if len(current_token) > 0:
        tokens += [current_token]

    composition = []
    in_digit = False
    in_element = False
    count = ''
    element = ''
    for token in tokens:
        if (not in_digit) and (not in_element):
            # TODO raise an exception if the first character is a digit
            element += token
            in_element = True
        elif in_digit:
             composition += [(count, element)]
             element = token
             count = ''
             in_digit = False
             in_element = True
        elif in_element:
            if token.isdigit():
                count = token
                in_digit = True
                in_element = False
            else:
                composition += [(count if count else '1', element)]
                element = token
                count=''
    composition += [(count if count else '1', element)]
    return composition







