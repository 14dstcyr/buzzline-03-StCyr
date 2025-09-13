# buzzline-03-StCyr

Streaming data does not have to be simple text.
Many of us are familiar with streaming video content and audio (e.g. music) files.

Streaming data can be structured (e.g. csv files) or
semi-structured (e.g. json data).

We'll work with two different types of data, and so we'll use two different Kafka topic names.
See [.env](.env).

## First, Use Tools from Module 1 and 2

Before starting, ensure you have completed the setup tasks in <https://github.com/denisecase/buzzline-01-case> and <https://github.com/denisecase/buzzline-02-case> first.
**Python 3.11 is required.**

## Second, Copy This Example Project & Rename

1. Once the tools are installed, copy/fork this project into your GitHub account
   and create your own version of this project to run and experiment with.
2. Name it `buzzline-03-yourname` where yourname is something unique to you.

Additional information about our standard professional Python project workflow is available at
<https://github.com/denisecase/pro-analytics-01>.

Use your README.md to record your workflow and commands.

---

## Task 0. If Windows, Start WSL

- Be sure you have completed the installation of WSL as shown in [https://github.com/denisecase/pro-analytics-01/blob/main/01-machine-setup/03c-windows-install-python-git-vscode.md](https://github.com/denisecase/pro-analytics-01/blob/main/01-machine-setup/03c-windows-install-python-git-vscode.md).

- We can keep working in **Windows VS Code** for editing, Git, and GitHub.
- When you need to run Kafka or Python commands, just open a **WSL terminal** from VS Code.

Launch WSL. Open a PowerShell terminal in VS Code. Run the following command:

```powershell
wsl
```

You should now be in a Linux shell (prompt shows something like `username@DESKTOP:.../repo-name$`).

Do **all** steps related to starting Kafka in this WSL window. 

---

## Task 1. Start Kafka (using WSL if Windows)

In P2, you downloaded, installed, configured a local Kafka service.
Before starting, run a short prep script to ensure Kafka has a persistent data directory and meta.properties set up. This step works on WSL, macOS, and Linux - be sure you have the $ prompt and you are in the root project folder.

1. Make sure the script is executable.
2. Run the shell script to set up Kafka.
3. Cd (change directory) to the kafka directory.
4. Start the Kafka server in the foreground.
5. Keep this terminal open - Kafka will run here
6. Watch for "started (kafka.server.KafkaServer)" message

```bash
chmod +x scripts/prepare_kafka.sh
scripts/prepare_kafka.sh
cd ~/kafka
bin/kafka-server-start.sh config/kraft/server.properties
```

**Keep this terminal open!** Kafka is running and needs to stay active.

For detailed instructions, see [SETUP_KAFKA](https://github.com/denisecase/buzzline-02-case/blob/main/SETUP_KAFKA.md) from Project 2. 

---

## Task 2. Manage Local Project Virtual Environment

Open your project in VS Code and use the commands for your operating system to:

1. Create a Python virtual environment
2. Activate the virtual environment
3. Upgrade pip
4. Install from requirements.txt

#### Windows

Open a new PowerShell terminal in VS Code (Terminal / New Terminal / PowerShell).

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip wheel setuptools
py -m pip install --upgrade -r requirements.txt
```

If you get execution policy error, run this first:
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

#### Mac / Linux

Open a new terminal in VS Code (Terminal / New Terminal)

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade -r requirements.txt
```

---

## Task 3. Start a Kafka JSON Producer

This producer generates earthquake JSON messages (tremors and aftershocks).

Before starting the JSON Producer:

1. Open a new terminal in your project root.
2. Activate your .venv.
3. Run the command for your operating system (see below).

What did we name the topic used with JSON data?
Hint: See the producer code and .env (json_stcyr).

#### Windows:

```
.venv\Scripts\activate
py producers/json_producer_stcyr.py
```

#### Mac/Linux:

```zsh
source .venv/bin/activate
python3 producers/json_producer_stcyr.py
```

## Task 4. Start a Kafka JSON Consumer

This consumer processes earthquake JSON messages and raises alerts on aftershocks/magnitude events.

Before starting the JSON Consumer:

1. Open a new terminal.
2. Activate your .venv.
3. Run the command for your operating system (see below).

What did we name the topic used with JSON data?

Hint: See the consumer code and .env  (json_stcyr).

#### Windows:

```shell
.venv\Scripts\activate
py consumers/json_consumer_stcyr.py
```

#### Mac/Linux:

```zsh
source .venv/bin/activate
python3 consumers/json_consumer_stcyr.py
```

## Task 5. Start a Kafka CSV Producer

This producer generates <u>seismic magnitude readings</u> and sends them to Kafka.
It can run in <u>two modes</u>:

### Option 1 — Synthetic Mode (default):
*No CSV file is required.
*Automatically generates magnitude readings with tremors and spikes.

What did we name the topic used with csv data?

Hint: See the producer code and .env.

#### Windows:

```shell
.venv\Scripts\activate
py producers/csv_producer_stcyr.py
```

#### Mac/Linux (or WSL):

```zsh
source .venv/bin/activate
python3 producers/csv_producer_stcyr.py
```

### Option 2 — File Mode (data/seismic.csv):

Replays seismic data from the included file: data/seismic.csv

Each row has two fields: timestamp and magnitude.

<u>Sends each row to Kafka as JSON</u>.

The file simulates:

*Small tremors (2.0–3.0)

*A major quake (5.0–6.0)

*Aftershocks (3.5–4.5)

*Return to calm (2.0–2.8)

<u>Example rows from data/seismic.csv</u>:

```
timestamp,magnitude
2025-01-01 00:00:00,2.5
2025-01-01 00:10:00,5.6   <-- major quake
2025-01-01 00:11:00,5.3   <-- aftershock
2025-01-01 00:18:00,2.4   <-- calm
```

#### Windows:

```shell
.venv\Scripts\activate
set CSV_SOURCE_FILE=data\seismic.csv
py producers/csv_producer_stcyr.py
```

#### Mac/Linux (or WSL):

```zsh
source .venv/bin/activate
CSV_SOURCE_FILE=data/seismic.csv python3 producers/csv_producer_stcyr.py
```

What did we name the topic used with CSV data?
Hint: See the producer code and .env (csv_stcyr).

## Task 6. Start a Kafka CSV Consumer

This consumer monitors seismic magnitudes, calculates rolling averages, and raises alerts on aftershocks or quakes ≥ 5.0.

Before starting the CSV Consumer:

1. Open a new terminal (yes, another one).
2. Activate your .venv.
3. Run the command for your operating system (see below).

What did we name the topic used with CSV data?
Hint: See the consumer code and .env (csv_stcyr).

#### Windows:

```shell
.venv\Scripts\activate
py consumers/csv_consumer_stcyr.py
```

#### Mac/Linux (or WSL):

```zsh
source .venv/bin/activate
python3 consumers/csv_consumer_stcyr.py
```

---

## How To Stop a Continuous Process

To kill the terminal, hit CTRL c (hold both CTRL key and c key down at the same time).

## About the Earthquake Simulation (CSV Example)

The CSV producer simulates seismic readings. Each record has a timestamp and magnitude value.

- Tremors are small magnitudes (2.0–4.0).
- Major quakes occur when magnitude ≥ 5.0.
- Aftershocks appear as sudden spikes following a quake.

The consumer:
- Maintains a rolling average of the last 5 readings.
- Raises **ALERT** if magnitude ≥ 5.0.
- Raises **ALERT** if sudden change Δ ≥ 1.0 (aftershock detection).


## Later Work Sessions

When resuming work on this project:

1. Open the project repository folder in VS Code. 
2. Start the Kafka service (use WSL if Windows) and keep the terminal running. 
3. Activate your local project virtual environment (.venv) in your OS-specific terminal.
4. Run `git pull` to get any changes made from the remote repo (on GitHub).

## After Making Useful Changes

1. Git add everything to source control (`git add .`)
2. Git commit with a -m message.
3. Git push to origin main.

```shell
git add .
git commit -m "your message in quotes"
git push -u origin main
```

## Save Space

To save disk space, you can delete the .venv folder when not actively working on this project.
You can always recreate it, activate it, and reinstall the necessary packages later.
Managing Python virtual environments is a valuable skill.

## License

This project is licensed under the MIT License as an example project.
You are encouraged to fork, copy, explore, and modify the code as you like.
See the [LICENSE](LICENSE.txt) file for more.
