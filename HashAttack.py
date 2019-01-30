import hashlib
import sys

# assumpt for report: outputs are evenly distributed in the output space
import secrets


class HashAttack():

    def compute_sha1(self, inpt, bit_num):
        h = hashlib.sha1()
        h.update(inpt.encode('utf-8'))
        bt_arr = bytearray(h.digest())
        bit_counter = 0
        needed_bits = bit_num % 8
        i = ((bit_num - needed_bits) // 8) # if needed_bits != 0 else 0
        if needed_bits == 0:
            return self.byte_arr_to_int(bt_arr,i)
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

    # TODO average this all out for final output
    def run_trials(self, trials, bits_wanted, method):
        print("Testing %s with %d bits wanted and %d trials:\n" % (method.__name__, bits_wanted, trials))
        total_loops = 0
        while trials > 0:
            total_loops += method(bits_wanted)
            trials -= 1
        trials = int(sys.argv[1])
        avg_steps = (2**(bits_wanted // 2)) if method.__name__ is self.collision_attack.__name__ else (2**bits_wanted)
        print("Math says this should of taken %d steps" % avg_steps)
        print("We got an average of %d steps" % (total_loops // trials))
        print("\n\n")


    def byte_arr_to_int(self, bt_arr, idx):
        return int.from_bytes(bt_arr[0:idx], byteorder='big', signed=False)

    def pre_image_attack(self, bits_wanted):
        counter = 0
        lorem = secrets.randbelow(1000000) + counter
        answer = self.compute_sha1(str(lorem), bits_wanted)
        loops = 0
        while True:
            counter += 1
            if answer == self.compute_sha1(str(lorem + counter), bits_wanted):
                print("Got it! Pre-image attack complete with answer %d in %d steps" % (answer, loops))
                print("The original message was %d compared to %d" % (lorem, lorem + counter))
                return loops + 1
            loops += 1

    def collision_attack(self, bits_wanted):
        loops, counter = 0, 0
        dct = {}
        while True:
            lorem = secrets.randbelow(1000000) + counter
            answer = self.compute_sha1(str(lorem + counter), bits_wanted)
            if answer in dct.keys():
                #print("Got it! Collision attack complete with answer %d in %d steps" % (answer, loops))
                #print("The original message was %d compared to %d" % (dct[answer], lorem + counter))
                return loops + 1
            dct[answer] = lorem
            counter += 1
            loops += 1


#lorem = 'Hello. My name is Inigo Montoya. You killed my father. Prepare to die.'
trials = int(sys.argv[1])
bits_wanted = int(sys.argv[2])
ha = HashAttack()

ha.run_trials(trials, bits_wanted, ha.pre_image_attack)
ha.run_trials(trials, bits_wanted, ha.collision_attack)


