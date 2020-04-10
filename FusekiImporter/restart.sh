#!/usr/bin/env bash
screen -ls | grep "Fuseki" | cut -d. -f1 | awk '{print $1}' | xargs kill
screen -d -m -S Fuseki bash -c 'cd ~/../../dev/fuseki-volume/apache-jena-fuseki-3.14.0 && java -jar fuseki-server.jar'