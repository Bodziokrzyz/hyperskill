def depict_status(table):
    print('''
    ---------
    | {} {} {} |
    | {} {} {} |
    | {} {} {} |
    ---------
    '''.format(*table))


table = list(' ' * 9)
combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
depict_status(table)

while True:
    x, y = input('Enter the coordinates: ').split()

    if not (x.isdigit() and y.isdigit()):
        print('You should enter numbers!')
    elif not (int(x) in [1, 2, 3] and int(y) in [1, 2, 3]):
        print('Coordinates should be from 1 to 3!')
    elif table[int(x) - int(y) * 3 + 8] != ' ':
        print('This cell is occupied! Choose another one!')
    else:
        table[int(x) - int(y) * 3 + 8] = 'X' if table.count('X') + table.count('O') & 1 else 'O'
        depict_status(table)

    if any(table[comb[0]] == 'X' and table[comb[1]] == 'X' and table[comb[2]] == 'X' for comb in combinations):
        print('X wins')
        break
    elif any(table[comb[0]] == 'O' and table[comb[1]] == 'O' and table[comb[2]] == 'O' for comb in combinations):
        print('O wins')
        break
    elif table.count('X') + table.count('O') == 9:
        print('Draw')
        break
