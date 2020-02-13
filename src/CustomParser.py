import os
import subprocess

file_path = "C:/Yuvan/Studies/Fourth_sem/ser517/apache-jena-3.14.0/bin/riot --validate "

root_dir = os.path.abspath('..')
root_dir = root_dir.replace('\\', '/')
output_path = root_dir + '/data/'


def parse_file(file_name):
    command = (file_path + output_path + file_name).split()
    filePath = output_path + file_name
    output = run_command(command)

    if 'Error' in output:
        #get the line number of the errors
        print("line number")
    else:
        return


    with open(filePath, "r") as input:
        with open(filePath, "w") as output:
            for lineno, line in enumerate(input):
                if lineno != "Error line number": #if not error line number write into file
                    output.write(line)

    parse_file(file_name)

    print(output)


def run_command(command):
    file_output = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
    return iter(file_output.stdout.readline, b'')


if __name__ == '__main__':

    for filename in os.listdir(output_path):
        parse_file(filename)
        break
