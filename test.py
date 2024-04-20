# alphabet = ['|', '+', '=']
# idx = -1
# input_str = ''

# def read_char():
#     global idx
#     idx += 1
#     if idx < len(input_str):
#         c = input_str[idx]
#     else:
#         return ''
#     if not c in alphabet:
#         raise Exception('Error!Illegal character!')
#     return c

# def undo_read():
#     global idx
#     if idx < len(input_str):
#         idx -= 1


# def execute():
#     global input_str
#     input_str = input()
#     s = '1'
#     stack = []
#     while True:
#         if s == '1':
#             c = read_char()
#             if c == '|':
#                 stack.append('[')
#                 print('|', end='')
#                 continue
#             if c == '+':
#                 print('+', end='')
#                 s = '2'
#                 continue
#             raise Exception('Error!Input not accepted!')
#         if s == '2':
#             c = read_char()
#             if c == '|':
#                 stack.append('[')
#                 print('|', end='')
#                 continue
#             if c == '=':
#                 print('=', end='')
#                 s = '3'
#                 continue
#             raise Exception('Error!Input not accepted!')
#         if s == '3':
#             c = read_char()
#             if len(stack) > 0 and stack[-1] == '[':
#                 undo_read()
#                 stack.pop()
#                 print('|', end='')
#                 continue
#             if c != '':
#                 raise Exception('Error!Input not accepted!')
#             return


# if __name__ == '__main__':
#     execute()


# s = '123'
# try:
#     print(s.index(' '))
# except:
#     print(s)