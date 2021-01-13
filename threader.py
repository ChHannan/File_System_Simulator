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
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args) -> list:
        Thread.join(self, *args)
        return self._return


def thread_function(input_commands: list[InputCommand], input_structure: list, connection_pointer):
    MUTEX_LOCK.acquire()
    for i in input_commands:
        if i.command_name == 'create':
            file_name = str(i.file_name.strip("\n"))
            connection_pointer.sendall(str.encode(create(file_name, input_structure)))

        elif i.command_name == 'read':
            read_data = read(i.file_name.strip('\n'), input_structure)
            if len(read_data) == 0:
                connection_pointer.sendall(str.encode('File is empty'))
            else:
                connection_pointer.sendall(str.encode(read_data))

        elif i.command_name == 'read_from':
            file_name = i.file_name.strip('\n')
            starting_index = int(i.arguments[0])
            reading_size = int(i.arguments[1].strip('\n'))
            connection_pointer.sendall(str.encode(read_from(file_name, starting_index, reading_size, input_structure)))

        elif i.command_name == 'write':
            file_name = i.file_name.strip('\n')
            read_data = str(i.arguments[0].strip('\n').strip("\""))
            write(file_name, read_data, input_structure, connection_pointer)

        elif i.command_name == 'write_at':
            index = int(i.arguments[0])
            read_data = str(i.arguments[1].strip("\n").strip("\""))
            input_structure = write_at(i.file_name, index, read_data, input_structure, connection_pointer)
        elif i.command_name == 'move':
            from_index = int(i.arguments[0])
            to_index = int(i.arguments[1])
            size = int(i.arguments[2].strip('\n'))
            input_structure = move_within_file(i.file_name, from_index, to_index, size, input_structure,
                                               connection_pointer)

        elif i.command_name == 'delete':
            file_name = str(i.file_name.strip("\n"))
            connection_pointer.sendall(delete(file_name, input_structure))

        elif i.command_name == 'truncate':
            size = int(i.arguments[0].strip('\n'))
            input_structure = truncate(i.file_name, size, input_structure, connection_pointer)

        elif i.command_name == 'rename':
            previous_name = str(i.file_name.strip('\n'))
            new_name = str(i.arguments[0].strip('\n'))
            connection_pointer.sendall(str.encode(rename(previous_name, new_name, input_structure)))

        elif i.command_name == 'get_directory_size':
            connection_pointer.sendall(str.encode(str(get_structure_size(input_structure))))

        elif i.command_name.strip('\n') == 'show':
            print_memory_map(input_structure, connection_pointer)

        else:
            connection_pointer.sendall(str.encode(f'Invalid arguments: {i.command_name}, {i.file_name}, {i.arguments}'))
    MUTEX_LOCK.release()
    return input_structure
