from threading import Thread, Lock

from file import *
from input_command import *

MUTEX_LOCK = Lock()


class Threader(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        MUTEX_LOCK.acquire()

        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
        MUTEX_LOCK.release()

    def join(self, *args) -> list:
        Thread.join(self, *args)
        return self._return


def thread_function(input_commands: list[InputCommand], input_structure: list, file_pointer):
    for i in input_structure:
        print("Fun")
        print(i.data)
    for i in input_commands:
        if i.command_name == 'create':
            file_name = str(i.file_name.strip("\n"))
            print(create(file_name, input_structure), file=file_pointer)

        elif i.command_name == 'read':
            read_data = read(i.file_name.strip('\n'), input_structure)
            if len(read_data) == 0:
                print('File is empty', file=file_pointer)
            else:
                print(read_data, file=file_pointer)

        elif i.command_name == 'read_from':
            file_name = i.file_name.strip('\n')
            starting_index = int(i.arguments[0])
            reading_size = int(i.arguments[1].strip('\n'))
            print(read_from(file_name, starting_index, reading_size, input_structure), file=file_pointer)

        elif i.command_name == 'write':
            file_name = i.file_name.strip('\n')
            read_data = str(i.arguments[0].strip('\n').strip("\""))
            write(file_name, read_data, input_structure, file_pointer)

        elif i.command_name == 'write_at':
            index = int(i.arguments[0])
            read_data = str(i.arguments[1].strip("\n").strip("\""))
            input_structure = write_at(i.file_name, index, read_data, input_structure, file_pointer)
        elif i.command_name == 'move':
            from_index = int(i.arguments[0])
            to_index = int(i.arguments[1])
            size = int(i.arguments[2].strip('\n'))
            input_structure = move_within_file(i.file_name, from_index, to_index, size, input_structure, file_pointer)

        elif i.command_name == 'delete':
            file_name = str(i.file_name.strip("\n"))
            print(delete(file_name, input_structure), file=file_pointer)

        elif i.command_name == 'truncate':
            size = int(i.arguments[0].strip('\n'))
            input_structure = truncate(i.file_name, size, input_structure, file_pointer)

        elif i.command_name == 'rename':
            previous_name = str(i.file_name.strip('\n'))
            new_name = str(i.arguments[0].strip('\n'))
            print(rename(previous_name, new_name, input_structure), file=file_pointer)

        elif i.command_name == 'get_directory_size':
            print(get_structure_size(input_structure), file=file_pointer)

        elif i.command_name.strip('\n') == 'show_memory_map':
            print_memory_map(input_structure, file_pointer)

        else:
            print(f'Invalid arguments: {i.command_name}, {i.file_name}, {i.arguments}', file=file_pointer)
    file_pointer.close()
    return input_structure


def read_input_file(file_number: int):
    input_commands_list = []
    input_file = open(f'input_thread{file_number}.txt', 'r')
    lines = input_file.readlines()
    for i in lines:
        commands = i.split(", ")
        command = InputCommand()
        for index, j in enumerate(commands):
            if index == 0:
                command.command_name = j
            elif index == 1:
                command.file_name = j
            else:
                j = j.strip('\n')
                command.arguments.append(j)
        input_commands_list.append(command)
    input_file.close()
    return input_commands_list


def get_user_input(input_structure):
    threads = []
    no_of_threads = int(input('Enter the no. of threads to be run: '))
    for i in range(1, no_of_threads + 1):
        output_file = open(f'output_thread{i}.txt', 'w')
        input_commands_list = read_input_file(i)
        thread = Threader(target=thread_function, args=(input_commands_list, input_structure, output_file))
        threads.append(thread)
        thread.start()
    for j in threads:
        thread_output = j.join()
        if isinstance(thread_output, list):
            input_structure = thread_output
        for i in input_structure:
            print("----")
            print(i.data)
    return input_structure
