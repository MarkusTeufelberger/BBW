#!/usr/bin/env python3
"""BUILD file generator.

Usage:
  buildfilegen.py (<directory>)
  buildfilegen.py (-h | --help)

Options:
  -h --help     Show this screen.
"""

import pathlib
import sys

import docopt
import jinja2
import yaml


def process_build_yml(parsed: list) -> dict:
    rule = ""
    name = ""
    srcs_list = ""
    target_list = ""


    output = {
        "header_list": [],
        "content": [],
    }

    # tar archive rule header
    output["header_list"].append('load("@bazel_tools//tools/build_defs/pkg:pkg.bzl", "pkg_tar")')

    # global filegroup
    output["content"].append({
        "rule": "filegroup",
        "name": "global_filegroup",
        "srcs_list": [],
        })

    # global tarball
    output["content"].append({
        "rule": "pkg_tar",
        "name": "global_tarball",
        "deps_list": [],
        })

    for entry in parsed:
        if "name" in entry:
            name = entry["name"]
        if "targets" in entry:
            target_list = entry["targets"]

        # Add target(s) to global_filegroup
        for buildrule in enumerate(output["content"]):
                if buildrule[1]["name"] == "global_filegroup":
                    for target in target_list:
                        output["content"][buildrule[0]]["srcs_list"].append(f"@{name}//:{target}")

        # create individual tarball
        output["content"].append({
            "rule": "pkg_tar",
            "name": f"{name}",
            "package_dir": f"/{name}",
            "files_list": [f"@{name}//:{target}" for target in target_list],
            })

        # add individual tarball to global_tarball
        for buildrule in enumerate(output["content"]):
                if buildrule[1]["name"] == "global_tarball":
                    output["content"][buildrule[0]]["deps_list"].append(f":{name}")

    # TODO: create more complex rule(s) to be able to run smoke tests (e.g. simple import + hello world)
    return output


def render_build_template(content: list, template_environment):
    return template_environment.get_template("BUILD.j2").render(content)


def main(arguments) -> int:
    template_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader("tools/internal/buildfilegen/templates"))
    mypath = pathlib.Path(arguments["<directory>"])
    for yml_file in list(mypath.glob("**/*.yml")):
        print(f"Processing {yml_file}")
        with yml_file.open() as current_file:
            try:
                parsed = yaml.load(current_file)
            except yaml.YAMLError as exception:
                print(exception)
        build_to_render = process_build_yml(parsed)
        rendered_build = render_build_template(build_to_render, template_environment)
        # TODO: add path to file
        with yml_file.parent.joinpath("BUILD").open(mode="w") as build_file:
            build_file.write(rendered_build)
        # TODO: run buildifier over the rendered template?
    return 0


# run main() if called standalone
if __name__ == "__main__":
    arguments = docopt.docopt(__doc__)
    sys.exit(main(arguments))
