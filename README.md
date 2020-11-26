# NetworkDiffBot
 
## How to Run

### 1. Clone Repository

```shell script
git clone https://github.com/hykilpikonna/NetworkDiffBot
cd NetworkDiffBot
```

### 2. Install Python Dependencies

(If you don't have Python 3.9 installed already, search about how to install Python 3.9 first)

```shell script
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

### 3. Create Start Script

Create File:

```shell script
nano start.sh
```

Script:

```shell script
export PYTHONPATH=PYTHONPATH:$pwd
export TG_TOKEN="<Your token here>"
python3 ./src/bot.py
# Then use Ctrl+X -> Y to save
```

Make it an executable:

```shell script
chmod +x start.sh
```

### 4. Run Script

```shell script
./start.sh
```
