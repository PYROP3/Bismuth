# Bismuth

Python-based web-app for managing discord bots

## Installing bots

Install supported bots into the `bots` folder using `git clone`
```sh
cd bots
git clone ...
```

### Supported bots

- [XeroqueHomes](https://github.com/PYROP3/XeroqueHomes): A bot for quickly finding people in voice chats (which should honestly be a native feature)

More bots might be added later. If you want, you may also develop your own bot to be used with Bismuth by (loosely) following the format in one of the bots above. Basically, it should be able to be executed standalone as a python application and should pipe its output to stdout so it can be captured by the manager. Then you just have to add it to the `bots` folder and _boom_!

### Generating bots file

After installing any new bots, you must (re-)generate the `bots.py` so the manager can find them. This file can be generated manually, following the pattern:

```
available_bots = [
    (<bot id>, <bot folder inside bots>, (<bot .py file>)),
    (<bot id>, <bot folder inside bots>, (<bot .py file>)), ...
]
```

It can also be generated automatically using the `generate_bots` tool

```
python3 generate_bots.py
```

## Running Bismuth

Run bismuth.py as a python3 app after installing the requirements

```
python3 -m pip install -r requirements.txt
python3 bismuth.py
```

If running for the first time, this will generate an auxiliary file and exit. Just run it again

## Managing bots

The web app will be accessible in your browser via port 5000
