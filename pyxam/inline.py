#!/usr/bin/env python3
# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Module inline
This code is loaded into the start of every template file prior to weaving.
"""
import random
import config


class pyxam:

    number = int('{number}')
    version = '{version}'.strip()
    student_first_name = '{student_first_name}'.strip()
    student_last_name = '{student_last_name}'.strip()
    student_name = '{student_name}'.strip()
    student_number = '{student_number}'.strip()
    wildcard = None
    table = None

    def import_questions(*paths):
        import fileutil
        for path in paths:
            path = fileutil.find_file(path)
            print(fileutil.read(path))

    def args(args):
        import options
        import shlex
        options.load_options(shlex.split(args))

    def shuffle(*choices):
        choices = list(choices)
        random.shuffle(choices)
        for choice in choices:
            print(choice)

    def numerical(solution, tolerance=0, percent=False):
        import options
        if percent:
            tolerance = solution * (tolerance / 100.0)
        if options.state.format() == 'moodle':
            print(':pyxam.numerical<text>{}</text><tolerance>{}</tolerance><tolerancetype>1</tolerancetype>'.format(solution, tolerance))
        elif tolerance == 0:
            print(config.numerical_format_no_tolerance.format(solution=str(solution)))
        else:
            print(config.numerical_format.format(
                solution=str(solution),
                tolerance=tolerance,
                lower=float(solution) - tolerance,
                upper=float(solution) + tolerance
            ))

    def calculated(equation, tolerance=0, percent=False):
        import re
        import options
        solution = eval(re.sub(r'\{([^}]*)\}', r'\1', equation))
        if percent:
            tolerance = solution * (tolerance / 100.0)
        if options.state.format() == 'moodle':
            print(':pyxam.calculated<text>{}</text><tolerance>{}</tolerance><tolerancetype>1</tolerancetype> \
            <correctanswerformat>1</correctanswerformat><correctanswerlength>2</correctanswerlength>'.format(equation, tolerance))
        if tolerance == 0:
            print(config.calculated_format_no_tolerance.format(solution=solution))
            return
        print(config.calculated_format.format(
            solution=str(solution),
            tolerance=tolerance,
            lower=float(solution) - tolerance,
            upper=float(solution) + tolerance
        ))

    def dataset(*wildcards):
        import options
        if options.state.format() == 'moodle':
            print('<dataset_definitions>')
            for wildcard in wildcards:
                wildcard.name = [ k for k,v in globals().items() if v is wildcard][0]
                print('<dataset_definition><status><text>private</text></status><name><text>{}</text></name> \
                <type>calculatedsimple</type><distribution><text>uniform</text></distribution> \
                <maximum><text>{}</text></maximum><minimum><text>{}</text></minimum> \
                <decimals><text>{}</text></decimals><itemcount>{}</itemcount><dataset_items>'.format(
                    wildcard.name, wildcard.max, wildcard.min, wildcard.decimals, len(wildcard.set)
                ))
                for number, value in enumerate(wildcard.set):
                    print('<dataset_item><number>{}</number><value>{}</value></dataset_item>'.format(number + 1, value))
                print('</dataset_items><number_of_items>{}</number_of_items></dataset_definition>'.format(len(wildcard.set)))
            print('</dataset_definitions>')

    def categorize(course, category):
        import options
        if options.state.format() == 'moodle':
            print('<question type="category"><category><text>{}/{}</text></category></question>'.format(course, category))


class Wildcard:

    def __init__(self, name='', function=None, args=[], wildcard=None, min=None, max=None, set=None, n=pyxam.number, decimals=0):
        self.name = str(name)
        self.decimals = decimals
        if function is not None:
            def call(i):
                new_args = [arg.set[i] for arg in args]
                return function(*new_args)
            set = [call(i) for i in range(len(args[0].set))]
        if wildcard is not None:
            self.set = wildcard.set
            self.min = wildcard.min
            self.max = wildcard.max
            self.decimals = wildcard.decimals
        elif set is not None and len(set) > 0:
            self.set = set
            self.min = self.set[0]
            self.max = self.set[0]
            for item in self.set:
                if item < self.min:
                    self.min = item
                if item > self.max:
                    self.max = item
                if '.' in str(item) and len(str(item).split('.')[1]) > decimals:
                    self.decimals = len(str(item).split('.')[1])
        else:
            self.set = []
            self.min = min
            self.max = max
            for item in range(n if n > 0 else 1):
                i = random.randint(min, max)
                self.set.append(random.randint(min, max) + round(random.random(), decimals))

    def __add__(self, other):
        if isinstance(other, Wildcard):
            return Wildcard(set=[a + b for a, b in zip(self.set, other.set)])
        else:
            return Wildcard(set=[a + other for a in self.set])

    def __sub__(self, other):
        if isinstance(other, Wildcard):
            return Wildcard(set=[a - b for a, b in zip(self.set, other.set)])
        else:
            return Wildcard(set=[a - other for a in self.set])

    def __mul__(self, other):
        if isinstance(other, Wildcard):
            return Wildcard(set=[a * b for a, b in zip(self.set, other.set)])
        else:
            return Wildcard(set=[a * other for a in self.set])

    def __truediv__(self, other):
        if isinstance(other, Wildcard):
            return Wildcard(set=[a / b for a, b in zip(self.set, other.set)])
        else:
            return Wildcard(set=[a / other for a in self.set])

    def __floordiv__(self, other):
        if isinstance(other, Wildcard):
            return Wildcard(set=[a // b for a, b in zip(self.set, other.set)])
        else:
            return Wildcard(set=[a // other for a in self.set])

    def __mod__(self, other):
        if isinstance(other, Wildcard):
            return Wildcard(set=[a % b for a, b in zip(self.set, other.set)])
        else:
            return Wildcard(set=[a % other for a in self.set])

    def __divmod__(self, other):
        if isinstance(other, Wildcard):
            return Wildcard(set=[divmod(a, b) for a, b in zip(self.set, other.set)])
        else:
            return Wildcard(set=[divmod(a, other) for a in self.set])

    def __pow__(self, other):
        if isinstance(other, Wildcard):
            return Wildcard(set=[a ** b for a, b in zip(self.set, other.set)])
        else:
            return Wildcard(set=[a ** other for a in self.set])

    def __and__(self, other):
        if isinstance(other, Wildcard):
            return Wildcard(set=[a and b for a, b in zip(self.set, other.set)])
        else:
            return Wildcard(set=[a and other for a in self.set])

    def __xor__(self, other):
        if isinstance(other, Wildcard):
            return Wildcard(set=[a ^ b for a, b in zip(self.set, other.set)])
        else:
            return Wildcard(set=[a ^ other for a in self.set])

    def __or__(self, other):
        if isinstance(other, Wildcard):
            return Wildcard(set=[a or b for a, b in zip(self.set, other.set)])
        else:
            return Wildcard(set=[a or other for a in self.set])

    def __lshift__(self, other):
        if isinstance(other, Wildcard):
            return Wildcard(set=[a << b for a, b in zip(self.set, other.set)])
        else:
            return Wildcard(set=[a << other for a in self.set])

    def __rshift__(self, other):
        if isinstance(other, Wildcard):
            return Wildcard(set=[a >> b for a, b in zip(self.set, other.set)])
        else:
            return Wildcard(set=[a >> other for a in self.set])

    def __abs__(self):
        return Wildcard(set=[abs(a) for a in self.set])

    def __pos__(self):
        return Wildcard(set=[a for a in self.set])

    def __neg__(self):
        return Wildcard(set=[-a for a in self.set])

    def __invert__(self):
        return Wildcard(set=[~a for a in self.set])

    def __complex__(self):
        return Wildcard(set=[complex(a) for a in self.set])

    def __round__(self, n=None):
        return Wildcard(set=[round(a, n) for a in self.set])

    def __eq__(self, other):
        return Wildcard(set=[a == b for a, b in zip(self.set, other.set)])

    def __ne__(self, other):
        return Wildcard(set=[a != b for a, b in zip(self.set, other.set)])

    def __lt__(self, other):
        return Wildcard(set=[a < b for a, b in zip(self.set, other.set)])

    def __gt__(self, other):
        return Wildcard(set=[a > b for a, b in zip(self.set, other.set)])

    def __le__(self, other):
        return Wildcard(set=[a <= b for a, b in zip(self.set, other.set)])

    def __ge__(self, other):
        return Wildcard(set=[a >= b for a, b in zip(self.set, other.set)])

    def __bool__(self):
        return all(self.set)

    def __repr__(self):
        return str(self.set[pyxam.number % len(self.set)])

    def __str__(self):
        return self.__repr__()

    def __float__(self):
        return float(str(self))

    def __int__(self):
        return int(str(self))

    def __hash__(self):
        """
        **PURE EVIL**
        By placing a wildcard in a dictionary printing that dictionary will call the hash function of that wildcard. We
        will print the value we want and then prevent the next print statement from occurring meaning we are the only
        ones to print.
        :return: 0
        """
        # Save stdout
        import sys
        stdout = sys.stdout.write

        # Restore stdout
        def _(*args, **kwargs):
            sys.stdout.write = stdout

        import options
        # Check if we are exporting to moodle, if we are print our name from the global namespace otherwise print self
        print('{'+[ k for k,v in globals().items() if v is self][0]+'}' if options.state.format() == 'moodle' else self)
        # Make the next print call be to anon function that will restore the print call and return 0 to satisfy the hash
        sys.stdout.write = _
        return 0

    def val(self):
        return float(self)


class Table:

    def __init__(self, css_class):
        self.css_class = css_class
        self.data = []

    def row(self, row):
        self.data.append((row, False))

    def header(self, row):
        self.data.append((row, True))

    def show(self):
        print('<table class="{}">'.format(self.css_class))
        for row, header in self.data:
            print('<tr>')
            for col in row:
                print('<th>{}</th>'.format(col) if header else '<td>{}</td>'.format(col))
            print('</tr>')
        print('</table>')


# Set random to be seeded by version
random.seed(pyxam.number + config.seed)
# Set the wildcard and Table alias
pyxam.wildcard = Wildcard
pyxam.table = Table