import os

from game import MasterMind, Color

colorf = '\x1b[{}m▇▇\x1b[0m'

color_escape_map = {
    Color.RED: colorf.format(31),
    Color.ORANGE: colorf.format(33),
    Color.YELLOW: colorf.format(93),
    Color.GREEN: colorf.format(32),
    Color.BLUE: colorf.format(34),
    Color.PURPLE: colorf.format(35),
}

game: MasterMind
message: str


def draw():
    print('Answer is:')
    print(draw_colors(game.thought))
    if game.history:
        print('History:')
        for h in game.history:
            print(draw_colors(h.colors), f'{h.correct_color}:{h.correct_position}')
    print()
    print(draw_colors(game.current))
    if message:
        print(f'\n\x1b[41;97mError:\x1b[0m', message)


def draw_colors(colors: 'list[Color]'):
    return ' '.join(color_escape_map[c] for c in colors)


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    global game, message
    game = MasterMind()
    message = ''
    print('Colors are numbered from 1-6. 1 means red and 6 means violet.')
    try:
        while not game.won:
            draw()
            message = ''
            user_input = input('Enter "<pos> <color_number>" or "done": ')
            if user_input.casefold() == 'done' or not user_input:
                game.commit()
            else:
                position, _, color = user_input.partition(' ')
                try:
                    position = int(position)
                    color = int(color)
                    assert position in range(1, 5)
                    assert color in range(1, 7)
                except (ValueError, AssertionError):
                    message = 'invalid input'
                else:
                    game.select_color(position - 1, Color._value2member_map_[color])
            cls()
        print('You won!')

    except (KeyboardInterrupt, OSError):
        pass


if __name__ == '__main__':
    main()
