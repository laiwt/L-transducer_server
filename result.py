alphabet = []
idx = -1
input_str = ''

def read_char():
    global idx
    idx += 1
    if idx < len(input_str):
        c = input_str[idx]
    else:
        return ''
    if not c in alphabet:
        raise Exception('Error!Illegal character!')
    return c

def undo_read():
    global idx
    if idx < len(input_str):
        idx -= 1

def execute():
    global input_str
    input_str = input()
    s = '1'
    while True:
        if s == '1':
            c = read_char()
            undo_read()
            s = '3'
        if s == '3':
            c = read_char()
            if c != '':
                raise Exception('Error!Input not accepted!')
            return


if __name__ == '__main__':
    try:
        execute()
    except Exception as e:
        print('\n' + str(e))