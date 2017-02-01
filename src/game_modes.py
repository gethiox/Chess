from src.engine_handler import Engine
from time import sleep


def human_vs_human(chess, engine_binary_path):
    game = chess(auto_show_board=False)
    game.new_game()
    game.show_board()

    while True:
        while True:
            try:
                status = game.move(input('[Białe] Podaj ruch: '))
            except KeyboardInterrupt:
                print()
                exit(0)
            except:
                print('nieprawidłowe posunięcie')
                continue
            else:
                break

        game.show_board(flipped=True)

        if status[0]:
            if game.on_move == 'w':
                if status[2]:
                    print('game over, black won')
                if status[3]:
                    print('stalemate! no legal moves for white!')
                if status[4]:
                    print('stalemate! three position repetition by white!')
            elif game.on_move == 'b':
                if status[2]:
                    print('game over, white won')
                if status[3]:
                    print('stalemate! no legal moves for black!')
                if status[4]:
                    print('stalemate! three position repetition by black!')
            sleep(2)
            break

        while True:
            try:
                status = game.move(input('[czarne] Podaj ruch: '))
            except KeyboardInterrupt:
                print()
                exit(0)
            except:
                print('nieprawidłowe posunięcie')
                continue
            else:
                break

        game.show_board()

        if status[0]:
            if game.on_move == 'w':
                if status[2]:
                    print('game over, black won')
                if status[3]:
                    print('stalemate! no legal moves for white!')
                if status[4]:
                    print('stalemate! three position repetition by white!')
            elif game.on_move == 'b':
                if status[2]:
                    print('game over, white won')
                if status[3]:
                    print('stalemate! no legal moves for black!')
                if status[4]:
                    print('stalemate! three position repetition by black!')
            sleep(2)
            break


def human_vs_cpu(chess, engine_binary_path):
    game = chess(auto_show_board=True)
    e1 = Engine(ponder=True, engine_binary_path=engine_binary_path)
    e1.run_engine()
    game.new_game()

    while True:
        while True:
            try:
                status = game.move(input('Podaj ruch: '))
            except KeyboardInterrupt:
                print()
                exit(0)
            except:
                print('nieprawidłowe posunięcie')
                continue
            else:
                break

        if status[0]:
            if game.on_move == 'w':
                if status[2]:
                    print('game over, black won')
                if status[3]:
                    print('stalemate! no legal moves for white!')
                if status[4]:
                    print('stalemate! three position repetition by white!')
            elif game.on_move == 'b':
                if status[2]:
                    print('game over, white won')
                if status[3]:
                    print('stalemate! no legal moves for black!')
                if status[4]:
                    print('stalemate! three position repetition by black!')
            sleep(2)
            break
        status = game.move(e1.bestmove(moves_seq=game.get_moves_seq()))
        if status[0]:
            if game.on_move == 'w':
                if status[2]:
                    print('game over, black won')
                if status[3]:
                    print('stalemate! no legal moves for white!')
                if status[4]:
                    print('stalemate! three position repetition by white!')
            elif game.on_move == 'b':
                if status[2]:
                    print('game over, white won')
                if status[3]:
                    print('stalemate! no legal moves for black!')
                if status[4]:
                    print('stalemate! three position repetition by black!')
            sleep(2)
            break


def cpu_vs_cpu(chess, engine_binary_path):
    game = chess(auto_show_board=True)
    e1 = Engine(ponder=True, engine_binary_path=engine_binary_path)
    e1.run_engine()
    e2 = Engine(ponder=False, engine_binary_path=engine_binary_path)
    e2.run_engine()
    game.new_game()

    while True:
        for i in range(300):
            status = game.move(e1.bestmove(moves_seq=game.get_moves_seq()))
            if status[0]:
                if game.on_move == 'w':
                    if status[2]:
                        print('game over, black won')
                    if status[3]:
                        print('stalemate! no legal moves for white!')
                    if status[4]:
                        print('stalemate! three position repetition by white!')
                elif game.on_move == 'b':
                    if status[2]:
                        print('game over, white won')
                    if status[3]:
                        print('stalemate! no legal moves for black!')
                    if status[4]:
                        print('stalemate! three position repetition by black!')
                sleep(2)
                break
            status = game.move(e2.bestmove(moves_seq=game.get_moves_seq()))
            if status[0]:
                if game.on_move == 'w':
                    if status[2]:
                        print('game over, black won')
                    if status[3]:
                        print('stalemate! no legal moves for white!')
                    if status[4]:
                        print('stalemate! three position repetition by white!')
                elif game.on_move == 'b':
                    if status[2]:
                        print('game over, white won')
                    if status[3]:
                        print('stalemate! no legal moves for black!')
                    if status[4]:
                        print('stalemate! three position repetition by black!')
                sleep(2)
                break
        game.new_game()