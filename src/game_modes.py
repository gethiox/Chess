from src.engine_handler import Engine
from time import sleep
from src.exceptions import *


def human_vs_human(chess, engine_binary_path):
    game = chess(auto_show_board=False)
    game.new_game()
    game.show_board()

    while True:
        status = input_from_human(game)

        if status[0]:
            print_game_end_status(status=status, on_move=game.on_move)
            break

        status = input_from_human(game)

        if status[0]:
            print_game_end_status(status=status, on_move=game.on_move)
            break


def human_vs_cpu(chess, engine_binary_path):
    game = chess(auto_show_board=True)
    e1 = Engine(ponder=True, engine_binary_path=engine_binary_path)
    e1.run_engine()
    game.new_game()

    while True:
        status = input_from_human(game)

        if status[0]:
            print_game_end_status(status=status, on_move=game.on_move)
            break

        status = game.move(e1.bestmove(moves_seq=game.get_moves_seq(), btime=1000, wtime=1000))

        if status[0]:
            print_game_end_status(status=status, on_move=game.on_move)
            break


def cpu_vs_cpu(chess, engine_binary_path):
    game = chess(auto_show_board=True)
    e1 = Engine(ponder=False, engine_binary_path=engine_binary_path, threads=1)
    e1.run_engine()
    e2 = Engine(ponder=False, engine_binary_path=engine_binary_path, threads=1)
    e2.run_engine()
    game.new_game()

    while True:
        status = game.move(e1.bestmove(moves_seq=game.get_moves_seq(), btime=100, wtime=100))

        if status[0]:
            print_game_end_status(status=status, on_move=game.on_move)
            break

        status = game.move(e2.bestmove(moves_seq=game.get_moves_seq(), btime=100, wtime=100))

        if status[0]:
            print_game_end_status(status=status, on_move=game.on_move)
            break


def print_game_end_status(status, on_move):
    if on_move == 'w':
        if status[2]:
            print('game over, black won')
        if status[3]:
            print('stalemate! no legal moves for white!')
        if status[4]:
            print('stalemate! three position repetition by white!')
    elif on_move == 'b':
        if status[2]:
            print('game over, white won')
        if status[3]:
            print('stalemate! no legal moves for black!')
        if status[4]:
            print('stalemate! three position repetition by black!')
    sleep(2)


def input_from_human(game):
    while True:
        if game.on_move == 'w':
            player_str = 'Białe: '
        elif game.on_move == 'b':
            player_str = 'Czarne: '
        try:
            input_stroke = input(player_str)
        except KeyboardInterrupt:
            exit(0)
        if 'exit' in input_stroke:
            exit(0)
        try:
            status = game.move(input_stroke)
        except IllegalMove:
            print('Nieprawidłowe posunięcie!')
            continue
        else:
            if game.on_move == 'w':
                game.show_board(flipped=False)
            elif game.on_move == 'b':
                game.show_board(flipped=True)
            return status
