import os
import subprocess

file_path = "C:/Yuvan/Studies/Fourth_sem/ser517/apache-jena-3.14.0/bin/riot --validate "
root_dir = os.path.abspath('..')
root_dir = root_dir.replace('\\', '/')
output_path = root_dir + '/data/'


def parse_file(file_name):
    command = (file_path + output_path + file_name).split()
    filePath = output_path + file_name
    # output = run_command(command)

    #Mocking the run_command function
    error_line_nos = []
    with open(filePath, "r") as input:
        for lineno, line in enumerate(input):
            if 'Error' in line:
                error_line_nos.append(lineno)
                break

    if len(error_line_nos) == 0:
        return

    with open(filePath, "r") as f:
        lines = f.readlines()

    with open(filePath, "w") as f:
        for lineno, line in enumerate(lines):
            if lineno not in error_line_nos: #if not error line number write into file
                f.write(line)

    parse_file(file_name)
    print("Parsing done")


def run_command(command):
    file_output = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
    return iter(file_output.stdout.readline, b'')


if __name__ == '__main__':

    for filename in os.listdir(output_path):
        parse_file(filename)
        break
