import subprocess


class EngineHandler:
    """
    Simple UCI chess engine handler
    http://wbec-ridderkerk.nl/html/UCIProtocol.html
    """

    def __init__(self, path: str, ponder: bool = False, threads: int = 4, hash: int = 256, multi_pv: int = 1):
        """
        :param path: path to binary of UCI chess engine (stockfish is recommended)
        :param ponder: True if pondering on enemy turn is expected
        :param threads: How many threads are sacrificed for the engine
        :param hash: memory size for hash table
        :param multi_pv: MultiPV ¯\_(ツ)_/¯
        """
        self.path = path
        self.process: subprocess.Popen = None
        self.logic_thread = None
        self.__sigterm = False
        self.__pondering = False
        self.__ponder = ponder
        self.__threads = threads
        self.__hash_size = hash
        self.__multi_pv = multi_pv

    def _read(self):
        """Reading data from engine"""
        line = self.process.stdout.readline().decode()
        if '\n' in line:
            line = line.replace('\n', '')
        return line

    def _write(self, string):
        """Write data to engine"""
        if '\n' not in string:
            string += '\n'
        self.process.stdin.write(string.encode())
        self.process.stdin.flush()

    def start_engine(self):
        """Run subprocess and configure """
        args = [self.path]
        self.process = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        self._write('setoption name Threads value %d' % self.__threads)
        self._write('setoption name Hash value %d' % self.__hash_size)
        self._write('setoption name Ponder value %s' % str(self.__ponder).lower())
        self._write('setoption name MultiPV value %d' % self.__multi_pv)
        self._write('ucinewgame')

    def stop_engine(self):
        """Makes sure that subprocess is closed correctly"""
        self._write('quit')
        try:
            self.process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            self.process.terminate()

    def _start_ponder(self):
        if not self.__pondering:
            self._write('go ponder')
            self.__pondering = True

    def _stop_ponder(self):
        if self.__pondering:
            self._write('stop')
            output = self._read()
            while 'bestmove' not in output:
                output = self._read()
            self.__pondering = False

    def best_move(self, fen: str = None, moves_seq: str = None, btime: int = 0, wtime: int = 0):
        """
        Required is at least "fen" or "moves_seq" parameter, "btime" and "wtime" is optional to determine how much
        time left for each side (in miliseconds)
        Note: moves_seq is a preferred way to inform about position because repetition can be avoided if possible
        :param fen: fenstring of game
        :param moves_seq: string of primitive move format (eg. e7e8q) separated by spaces
        :param btime: miliseconds of left time of the black side (optional)
        :param wtime: miliseconds of left time of the white side (optional)
        :return:
        """
        if fen is None and moves_seq is None:
            raise ValueError('you need to specify fenstring or move sequence of the board state.')

        if btime > 0 and wtime > 0:
            go_string = 'go wtime %d btime %d' % (wtime, btime)
        else:
            go_string = 'go'

        if fen is not None:
            if self.__ponder:
                self._stop_ponder()
            self._write('position fen %s' % fen)
            self._write(go_string)
            output = self._read()
            while 'bestmove' not in output:
                output = self._read()
            bestmove = output.split()[1]
            if self.__ponder:
                self._start_ponder()
            return bestmove

        elif moves_seq is not None:
            if self.__ponder:
                self._stop_ponder()
            if len(moves_seq) > 0:
                self._write('position startpos moves %s' % moves_seq)
            else:
                self._write('position startpos')
            self._write(go_string)
            output = self._read()
            while 'bestmove' not in output:
                output = self._read()
            bestmove = output.split()[1]
            if self.__ponder:
                self._start_ponder()
            return bestmove
