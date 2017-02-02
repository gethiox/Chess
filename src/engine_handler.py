import subprocess


class Engine:
    """
    UCI interface documentation:
    http://wbec-ridderkerk.nl/html/UCIProtocol.html
    """

    def __init__(self, engine_binary_path='./src/helpers/stockfish', ponder=False, threads=4):
        self.path = engine_binary_path
        self.process = None
        self.playing_color = None
        self.logic_thread = None
        self.sigterm = False
        self.pondering = False
        self.ponder = ponder
        self.threads = threads

    def _read(self):
        line = self.process.stdout.readline().decode()
        if '\n' in line:
            line = line.replace('\n', '')
        return line

    def _write(self, string):
        if '\n' not in string:
            string += '\n'
        self.process.stdin.write(string.encode())
        self.process.stdin.flush()

    def run_engine(self):
        args = [self.path]
        self.process = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        self._write('setoption name Threads value %d' % self.threads)
        self._write('setoption name Hash value 256')
        self._write('setoption name Ponder value true')
        self._write('setoption name MultiPV value 2')
        self._write('ucinewgame')

    def start_ponder(self):
        if not self.pondering:
            self._write('go ponder')
            self.pondering = True

    def stop_ponder(self):
        if self.pondering:
            self._write('stop')
            output = self._read()
            while 'bestmove' not in output:
                output = self._read()
            self.pondering = False

    def bestmove(self, fenstring=None, moves_seq=None, btime=None, wtime=None):
        if fenstring is None and moves_seq is None:
            raise Exception('you need to specify fenstring or move sequence as board state.')

        if isinstance(btime, int) and isinstance(wtime, int):
            go_string = 'go wtime %d btime %d' % (wtime, btime)
        else:
            go_string = 'go'

        if fenstring is not None:
            if self.ponder:
                self.stop_ponder()
            self._write('position fen %s' % fenstring)
            self._write(go_string)
            output = self._read()
            while 'bestmove' not in output:
                output = self._read()
            bestmove = output.split()[1]
            if self.ponder:
                self.start_ponder()
        elif moves_seq is not None:
            if self.ponder:
                self.stop_ponder()
            if len(moves_seq) > 0:
                self._write('position startpos moves %s' % moves_seq)
            else:
                self._write('position startpos')
            self._write(go_string)
            output = self._read()
            while 'bestmove' not in output:
                output = self._read()
            bestmove = output.split()[1]
            if self.ponder:
                self.start_ponder()
        else:
            raise ValueError

        return bestmove