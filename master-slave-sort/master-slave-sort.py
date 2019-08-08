'''
Problem:
Multiple slaves are served by a single master. Each slave can only communicate with the master.
If each slave has an input array, come up with an algorithm to merge all the input arrays into one large sorted array
and write back the result to the individual slaves. The solution should have an O(L) space complexity
in the master where L = number of slaves.

Solution:
For this problem, I will be using an array of size L in the master where each index in the array corresponds to
individual slaves. Here are the steps to this solution:
1. Individually sort the slave input arrays
2. The next step is to merge all these sorted arrays
3. Initialize an array of size L in the master
4. Find the minimum of each slave input, and send that to the master array in the correct slave index
5. Find the minimum of the master array (final_min), and this can be appended to our final sorted array
6. Move final_min to slave output array
7. Now, figure out which slave corresponded to final_min, and update the master array with next element from this slave
8. Repeat steps 5, 6 and 7. Keep filling the slave output arrays till all of them are filled

Author:
Prashanth Palaniappan
'''

import sys
import random


class Slave:
    def __init__(self, input_val):
        self.input_array = input_val
        self.output_array = []
        self.array_size = len(self.input_array)


class Master:
    def __init__(self, num_slaves):
        self.min_array = [sys.maxsize] * num_slaves

    def receive_min_from_slave(self, min_num, slave_index):
        self.min_array[slave_index] = min_num

    def compute_and_send_new_min_to_slave(self):
        target_min = sys.maxsize
        target_min_index = sys.maxsize
        for i in range(len(self.min_array)):
            if self.min_array[i] < target_min:
                target_min = self.min_array[i]
                target_min_index = i
        return target_min, target_min_index


def generate_slaves():
    number_of_slaves = int(input('\n Enter the number of slaves : '))
    list_of_slaves = []
    for i in range(number_of_slaves):
        slave_array_size = random.randint(0, 10)
        input_val = []
        for j in range(slave_array_size):
            input_val.append(random.randint(1, 100))
        new_slave = Slave(input_val)
        print('\n Slave ' + str(i) + ' input array : ' + str(new_slave.input_array))
        list_of_slaves.append(new_slave)
    return list_of_slaves


def generate_master(number_of_slaves):
    return Master(number_of_slaves)


def individual_slave_sort(list_of_slaves):
    for slave in list_of_slaves:
        # reverse sort so that we can use the list as a stack and keep popping the least value
        slave.input_array.sort(reverse=True)


def mergesort_slaves_using_master(list_of_slaves, master):
    # send minimum from each slave to master along with the slave index
    for slave_index, slave in enumerate(list_of_slaves):
        if slave.input_array: # this is to check for empty list; if empty, we will send int_max value
            master.receive_min_from_slave(slave.input_array.pop(), slave_index)
        else:
            master.receive_min_from_slave(sys.maxsize, slave_index)

    # find the last slave and keep a loop going until all the slave output arrays are filled
    last_slave = list_of_slaves[-1]
    while len(last_slave.output_array) < last_slave.array_size:
        # compute final_min value from the master array, and also note down the slave that had this value
        min_val, min_slave_index = master.compute_and_send_new_min_to_slave()
        min_slave = list_of_slaves[min_slave_index]

        # push the final_min value to the slave output array
        for slave in list_of_slaves:
            if len(slave.output_array) < slave.array_size:
                slave.output_array.append(min_val)
                break

        # pop the next value of the slave that had final_min value
        if min_slave.input_array:
            master.receive_min_from_slave(min_slave.input_array.pop(), min_slave_index)
        else:
            master.receive_min_from_slave(sys.maxsize, min_slave_index)


def print_slave_output(list_of_slaves):
    print('\n ===== Result after sorting ===== ')
    for slave_index, slave in enumerate(list_of_slaves):
        print('\n Slave ' + str(slave_index) + ' output array : ' + str(slave.output_array))


def main():
    # Generate slaves and master
    list_of_slaves = generate_slaves()
    number_of_slaves = len(list_of_slaves)
    master = generate_master(number_of_slaves)
    # sort individual slave inputs
    individual_slave_sort(list_of_slaves)
    # merge sorted arrays using master
    mergesort_slaves_using_master(list_of_slaves, master)
    # print final result
    print_slave_output(list_of_slaves)


if __name__ == "__main__":
    main()
