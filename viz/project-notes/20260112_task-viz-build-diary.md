# [[2026-03-01]]

## DONE tasks.(fix)running viz


- [ ] (bugfix) MR data source file update in `ExaGO/viz/src/module_casedata.js#L3` to `"../data/case_ACTIVSg10k.json"` to skip running a whole python script (the file already exists in ExaGO `develop` branch)
The error was with this file [`ExaGO/viz/src/module_casedata.js#L3`](https://github.com/pnnl/ExaGO/blob/develop/viz/src/module_casedata.js#L3) instruction importing data source file which does not exist:
```javascript
import inputcasedata from "../data/opflowout-70K.json" with { type: "json" };
```
It can be replaced with existing [`ExaGO/viz/data/case_ACTIVSg10k.json`](https://github.com/pnnl/ExaGO/blob/develop/viz/data/case_ACTIVSg10k.json) data source file from [ExaGO/viz/data](https://github.com/pnnl/ExaGO/tree/develop/viz/data) folder:
```javascript
import inputcasedata from "../data/case_ACTIVSg10k.json" with { type: "json" };
```
 
 [ExaGO/viz/geninputfile.py](https://github.com/pnnl/ExaGO/blob/develop/viz/geninputfile.py) file actually does the same thing with [this line](https://github.com/pnnl/ExaGO/blob/develop/viz/geninputfile.py#L40)
```python
...
    f.write('import inputcasedata from "../data/' + basefile + '" with { type: "json" };\n')
...
```
where `basefile` is `data/case_ACTIVSg10k.json` as instructed in terminal command flow docs:
```bash
ExaGO/viz/backend$ cd ..
ExaGO/viz$ python3 geninputfile.py data/case_ACTIVSg10k.json
```
So it actually does not make much sense to run the script to change a file name for using mock data purposes. Of course data pipeline building settings should be automated later on.
# [[2026-02-10]]
- [x] (fix) run viz  [created:: 2026-02-09]  [due:: 2026-02-11]  [completion:: 2026-03-01]
	- [[#DONE tasks.(fix)running viz|RESULT]]
	- [x] check original mock database  [completion:: 2026-03-01]
	- [x] check integration with map  [completion:: 2026-03-01]
	  - if it is right -> issue on that
	    - looks like when I `git pull --rebase upstream develop` it removed generated datafiles and venv. Reinstall.
```bash
➜  viz git:(develop) ✗ yarn start
yarn run v1.22.22
$ yarn dev
$ vite

  VITE v7.3.1  ready in 208 msß

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
9:58:27 PM [vite] (client) Pre-transform error: Failed to resolve import "../data/opflowout-70K.json" from "src/module_casedata.js". Does the file exist?
  Plugin: vite:import-analysis
  File: /Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/src/module_casedata.js:3:27
  1  |  // ExaGo Viz Input File
  2  |  
  3  |  import inputcasedata from "../data/opflowout-70K.json" with { type: "json" };
     |                             ^
  4  |  
  5  |  export default {
Sourcemap for "/Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/node_modules/react-widgets/styles.css" points to missing source files
9:58:28 PM [vite] Internal server error: Failed to resolve import "../data/opflowout-70K.json" from "src/module_casedata.js". Does the file exist?
  Plugin: vite:import-analysis
  File: /Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/src/module_casedata.js:3:27
  1  |  // ExaGo Viz Input File
  2  |  
  3  |  import inputcasedata from "../data/opflowout-70K.json" with { type: "json" };
     |                             ^
  4  |  
  5  |  export default {
      at TransformPluginContext._formatLog (file:///Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/node_modules/vite/dist/node/chunks/config.js:28999:43)
      at TransformPluginContext.error (file:///Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/node_modules/vite/dist/node/chunks/config.js:28996:14)
      at normalizeUrl (file:///Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/node_modules/vite/dist/node/chunks/config.js:27119:18)
      at async file:///Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/node_modules/vite/dist/node/chunks/config.js:27177:32
      at async Promise.all (index 0)
      at async TransformPluginContext.transform (file:///Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/node_modules/vite/dist/node/chunks/config.js:27145:4)
      at async EnvironmentPluginContainer.transform (file:///Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/node_modules/vite/dist/node/chunks/config.js:28797:14)
      at async loadAndTransform (file:///Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/node_modules/vite/dist/node/chunks/config.js:22670:26)
      at async viteTransformMiddleware (file:///Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/node_modules/vite/dist/node/chunks/config.js:24542:20)

```
# [[2026-01-17]]
- [x] (Vladimir) build Viz  [completion:: 2026-01-17]

# Launch full-scale app `DONE`
- [x] launch full app  [created:: 2026-01-12]  [completion:: 2026-01-17]

## PROBLEM: ChatGrid 5000 server port error
created [[2026-01-16]]
### SUGGESTED solution
- [ ] (issue) port picking strategy [created:: 2026-01-18]
	- REQUIREMENTS: front <-> backend synching 
	- IDEAS: check if a port is free script/tool, vite proxy, environment variable)

### READY solution: pick another port (5001)
#### `app.jsx``L:685-698`
- [x] (build) pick another port on `app.jsx:694`(5001, 3000, 8000,8080,5050)  and sync with backend.`server.py:44`
  - [DONE](https://github.com/Walter462/ExaGO/commit/abacd47a0bf4fde939f132a3da834ae7564206d4)

```javascript
  async function fetchMyData(params) {
    try {
	...
      const response = await fetch(`http://localhost:5001/data`, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(postData),
      });
	...
```

#### `server.py`
- [x] (build) pick another port on `server.py:44` (5001, 3000, 8000,8080,5050) side and sync with frontend `jsx.app:694`
  - [DONE](https://github.com/Walter462/ExaGO/commit/abacd47a0bf4fde939f132a3da834ae7564206d4)

```python
...
# Running app
if __name__ == '__main__':
    # Run on all interfaces to accept both localhost and 127.0.0.1
    app.run(host='0.0.0.0', port=5001, debug=True)
    
```

### ANALYSIS
#### Check `http://localhost:5000`

>[!CAUTION] 
> MacOs uses this port: `AirPlay Receiver`.

```bash
➜  viz git:(my-cool-feature-dev) ✗ lsof -i :5000
COMMAND   PID      USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
ControlCe 971 walternzd   10u  IPv4 0xaab6826cb96c2976      0t0  TCP *:commplex-main (LISTEN)
ControlCe 971 walternzd   11u  IPv6 0xc55ab3aebc3157ce      0t0  TCP *:commplex-main (LISTEN)
```

- `ControlCe` = Control Center
- `commplex-main` = the service name for TCP port 5000
- The port is bound on both IPv4 and IPv6
- It is LISTENING locally

#### What port 5000 is used for on macOS

On modern macOS versions (Monterey → Sonoma → Sequoia):
- Port **5000** is used internally by **Control Center**
- It supports **local IPC (inter-process communication)** between:
    - Control Center
    - System UI components (Wi-Fi, AirPlay, Display, Focus modes, etc.)
- It is **not a public web server**
- It is **not exposed externally** unless you explicitly open it via firewall rules

#### Why it can be confusing

- Developers often use **port 5000** for:
    - Flask
    - FastAPI
    - Local dev servers
- macOS doesn’t “reserve” it formally, but **Control Center grabs it early**, so:
	- Your app may fail to bind to port 5000
	- `lsof` shows it as already in use

#### Code analysis

>[!IMPORTANT] 
> check `http://localhost:5000` and server funcionality

According to the browser console (see below) the execution stops at this code in `App.jsx, line 694` responsible for calling a server: [const response = await fetch(`http://localhost:5000/data`, {](https://github.com/Walter462/ExaGO/blob/16ed29d9604d52682f9c9eb24fb71a046104d4e8/viz/src/App.jsx#L694)

---

This error handler is inside this function:
[async function fetchMyData(params) {](https://github.com/Walter462/ExaGO/blob/16ed29d9604d52682f9c9eb24fb71a046104d4e8/viz/src/App.jsx#L685)

---

 Responding phrase comes from that App.jsx code:
 [} catch (error) {
      return "Sorry I didn't find the answer to your question. Please try to rephrase it or provide more details.";
    }](https://github.com/Walter462/ExaGO/blob/16ed29d9604d52682f9c9eb24fb71a046104d4e8/viz/src/App.jsx#L758-L760)

### DESCRIPTION 

Problem Logs and ScreenShots

>[!CAUTION]- error
> ![[Screenshot 2026-01-17 at 13.26.19.png|600]]
<img src="./attachments/Screenshot 2026-01-17 at 13.26.19.png" width="600" />


---
>[!NOTE]- Initial state
>![[Screenshot 2026-01-17 at 13.23.40.png|600]]

<img src="./attachments/Screenshot 2026-01-17 at 13.23.40.png" width="600" />

#  Build and Start backend and frontend modules `DONE`
- [x] Build and Start backend and frontend modules (separately) [dependsOn:: 96wrgc,owk922]  [completion:: 2026-01-15]

Next:
- check full-scale FrontEnd<->BackeEnd

## Backend `DONE `
- [x] ExaGo.VIZ.backend build and UP  [id:: owk922]  [completion:: 2026-01-16]

### PROBLEM:`Python3.14` and `Langchain` incompatibility
Added [[2026-01-14]]

#### SUGGESTED solution
- [x] (build) .venv Python3.13 or 3.14  [created:: 2026-01-14]  [due:: 2026-02-09]  [completion:: 2026-02-25]
- [x] (build) update dependencies (check: [requirements.txt](https://github.com/langchain-ai/langchain-academy/blob/main/requirements.txt))  [created:: 2026-01-14]  [due:: 2026-02-09]  [completion:: 2026-02-25]
	- RESULT: [Chatgrid_backend (AI agent)](https://github.com/Walter462/ExaGO/commit/7851c1cf70af47ebabf57fd50588bfbcb35f5d98)

```bash
#install dependencies first
pip list	#check
pip freeze > requirements.txt	#create/rewrite file
```

- add **environment markers**:
```text
langchain-openai==0.2.1 ; python_version >= "3.10"
```

- restore .venv
```bash
pip install -r requirements.txt	#restore .venv dependencies
```

- (fix) bug `langchain==0.0.233 ` is incompatible with Python3.14 (backward compatibility problem because of Python3.14 typing annotations issues for this LangChain version) update code to Python3.14  
- create python version file
```bash
python --version > .python-version
```
- add to `readme.txt`
```text
## Requirements
- Python 3.13
```

- Enforce in CI / runtime
If you use `pyproject.toml`:
```
[project]
requires-python = ">=3.11,<3.13"
```
Or in GitHub Actions:
```
python-version: "3.11"
```

##### `requirements.txt`

```bash
Flask==2.3.2
Flask-Cors==4.0.0
openai==0.27.8
openapi-schema-pydantic==1.2.4
langchain==0.1.0 # update dependency version for Python3.14+ (from 0.0.233)
langsmith==0.0.5
shapely==2.1.2
pandas==2.3.3
geopandas==1.1.1
psycopg2-binary==2.9.11 #add dependency
```

#### READY solution: stay at Python3.12
>[!success] `langchain==0.0.233 `works With Python3.12.6

##### `requirements.txt`

```bash
Flask==2.3.2
Flask-Cors==4.0.0
openai==0.27.8
openapi-schema-pydantic==1.2.4
langchain==0.0.233 # `0.1.0` update dependency version for Python3.14+ 
# langchain>=0.1.0
langsmith==0.0.5
shapely==2.1.2
pandas==2.3.3
geopandas==1.1.1
psycopg2-binary==2.9.11 #add dependency
```

#### ANALYSIS

>[!danger]  
>`langchain==0.0.233 ` is incompatible with Python3.14

Looking at  requirements.txt, we are using `langchain 0.0.233`, which is an older version that has compatibility issues with Python 3.14. The error occurs because:
1. **Old langchain version**:  `langchain 0.0.233` has outdated type annotations
2. **Python 3.14 strictness**: Newer Python versions are stricter about type checking
3. **Missing type annotations**: The `CopyFileTool` class in langchain lacks proper type annotations for `args_schema`

#### DESCRIPTION

Got this problem when I start to run Python server.

```python
(.venv) ➜  backend git:(my-cool-feature-dev) ✗ python server.py 
Traceback (most recent call last):
  File "/Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/backend/server.py", line 6, in <module>
    from sqlchain import sqlchain
  File "/Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/backend/sqlchain.py", line 1, in <module>
    from langchain import SQLDatabase, SQLDatabaseChain
  File "/Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/backend/.venv/lib/python3.14/site-packages/langchain/__init__.py", line 6, in <module>
    from langchain.agents import MRKLChain, ReActChain, SelfAskWithSearchChain
  File "/Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/backend/.venv/lib/python3.14/site-packages/langchain/agents/__init__.py", line 2, in <module>
    from langchain.agents.agent import (
    ...<6 lines>...
    )
  File "/Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/backend/.venv/lib/python3.14/site-packages/langchain/agents/agent.py", line 16, in <module>
    from langchain.agents.tools import InvalidTool
  File "/Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/backend/.venv/lib/python3.14/site-packages/langchain/agents/tools.py", line 8, in <module>
    from langchain.tools.base import BaseTool, Tool, tool
  File "/Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/backend/.venv/lib/python3.14/site-packages/langchain/tools/__init__.py", line 15, in <module>
    from langchain.tools.file_management import (
    ...<7 lines>...
    )
  File "/Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/backend/.venv/lib/python3.14/site-packages/langchain/tools/file_management/__init__.py", line 3, in <module>
    from langchain.tools.file_management.copy import CopyFileTool
  File "/Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/backend/.venv/lib/python3.14/site-packages/langchain/tools/file_management/copy.py", line 25, in <module>
    class CopyFileTool(BaseFileToolMixin, BaseTool):
    ...<35 lines>...
            raise NotImplementedError
  File "/Users/walternzd/0_SSD/Projects/Dev/ExaGO/viz/backend/.venv/lib/python3.14/site-packages/langchain/tools/base.py", line 55, in __new__
    raise SchemaAnnotationError(
    ...<6 lines>...
    )
langchain.tools.base.SchemaAnnotationError: Tool definition for CopyFileTool must include valid type annotations for argument 'args_schema' to behave as expected.
Expected annotation of 'Type[BaseModel]' but got 'None'.
Expected class looks like:

class ChildTool(BaseTool):
    ...
    args_schema: Type[BaseModel] = SchemaClass
    ...
```


### PROBLEM: no psycopg2 dependency

#### READY solution: update requirements

Add `psycopg2-binary==2.9.11` to requirements.txt
- [x] (build) MR add `psycopg2-binary==2.9.11` to `requirements.txt` (dependency lack in current version)  [created:: 2026-01-13]  [completion:: 2026-02-25]
	- REAULT: [Chatgrid_backend (AI agent)](https://github.com/Walter462/ExaGO/commit/7851c1cf70af47ebabf57fd50588bfbcb35f5d98)

##### `requirements.txt`

```bash
Flask==2.3.2
Flask-Cors==4.0.0
openai==0.27.8
openapi-schema-pydantic==1.2.4
langchain==0.0.233
langsmith==0.0.5
shapely==2.1.2
pandas==2.3.3
geopandas==1.1.1
psycopg2-binary==2.9.11 #add dependency
```

#### DESCRIPTION
Eve building pipeline adds `psycopg2-binary` to python venv manually.

##  Frontend `DONE`
- [x] ExaGo.VIZ.frontend build and UP  [id:: 96wrgc]  [completion:: 2026-01-12]

# Eve shell instructions
VIZ installation process from eve 

## Eve shell routine notes
- check psql is in global
- add psycopg2-binary to requirements.txt if we really need it
- DB create ExaGo DB instance incorrect syntax

## Routine 

```bash
# pull ExaGo git
ExaGO$cd lib/ExaGO/
ExaGO$git status
ExaGO$git pull
ExaGO$sudo apt update
# nvm install
ExaGO$which curl
ExaGO$curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
ExaGO$source ~/.bashrc
# nvm version pick
ExaGO$nvm install 24
ExaGO$nvm use 24
# yarn install
ExaGO$npm install --global yarn
ExaGO$cd viz/
ExaGO/viz$ yarn install
# python install
ExaGO/viz$ sudo apt install python3-pip
ExaGO/viz$ sudo apt install python3
# python dependencies install
ExaGO/viz$ cd backend/
ExaGO/viz$ pip3
# Eve: does not work
ExaGO/viz$ pip3 install -r requirements.txt 
ExaGO/viz$ python3 -m venv .venv
# Eve: works 
# python intall
ExaGO/viz$ sudo apt install python3.12-venv
# python venv
ExaGO/viz/backend$ python3 -m venv .venv
ExaGO/viz/backend$ source .venv/bin/activate
# python dependencies install into venv
(.venv) ExaGO/viz/backend$ pip3 install -r requirements.txt
# generate data
(.venv) ExaGO/viz/backend$ cd ..
(.venv) ExaGO/viz$ python3 geninputfile.py data/case_ACTIVSg10k.json
# This enables the website
(.venv) ExaGO/viz$ yarn start

# Open a different window
$ cd lib/ExaGO/viz/backend/
ExaGO/viz/backend$ source .venv/bin/activate
(.venv) ExaGO/viz/backend$ python3 ../data/jsontocsv.py ../data/case_ACTIVSg10k.json

# DB
# Open a different window
$ sudo apt install postgresql postgresql-contrib
$ sudo systemctl status postgresql
$ sudo -i -u postgres
# V: add psql to global environment
postgres@LAP136650:~$ psql
postgres=# \du
postgres=# ALTER USER postgres WITH PASSWORD 'ExaGO.2025';
postgres=# \q
postgres@LAP136650:~$ exit
# DB create ExaGo DB instance
$ cd lib/ExaGO/viz/backend/
ExaGO/viz/backend$ PGUSER=postgres PGPASSWORD=ExaGO.2025 ./create_db.sh  --db exago_db –schema-sql ./schema.sql --drop  --truncate
# V: not working
# V: ERROR: –schema-sql -"add -"-> --schema-sql
CORRECT: PGUSER=postgres PGPASSWORD=ExaGO.2025 ./create_db.sh --db exago_db --schema-sql ./schema.sql --drop --truncate

# add API and DB credentials
ExaGO/viz/backend$ vi config.py
# start venv
ExaGO/viz/backend$ source .venv/bin/activate

(.venv) ExaGO/viz/backend$ python3 server.py
ModuleNotFoundError: No module named 'psycopg2'
(.venv) ExaGO/viz/backend$ pip3 install psycopg2-binary
(.venv) ExaGO/viz/backend$ python server.py

This enables the chatgrid
```
