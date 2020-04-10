import subprocess

commands = {
    "stop_server": 'screen -ls | grep "Fuseki" | cut -d. -f1 | awk "{print $1}" | xargs kill',
    "start_server": "screen -d -m -S Fuseki bash -c 'cd ~/fuseki/apache-jena-fuseki-3.14.0 && java -jar fuseki-server.jar'"
}


def run_command(command):
    file_output = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
    return iter(file_output.stdout.readline, b'')


def restart():
    for output in run_command("sh restart.sh".split()):
        print(str(output))


if __name__ == '__main__':
    restart()


