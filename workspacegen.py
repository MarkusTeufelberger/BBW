#!/usr/bin/env python3
"""WORKSPACE file generator.

Usage:
  workspacegen.py (<yml_file>...)
  workspacegen.py (-h | --help)

Options:
  -h --help     Show this screen.
"""

import hashlib
import sys

import docopt
import jinja2
import requests
import yaml


def process_yml(parsed: list) -> list:
    rule = ""
    name = ""
    build_file = ""
    sha256 = ""
    strip_prefix = ""
    urls_list = ""
    remotes_list = ""
    commit = ""

    output = {"content": []}

    for entry in parsed:
        # update whatever is already defined
        if "rule" in entry:
            rule = entry["rule"]
        if "name" in entry:
            name = entry["name"]
        if "build_file" in entry:
            build_file = entry["build_file"]
        if "sha256" in entry:
            sha256 = entry["sha256"]
        if "strip_prefix" in entry:
            strip_prefix = entry["strip_prefix"]
        if "urls_list" in entry:
            urls_list = entry["urls_list"]
        if "remotes" in entry:
            remotes_list = entry["remotes"]
        if "commit" in entry:
            commit = entry["commit"]

        # currently only new_http_archive is supported...
        if rule != "new_http_archive":
            raise NotImplementedError

        # automagic for some hosts:

        # github.com:
        # You can get a repository at a certain commit via
        # "https://github.com/<user>/<repo>/archive/<commit>.zip"
        # Prefix to be stripped from this archive:
        #  "<repo>-<commit>"
        if len(remotes_list) == 1:
            if remotes_list[0].startswith(
                    "https://github.com") or remotes_list[0].startswith(
                        "http://github.com"):
                gh_user = remotes_list[0].split("/")[3]
                gh_repo = remotes_list[0].split("/")[4]
                urls_list = [
                    f"https://github.com/{gh_user}/{gh_repo}/archive/{commit}.zip"
                ]
                strip_prefix = f"{gh_repo}-{commit}"

        # get the first file in urls_list and calculate a sha256 hash
        print(f"Downloading {urls_list[0]}")
        r = requests.get(urls_list[0])
        # TODO: error handling
        print(f"Hashing {urls_list[0]} (size: {len(r.content)})")
        sha256 = hashlib.sha256(r.content).hexdigest()

        # currently only new_http_archive is supported...
        if rule == "new_http_archive":
            output["content"].append({
                "rule": rule,
                "name": name,
                "build_file": build_file,
                "sha256": sha256,
                "strip_prefix": strip_prefix,
                "urls_list": urls_list,
            })

    return output


def render_template(content: list, template_environment):
    return template_environment.get_template("WORKSPACE.j2").render(content)


def main(arguments) -> int:
    template_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader("."))
    for yml_file in arguments["<yml_file>"]:
        print(f"Processing {yml_file}")
        with open(yml_file, "r") as current_file:
            try:
                parsed = yaml.load(current_file)
            except yaml.YAMLError as exc:
                print(exc)
        to_render = process_yml(parsed)
        rendered = render_template(to_render, template_environment)
        # TODO: splitting filenames like this is ugly and brittle, change it!
        with open(yml_file.split(".")[0] + ".WORKSPACE", "w") as build_file:
            build_file.write(rendered)
        # TODO: run buildifier over the rendered template?
    return 0


# run main() if called standalone
if __name__ == "__main__":
    arguments = docopt.docopt(__doc__)
    sys.exit(main(arguments))
