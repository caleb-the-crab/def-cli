#!/bin/python
# pipe the json string returned from https://api.dictionaryapi.dev
# from stdin to a rich console print object and display
import sys
import json
from flatten_json import flatten
from rich.console import Console
from rich.panel import Panel
from math import floor
raw = json.load(sys.stdin)
try:
   #data = flatten(raw[0])
   data = raw[0]
except KeyError:
    print("Word not found.")
    quit()

word = data["word"]
phonetics = data["phonetics"]
meanings = data["meanings"]

readout = "\n"

ipa = ""
for d in phonetics:
    try:
        ipa += d["text"] + ", "
    except KeyError:
        pass
ipa = ipa[:-2]

readout += f'[#888888 italic]Pronunciation: {ipa}[/]\n'
for meaning in meanings:
    readout += f'\n[bold]{word}[/] - [italic]{meaning["partOfSpeech"]}[/]\n'
    definitions = meaning["definitions"]
    synonyms = meaning["synonyms"]
    antonyms = meaning["antonyms"]
    for definition in definitions:
        readout += f'[bold yellow] - [/]{definition["definition"]}\n'
        try:
            readout += f"[#888888 italic]   Ex.{definition['example']}[/]\n"
        except KeyError:
            pass
        try:
            if len(definition["synonyms"]) > 0:
                readout += "   [#88aa88]> Synonyms: [/]"
                for synonym in definition["synonyms"]:
                    readout += f'[italic #888888]{synonym}, [/]'
                readout = readout[:-5]
                readout += "[/]\n"
        except KeyError:
            pass
        try:
            if len(definition["antonyms"])> 0:
                readout += "   [#aa8888]> Antonyms: [/]"
                for antonym in definition["antonyms"]:
                    readout += f'[italic #888888]{antonym}, [/]'
                readout = readout[:-5]
                readout += "[/]\n"
        except KeyError:
            pass

    if len(synonyms) > 0:
        readout += "\n [#88aa88]> Synonyms: [/]"
        for synonym in synonyms:
            readout += f'[italic #888888]{synonym}, [/]'
        readout = readout[:-5]
        readout += "[/]\n"
    if len(antonyms) > 0:
        readout += "\n [#aa8888]> Antonyms: [/]"
        for antonym in antonyms:
            readout += f'[italic #888888]{antonym}, [/]'
        readout = readout[:-5]
        readout += "[/]\n"

console = Console()
panel = Panel(
            readout,
            title=f"[yellow]Definition for [bold]{word}[/]",
            title_align="left",
            width=int(floor(console.size.width/2)),
            )

console.print(panel)
