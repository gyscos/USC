import readline

class Completer(object):
    def __init__(self, options, entry):
        self.options = options
        self.entry = entry
        self.candidates = []

    def add_list(self, name, content = None):
        if content is None:
            content = {}
        self.options[name] = content

    def add_to_list(self, name, content):
        if isinstance(content, dict):
            self.options[name].update(content)
        elif isinstance(content, set):
            for elmt in content:
                self.add_to_list(name, elmt)
        else:
            self.add_to_list(name, {content:[]})

    def getCandidateList(self, words, expected):

        if not expected:
            return []
        if not words:
            return list(self.options[expected[0]])

        if not words[0] in self.options[expected[0]]:
            return []

        try:
            nexts = self.options[expected[0]][words[0]]
            return self.getCandidateList(words[1:], nexts + expected[1:])
        except:
            return self.getCandidateList(words[1:], expected[1:])

    def getCandidatesFromIndex(self, index) :
        return [op['name'] for op in self.options[index]]

    def getCandidatesFromWords(self, words):
        index = self.entry
        try:
            for word in words:
                index = [op['index']
                            for op in self.options[index]
                            if op['name'] == word ][0]
            return self.getCandidatesFromIndex(index)
        except:
            return []

    def complete(self, text, state):
        reponse = None

        if state == 0:
            origline = readline.get_line_buffer()
            begin = readline.get_begidx()
            end = readline.get_endidx()

            being_completed = origline[begin:end]
            words = origline.split()

            try:
                if begin == end:
                    candidates = self.getCandidateList(words, [self.entry])
                else:
                    candidates = self.getCandidateList(words[0:-1], [self.entry])

                if being_completed:
                    self.candidates = [ w+' ' for w in candidates
                                        if w.startswith(being_completed) ]
                else:
                    self.candidates = candidates

            except err:
                self.candidates = []

        try:
            response = self.candidates[state]
        except IndexError:
            reponse = None

        return response

"""

Exemples :

com = Completer({
    "entry" : { "list" : ["names"], "stop":[] },
    "names" : { "bob" : [], "jack" : [] }

    }, "entry")

readline.read_init_file("usc.rc")
readline.set_completer(com.complete)

s = input("> ")

"""
