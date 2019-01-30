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
        i = ((bit_num - needed_bits) // 8) if needed_bits != 0 else 0
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
        return self.byte_arr_to_int(bt_arr, i)

    # TODO average this all out for final output
    def run_trials(self, trials, bits_wanted):
        counter = 0
        while trials > 0:
            lorem = secrets.randbelow(1000000) + counter
            answer = self.compute_sha1(str(lorem), bits_wanted)
            loops = 0
            while True:
                counter += 1
                if answer == self.compute_sha1(str(lorem + counter), bits_wanted):
                    print("Got it! Found a collision with answer %d in %d steps" % (answer, loops))
                    break
                loops += 1
            trials -= 1


    def byte_arr_to_int(self, bt_arr, idx):
        return int.from_bytes(bt_arr[0:idx + 1], byteorder='big', signed=False)


#lorem = 'Hello. My name is Inigo Montoya. You killed my father. Prepare to die.'
trials = int(sys.argv[1])
bits_wanted = int(sys.argv[2])
ha = HashAttack()
ha.run_trials(trials, bits_wanted)


