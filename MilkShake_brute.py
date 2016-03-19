
import collections

def return_int_list(str_in):
    return [int(x) for x in str_in.split()]


MilkshakeType = collections.namedtuple('MilkshakeType', 'flavour, malted')


class Customer:
    def __init__(self, str_in, truth_table):
        input_list = return_int_list(str_in)
        self.liked_milkshakes = input_list[0]
        self.milkshake_both = {}
        self.milkshake_malted = None
        self.milkshake_plain = set()
        for i in range(0, self.liked_milkshakes):
            flavour = input_list[(2 * i) + 1] - 1
            is_malted = input_list[2 * i + 2]
            if is_malted:
                self.milkshake_malted = flavour
            else:
                self.milkshake_plain.add(flavour)
            self.milkshake_both[flavour] = is_malted

            truth_table[flavour] = is_malted

    def acceptable_result(self, attempted_flavour):
        for flavour, type in self.milkshake_both.items():
            if attempted_flavour[flavour] == type:
                return True
        return False

    def update_liked(self,liked):
        liked_milkshakes = self.liked_milkshakes
        if self.milkshake_malted is not None:
            liked['malted'][self.liked_milkshakes-1].add(self.milkshake_malted)
            liked_milkshakes -= 1
        if liked_milkshakes > 0:
            liked['plain'][self.liked_milkshakes-1].update(self.milkshake_plain)


class Milkshakes:
    IMPOSSIBLE = "IMPOSSIBLE"

    def __init__(self, file_pointer: open):
        self.number_of_flavours = int(file_pointer.readline())
        self.number_of_customers = int(file_pointer.readline())
        self.truth_table = [[None for i in range(0, self.number_of_flavours)].copy() for j in
                            range(0, self.number_of_customers)]
        self.customer = []
        for i in range(0, self.number_of_customers):
            self.customer.append(Customer(file_pointer.readline()[:-1], self.truth_table[i]))

    def get_result(self):
        my_array = [{0} for i in range(0, self.number_of_flavours)]
        for i_flavour in range(0, self.number_of_flavours):
            for i_customer in range(0, self.number_of_customers):
                type = self.truth_table[i_customer][i_flavour]
                if type == 1:
                    my_array[i_flavour].add(type)

        option_arrays = [[] for i in range(0, self.number_of_flavours + 1)]
        get_list_options(my_array, option_arrays)
        sorted_option_array = []
        for options_by_malted in option_arrays:
            for each_option_array in options_by_malted:
                sorted_option_array.append(each_option_array)
        acceptable_result = self.get_acceptable_results(sorted_option_array)
        if acceptable_result is None:
            return self.IMPOSSIBLE
        else:
            return ' '.join([str(x) for x in acceptable_result])

    def get_acceptable_results(self, option_arrays):
        acceptable_result = None
        malt_count = self.number_of_flavours + 1
        for attempt in option_arrays:

            current_malt_count = len([x for x in attempt if x == 1])
            if current_malt_count >= malt_count:
                continue
            for o_customer in self.customer:
                if not o_customer.acceptable_result(attempt):
                    break
            else:
                malt_count = current_malt_count
                acceptable_result = attempt
        return acceptable_result


def get_list_options(my_array, result, i_min=0, progress=None):
    if progress is None:
        progress = []
    if my_array[i_min] is None:
        my_array[i_min] = {0}
    for options in my_array[i_min]:
        if i_min == len(my_array) - 1:
            final_array = progress + [options]
            current_malt_count = len([x for x in final_array if x == 1])
            result[current_malt_count].append(final_array)
        else:
            get_list_options(my_array, result, i_min + 1, progress[:] + [options])
