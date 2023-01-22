#!/bin/python
# pipe the json string returned from https://api.dictionaryapi.dev
# from stdin to a rich console print object and display
#
# I am aware that this is super messy
# It will be refactored further when I get the motivation
import sys
import json
from rich.console import Console
from rich.panel import Panel
from math import floor

STYLES = {
    "highlight" : "yellow bold",
    "standout"  : "white bold",
    "normal"    : "white",
    "lowlight"  : "#888888 italic",
    "border"    : "yellow",
    "synonym"   : "#88aa88",
    "antonym"   : "#aa8888",
    }

def load_json() -> str:
    try:
        return json.load(sys.stdin)
    except json.decoder.JSONDecodeError:
        print("Unable to parse JSON")
        quit()

def extract_word_object(raw_data) -> str:
    try:
        return raw_data[0]
    except KeyError:
        print("Word not found.")
        quit()

def trim_end(string: str, num=5, end="\n") -> str:
    return string[:-num] + f"[/]{end}"

def build_ipa(ipa_obj: dict, ipa_buf=f"\n[{STYLES['lowlight']}]Pronunciation: [/]") -> str:
    if len(ipa_obj) > 0: 
        for p in ipa_obj:
            try:
                ipa_buf += f"[{STYLES['lowlight']}]{p['text']}, [/]"
            except KeyError:
                pass
        return trim_end(ipa_buf)
    else:
        return ""

def build_readout(data: dict, readout_buf="") -> str:
    readout_buf += build_ipa(data["phonetics"])
    for meaning in data["meanings"]:
        readout_buf += f"\n[{STYLES['standout']}]{data['word']}[/] - [{STYLES['lowlight']}]{meaning['partOfSpeech']}[/]\n"
        definitions = meaning["definitions"]
        synonyms = meaning["synonyms"]
        antonyms = meaning["antonyms"]
        for definition in definitions:
            readout_buf += f"[{STYLES['highlight']}] - [/][{STYLES['normal']}]{definition['definition']}[/]\n"
            try:
                readout_buf += f"[{STYLES['lowlight']}]   Ex. {definition['example']}[/]\n"
            except KeyError:
                pass
            try:
                if len(definition["synonyms"]) > 0:
                    readout_buf += f"   [{STYLES['synonyms']}]> Synonyms: [/]"
                    for synonym in definition["synonyms"]:
                        readout_buf += f"[{STYLES['lowlight']}]{synonym}, [/]"
                    readout_buf = trim_end(readout_buf)
            except KeyError:
                pass
            try:
                if len(definition["antonyms"]) > 0:
                    readout_buf += f"   [{STYLES['antonym']}]> Antonyms: [/]"
                    for antonym in definition["antonyms"]:
                        readout_buf += f"[{STYLES['lowlight']}]{antonym}, [/]"
                    readout_buf = trim_end(readout_buf)
            except KeyError:
                pass

        if len(synonyms) > 0:
            readout_buf += f"\n [{STYLES['synonym']}]> Synonyms: [/]"
            for synonym in synonyms:
                readout_buf += f"[{STYLES['lowlight']}]{synonym}, [/]"
            readout_buf = trim_end(readout_buf)
        if len(antonyms) > 0:
            readout_buf += f"\n [{STYLES['antonym']}]> Antonyms: [/]"
            for antonym in antonyms:
                readout_buf += f"[{STYLES['lowlight']}]{antonym}, [/]"
            readout_buf = trim_end(readout_buf)
    return readout_buf

def run():
    raw = load_json()
    data = extract_word_object(raw)
    readout = build_readout(data)
    console = Console()
    panel = Panel(
                readout,
                title=f"[{STYLES['normal']}]Definition for [{STYLES['highlight']}]{data['word']}[/]",
                title_align="left",
                width=int(floor(console.size.width/2)),
                )

    console.print(panel)

if __name__ == "__main__":
    run()
