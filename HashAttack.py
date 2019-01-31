import hashlib
import sys

# assumpt for report: outputs are evenly distributed in the output space
import secrets


class HashAttack:

    def __init__(self):
        super().__init__()
        self.trials = 0
        self.bits_wanted = 0

    def compute_sha1(self, inpt, bit_num):
        h = hashlib.sha1()
        h.update(inpt.encode('utf-8'))
        bt_arr = bytearray(h.digest())
        #bit_counter = 0
        needed_bits = bit_num % 8
        i = ((bit_num - needed_bits) // 8) # if needed_bits != 0 else 0
        if needed_bits == 0:
            return self.byte_arr_to_int(bt_arr, i)
        # get rid of the 'ob'
        b = bin(bt_arr[i])[2:]
        # pad if needed
        if len(b) < 8:
            b = "".zfill(8 - len(b)) + b
        # grab the number of bits we need out of the byte
        b = b[:needed_bits]
        #print(bt_arr[i])
        # pad with zeroes and convert the binary string to an int
        if len(b) < 8:
            # replace old int with new
            bt_arr[i] = int(b + "".zfill(8 - len(b)), 2)
        #print(bt_arr[i])
        # return only the bits asked for
        return self.byte_arr_to_int(bt_arr, i + 1)

    def run_trials(self, method):
        print("Testing %s with %d bits wanted and %d trials:\n" % (method.__name__, self.bits_wanted, self.trials))
        total_loops = 0
        tr = self.trials
        while tr > 0:
            total_loops += method()
            tr -= 1
        avg_steps = (2**(self.bits_wanted // 2)) if method.__name__ is self.collision_attack.__name__ else (2**self.bits_wanted)
        print("Math says this should of taken %d steps" % avg_steps)
        print("We got an average of %d steps" % (total_loops // self.trials))
        print("\n\n")


    def byte_arr_to_int(self, bt_arr, idx):
        return int.from_bytes(bt_arr[0:idx], byteorder='big', signed=False)

    def pre_image_attack(self):
        counter = 0
        lorem = secrets.randbelow(1000000) + counter
        answer = self.compute_sha1(str(lorem), self.bits_wanted)
        loops = 0
        while True:
            counter += 1
            if answer == self.compute_sha1(str(lorem + counter), self.bits_wanted):
                #print("Got it! Pre-image attack complete with answer %d in %d steps" % (answer, loops))
                #print("The original message was %d compared to %d" % (lorem, lorem + counter))
                return loops
            loops += 1

    def collision_attack(self):
        loops, counter = 0, 0
        dct = {}
        while True:
            lorem = secrets.randbelow(1000000) + counter
            answer = self.compute_sha1(str(lorem + counter), self.bits_wanted)
            if answer in dct.keys():
                #print("Got it! Collision attack complete with answer %d in %d steps" % (answer, loops))
                #print("The original message was %d compared to %d" % (dct[answer], lorem + counter))
                return loops
            dct[answer] = lorem
            counter += 1
            loops += 1

    def run_test(self, trials=None, bits_wanted=None):
        try:
            if trials is None:
                self.trials = int(sys.argv[1])
                if bits_wanted is None:
                    self.bits_wanted = int(sys.argv[2])
            else:
                self.trials = trials
                self.bits_wanted = bits_wanted

        except IOError or IndexError as err:
            sys.stderr.write('HashAttack ERROR: %s\n' % str(err))
            exit(1)
        self.run_trials(self.pre_image_attack)
        self.run_trials(self.collision_attack)
