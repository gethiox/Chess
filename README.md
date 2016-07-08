Jak użyć?

chess.py [--help] (-f | -n | -a | -h <ip> | -j <ip>) [-p <port>]
         [-s ./stockfish]

Skrypt można uruchomić w jednym z trzech trybów:
- cpu vs cpu (-a, --auto)
- human vs cpu (-n, --normal)
- human vs human (-f, --alone)

z czego tylko ostatni nie potrzebuje do działania silnika szachowego,
którego ścieżkę należy wskazać parametrem -s
Polecany silnik to stockfish - http://stockfishchess.org/

To dość prymitywny system gry, większą funkcjonalnosć można osiagnać używając
modułu w konsoli. Wielkie litery oznaczają bierki białe, małe natomiast bierki czarne.

**Opis gry w konsoli**

`>>> from chess import *`
`>>> game = Chess()`
`>>> game.new_game()`
`>>> game.show_board(compact=True)`
` r n b q k b n r `
` p p p p p p p p `
` . . . . . . . . `
` . . . . . . . . `
` . . . . . . . . `
` . . . . . . . . `
` P P P P P P P P `
` R N B Q K B N R `

`>>> game.get_position()`
`'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 1 0'`

do wykonywania ruchów służy metoda **`move()`**

`>>> game.move('e2e4')`
`(False, False, False, False, False)`
`>>> game.move('d7d5')`
`(False, False, False, False, False)`
`>>> game.show_board(compact=True)`
` r n b q k b n r `
` p p p . p p p p `
` . . . . . . . . `
` . . . p . . . . `
` . . . . P . . . `
` . . . . . . . . `
` P P P P . P P P `
` R N B Q K B N R `

Widoczna krotka po wykonaniu posunięcia określa status gry na szachownicy,
kolejno:

- koniec gry (szach-mat LUB remis przez powtórzenia LUB remis przez brak mozliwych posunięć).
- szach
- mat
- remis przez powtórzenia
- remis przez brak możliwych posunięć 

Można wyświetlić możliwe posunięcia dla danej figury za pomocą metody **`show_legal_moves()`**
ustawmy sobie więc od razu pozycję kilka posunięć później:
`>>> game.set_position('rnb1kbnr/ppp1pppp/4q3/3p4/4P3/P1N5/1PPP1PPP/R1BQKBNR w KQkq - 4 0')`
`True`
`>>> game.show_board(compact=True)`
` r n b . k b n r `
` p p p . p p p p `
` . . . . q . . . `
` . . . p . . . . `
` . . . . P . . . `
` P . N . . . . . `
` . P P P . P P P `
` R . B Q K B N R `

teraz sprawdźmy jakie możliwe posunięcia ma dostępne pion stojący na `e4`

`>>> game.show_legal_moves('e4', compact=True)`
` r n b . k b n r `
` p p p . p p p p `
` . . . . q . . . `
` . . . p + . . . `
` . . . . P . . . `
` P . N . . . . . `
` . P P P . P P P `
` R . B Q K B N R `

Widzimy że dostępne posunięcie to tylko ruch na przód (oznaczone plusem), biały pion nie może zbić piona czarnego ponieważ w tej pozycji odsłaniałby się na szacha ze strony czarnej królowej stojącej na `e6`
Sprawdźmy zatem skoczka na `c3`

`>>> game.show_legal_moves('c3', compact=True)`
` r n b . k b n r `
` p p p . p p p p `
` . . . . q . . . `
` . + . + . . . . `
` + . . . P . . . `
` P . N . . . . . `
` + P P P + P P P `
` R + B Q K B N R `

Jak nie trudno zauważyć ten już może zbić wspomnianego wcześniej piona i oczywiście poruszyć się również na inne pola.

Pozostałe funkcje:

- **undo()** - cofa pozycję na szachownicy o podaną ilość posunięć
- **redo()** - przywraca pozycję na przód o podaną ilosć posunięć
- **legal_moves()** - zwraca listę dostępnych legalnych posunięć, korzsta z niej metoda **show_legal_moves()**
- **show_board()** - wyświetla bierzącą szachownicę, domyślnie w dużym trybie, w kompaktowym podając jej parametr **compact=True**
- **get_moves_seq()** - zwraca historę wykonanych posunięć
- **get_position()** - zwraca aktualną pozycję w postaci fen\_string
- **set_position()** - ustawia pozycję z fen\_stringu
- **am_i_checked()** - zwraca czy gracz który obecnie jest przy wykonywaniu ruchu jest szachowany
- **am_i_stalemated()**- jw. ale czy zremisowany poprzez repetycję
- **am_i_mated()** - jw. ale czy jest zamatowany
- **am_i_pated()** - jw. ale czy nie ma dostępnych żadnych posunięć

informacje dodatkowa:
warto utworzyć grę z parametrem **auto_show_board=True**, nie trzeba wtedy wyświetlać ręcznie za każdym razem szachownicy (albo ustawić zmienną utworzonej klasy **auto_show_board=True**)
Moduł gry sieciowej nie jest dokończony
