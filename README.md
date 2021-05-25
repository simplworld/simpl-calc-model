# simpl-calc-model - example single-player simulation model service.

## Python Setup (assumes Python 3.6 and simpl-games-api server running)


## Install simpl-calc-model

```shell
$ git clone https://github.com/simplworld/simpl-calc-model.git
$ cd simpl-calc-model
```

## Local Docker Setup

The Simpl API server needs to be started first to create the `simpl` bridge network.

Install [simpl-games-api master](https://github.com/simplworld/simpl-games-api) and run it in 
docker-compose so that it exposes itself as hostname `api` on port `8100`. 

You also need to have a `is_staff=True` user in the simpl-games-api database that
corresponds to the `SIMPL_GAMES_AUTH` setting used here.

After you clone the repo, run:

```bash
$ docker-compose up
```

this will create the Docker image and run it.  The first time you run it it will error
as it can't find the simpl-calc game in the API.

In a separate terminal, create a shell into the simpl-calc-model container by running:

```bash
$ docker-compose run --rm model.backend bash
```

Once you are in the container shell, run this command:

```shell
$ ./manage.py create_default_env
```

You should see this create the 'simpl-calc' game, phases, users, etc.

Exit from the shell then stop and restart the docker container by running these commands: 

```bash
$ exit
$ docker-compose down
$ docker-compose up
```

You should now see a startup log message to the effect of:

```
Game `simpl-calc` installed in 2.063s.
```

This means the simpl-calc-model is able to successfully communicate with the API.

## Local Setup Without Docker

### Create a virtual environment and install Python dependencies

```bash
$ mkvirtualenv simpl-calc-model
$ pip install -r requirements.txt
```

### Run model service

```shell
$ export DJANGO_SETTINGS_MODULE=simpl_calc_model.settings
$ ./manage.py run_modelservice
```

If you need some serious debugging help, the model_service includes the ability to do

```shell
$ ./manage.py run_modelservice --loglevel=debug
```

Which will turn on verbose debugging of the Autobahn/Crossbar daemon to help debug interactions between the browser and model service backend.

### Run model service as 2 processes

1. Get a copy of the currently in use crossbar configuration by running
    `./manage.py run_modelservice --print-config > config.json`
1. Edit `config.json` to remove the entire {"type": "guest", ...} stanza and final line
1. Run crossbar service:    
    `./manage.py run_modelservice --config=./config.json --loglevel info --settings=simpl_calc_model.settings`
1. In a separate terminal, run guest service:    
    `HOSTNAME=localhost PORT=8080 ./manage.py run_guest --settings=simpl_calc_model.settings`


## Run unit tests

```shell
$ pytest
```

## Development commands:

### 1 - To setup up database for simpl-calc development use:

1. Creates the simpl-calc game with one phase (Play) and one role (Calculator).
1. Adds a 'default' run..
1. Adds 1 leader ('leader@calc.edu'/'leader') to the run.
1. Adds 2 players to the run ('s#@calc.edu'/'s#' where # is between 1..2. Each player has a private scenario and period 1.
1. The run is set to 'Play' phase

execute:

```shell
$ ./manage.py create_default_env
```

To make it easier to recreate the default run you can pass the `--reset` option to delete the
default run and recreate it from scratch like this:

```shell
$ ./manage.py create_default_env --reset
```

To create a run with a non-default name, use:

```shell
./manage.py create_default_env -n <name>
```

where:
 **name** is the run name (default is 'default') and the base of player email ids (default is 's')  

### 2 - To submit a decision on a scenario:

```shell
$ ./manage.py submit_decision -s <scenario_id> -d <decision>
```

## Modelservice Profiling

### Run modelservice profiling tests locally

1. Run simpl-games-api modelservice
1. Run simpl-calc-model modelservice

In a separate terminal window,

Create and activate a virtual environment:

```shell
$ mkvirtualenv simpl-calc-model
$ pip install -r requirements.txt
```

Create a test run named 'a' with 2 players named after the run (e.g. run 'a' with players 'a1@div.edu', etc)

```shell
$ ./manage.py create_default_env -n a
```

To run each player test once for each user in the `emails/emails-4.txt` file, run:

```shell
$ profile.sh -m game.profilers -u emails/emails-2.txt -g 1
```

to launch a separate profiling task for each email in the file:

```
./manage.py profile -m game.profilers -g 1 -w 2 --log-level error --user-email a1@div.edu
./manage.py profile -m game.profilers -g 1 -w 2 --log-level error --user-email a2@div.edu
```

Once all tasks complete, message will be printed out indicating how many seconds it took to run all profile tests

Before rerunning the profiling test, recreate the test run:

```shell
$ ./manage.py create_default_env -n a --reset
```

Copyright © 2018 The Wharton School,  The University of Pennsylvania 

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

