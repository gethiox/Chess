import subprocess


class Engine:
    """
    UCI interface documentation:
    http://wbec-ridderkerk.nl/html/UCIProtocol.html
    """

    def __init__(self, engine_binary_path='./src/helpers/stockfish', ponder=False):
        self.path = engine_binary_path
        self.process = None
        self.playing_color = None
        self.logic_thread = None
        self.sigterm = False
        self.pondering = False
        self.ponder = ponder

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
        self._write('setoption name Threads value 4')
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

    def bestmove(self, fenstring=None, moves_seq=None):
        if fenstring is not None:
            if self.ponder:
                self.stop_ponder()
            self._write('position fen %s' % fenstring)
            self._write('go wtime 5000 btime 5000000')
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
            self._write('go wtime 50000 btime 5000')
            output = self._read()
            while 'bestmove' not in output:
                output = self._read()
            bestmove = output.split()[1]
            if self.ponder:
                self.start_ponder()
        else:
            raise ValueError

        return bestmove