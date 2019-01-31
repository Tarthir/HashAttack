import HashAttack as ha
import sys
old_std = sys.stdout
h = ha.HashAttack()

print("Starting test")
sys.stdout = open('8bits75trials.txt', 'w')
h.run_test(75, 8)
sys.stdout = old_std
print("Test complete\n")

print("Starting test")
sys.stdout = open('10bits75trials.txt', 'w')
h.run_test(75, 10)
sys.stdout = old_std
print("Test complete\n")

print("Starting test")
sys.stdout = open('16bits75trials.txt', 'w')
h.run_test(75, 16)
sys.stdout = old_std
print("Test complete\n")

print("Starting test")
sys.stdout = open('18bits75trials.txt', 'w')
h.run_test(75, 18)
sys.stdout = old_std
print("Test complete\n")

print("Starting test")
sys.stdout = open('20bits75trials.txt', 'w')
h.run_test(75, 20)
sys.stdout = old_std
print("Test complete")
