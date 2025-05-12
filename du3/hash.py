import sys

# Hash function
def custom_hash(text, mod_value):
    result = 0
    for idx, char in enumerate(text):
        char_value = 31 if char == ' ' else ord(char) - 96
        result += char_value * (32 ** idx)
    return result % mod_value


# Node of hash table
class Item:
    def __init__(self, key):
        self.key = key
        self.count = 1


# Hash table with linear probing and dynamic expansion
class HashMap:
    def __init__(self, capacity=11):
        self.size = 0
        self.initial_capacity = capacity
        self.slots = [None] * capacity

    def __load_factor(self):
        return self.size / len(self.slots)

    def __resize(self, new_capacity):
        old_data = self.slots
        self.slots = [None] * new_capacity
        self.size = 0

        for element in old_data:
            if element and element.key:
                position = self.add(element.key)
                self.slots[position].count = element.count

    def add(self, key):
        pos = custom_hash(key, len(self.slots))
        start_pos = pos
        attempts = len(self.slots)

        while attempts > 0:
            if self.slots[pos] is None:
                self.slots[pos] = Item(key)
                self.size += 1
                break
            elif self.slots[pos].key == key:
                self.slots[pos].count += 1
                break
            elif self.slots[pos].key is None:
                found = self.find(key)
                if found != -1:
                    self.slots[found].count += 1
                    break
                else:
                    self.slots[pos] = Item(key)
                    self.size += 1
                    break

            pos = (pos + 1) % len(self.slots)
            attempts -= 1

        if self.__load_factor() >= 0.7:
            self.__resize(len(self.slots) * 2)
            return self.find(key)

        return pos

    def find(self, key):
        pos = custom_hash(key, len(self.slots))
        attempts = len(self.slots)

        while attempts > 0:
            node = self.slots[pos]
            if node is None:
                return -1
            if node.key == key:
                return pos

            pos = (pos + 1) % len(self.slots)
            attempts -= 1

        return -1

    def remove(self, key):
        pos = self.find(key)
        if pos == -1:
            return -1

        self.slots[pos].count -= 1
        if self.slots[pos].count == 0:
            self.size -= 1
            self.slots[pos].key = None

        if self.__load_factor() <= 0.3:
            new_capacity = len(self.slots) // 2
            if new_capacity >= self.initial_capacity:
                self.__resize(new_capacity)
            return self.find(key)

        return pos


# Command Manager
class CommandProcessor:
    initialized = False
    active_command = None
    active_person = None
    hash_maps = {}
    names = {
        1: "Mirek",
        2: "Jarka",
        3: "Jindra",
        4: "Rychlonozka",
        5: "Cervenacek"
    }

    def __initialize(self):
        if self.initialized:
            return

        for i in range(1, 6):
            self.hash_maps[i] = HashMap()

        self.initialized = True

    def __process_i(self, params):
        if self.initialized:
            return

        for i in range(len(params)):
            self.hash_maps[i + 1] = HashMap(int(params[i]))

        for j in range(len(params) + 1, 6):
            self.hash_maps[j] = HashMap()

        self.initialized = True

    def __command_a(self):
        self.active_command = 'a'
        self.active_person = None

    def __command_c(self, person_id):
        if person_id not in range(1, 6):
            sys.stderr.write("Error: Chybny vstup!\n")
            return
        self.active_command = 'c'
        self.active_person = person_id

    def __command_p(self):
        if self.active_person is None:
            sys.stderr.write("Error: Chybny vstup!\n")
            return
        self.active_command = 'p'
        person_name = self.names[self.active_person]
        current_map = self.hash_maps[self.active_person]
        sys.stdout.write(f"{person_name}\n\t{len(current_map.slots)} {current_map.size}\n")

    def __command_d(self):
        if self.active_person is None:
            sys.stderr.write("Error: Chybny vstup!\n")
            return
        self.active_command = 'd'

    def run(self):
        while True:
            try:
                line = input().strip()
                if line == '':
                    break

                if not self.initialized:
                    if line.startswith("#i"):
                        args = line.split()
                        if args[0] != "#i":
                            sys.stderr.write("Error: Chybny vstup!\n")
                            continue
                        self.__process_i(args[1:])
                        continue
                    else:
                        self.__initialize()

                if line.startswith('#'):
                    parts = line.split()
                    if len(parts[0]) != 2:
                        sys.stderr.write("Error: Chybny vstup!\n")
                        continue

                    cmd = parts[0][1]
                    if cmd == 'a':
                        self.__command_a()
                    elif cmd == 'p':
                        self.__command_p()
                    elif cmd == 'd':
                        self.__command_d()
                    elif cmd.isdigit():
                        self.__command_c(int(cmd))
                    else:
                        sys.stderr.write("Error: Chybny vstup!\n")
                    continue

                if self.active_command == 'a':
                    for hmap in self.hash_maps.values():
                        hmap.add(line)
                elif self.active_command == 'p':
                    hmap = self.hash_maps[self.active_person]
                    pos = hmap.find(line)
                    if pos == -1:
                        sys.stdout.write(f"\t{line} -1 0\n")
                    else:
                        sys.stdout.write(f"\t{line} {pos} {hmap.slots[pos].count}\n")
                elif self.active_command == 'd':
                    self.hash_maps[self.active_person].remove(line)

            except EOFError:
                break


if __name__ == "__main__":
    processor = CommandProcessor()
    processor.run()
