#!/usr/bin/env python3
"""buildozerfile file generator.

Usage:
  buildozerfilegen.py (<directory>)
  buildozerfilegen.py (-h | --help)

Options:
  -h --help     Show this screen.
"""

import glob
import hashlib
import pathlib
import shutil
import sys

import docopt
import requests
import yaml


def create_subfolders(parsed: list, path):
    for entry in parsed:
        if "version" not in entry:
            raise RuntimeError("You need to specify a version for every entry")
        path.mkdir(exist_ok=True)
        with_version = path / entry["version"]
        assert(with_version.parent == path)
        with_version.mkdir(exist_ok=True)


def move_test_build_files(parsed: list, path, dependencies: dict):
    build_file = None
    for entry in parsed:
        if "version" not in entry:
            raise RuntimeError("You need to specify a version for every entry")
        tests_with_version = path / "releases_tests" / entry["version"]
        if "build_file" in entry:
            build_file = entry["build_file"]
        assert(build_file != None)
        build_file_src = path / "BUILD files" / build_file
        tests_build_file_dst = tests_with_version / build_file
        shutil.copyfile(build_file_src, tests_build_file_dst)
    for version in dependencies:
        for dep in dependencies[version]:
            # HACK, this is brittle and specific to boost libraries!
            # TODO: generalize this
            if "boostorg" in str(dep):
                build_file = str(dep.stem) + ".BUILD"
                tests_with_version = path / "releases_tests" / version
                build_file_src = dep.parent / "BUILD files" / build_file
                tests_build_file_dst = tests_with_version / build_file
                shutil.copyfile(build_file_src, tests_build_file_dst)


def move_build_files(parsed: list, path):
    build_file = None
    for entry in parsed:
        if "version" not in entry:
            raise RuntimeError("You need to specify a version for every entry")
        with_version = path / "releases" / entry["version"]
        if "build_file" in entry:
            build_file = entry["build_file"]
        assert(build_file != None)
        build_file_src = path / "BUILD files" / build_file
        build_file_dst = with_version / build_file
        shutil.copyfile(build_file_src, build_file_dst)


def move_test_files(parsed: list, path):
    test_files = []
    for entry in parsed:
        if "version" not in entry:
            raise RuntimeError("You need to specify a version for every entry")
        tests_with_version = path / "releases_tests" / entry["version"]
        if "smoke_tests" in entry:
            test_files = []
            for test in entry["smoke_tests"]:
                test_files += test["source_files"]
        assert(test_files != [])
        for test_file in test_files:
            test_file_src = path / "tests" / test_file
            test_file_dst = tests_with_version / test_file
            shutil.copyfile(test_file_src, test_file_dst)


def concat_buildozerfiles(path, dependencies: dict):
    # concatenate all relevant buildozerfiles
    #print(dependencies)

    for version in dependencies:
        with open(path / version / "buildozerfile", "w") as target_file:
            for dep in dependencies[version]:
                with open(dep.parent / "releases" / version / "buildozerfile", "r") as source_file:
                    target_file.write(source_file.read())


def get_targets(all_files: dict) -> dict:
    # "@boost_system//:system" --> PosixPath('packages/github.com/boost/system/boost_system.yml')
    output = {}
    for yml_file in all_files:
        name = ""
        targets_list = ""
        for entry in all_files[yml_file]:
            if "name" in entry:
                name = entry["name"]
            if "targets" in entry:
                targets_list = [f"@{name}//:{target}" for target in entry["targets"]]
            for target in targets_list:
                output[target] = yml_file
    return output


def get_dependencies(parsed: list, targets: dict) -> dict:
    output = {}
    ext_dependencies = set()
    test_dependencies = set()
    name = ""
    targets_list = ""
    for entry in parsed:
        if "version" not in entry:
            raise RuntimeError("You need to specify a version for every entry")

        # Always add own targets to dependencies
        if "name" in entry:
                name = entry["name"]
        if "targets" in entry:
            targets_list = [f"@{name}//:{target}" for target in entry["targets"]]
        for target in targets_list:
            ext_dependencies.add(targets[target])
        # Add dependencies defined for this version
        if "deps" in entry:
            ext_dependencies = set()
            for dep in entry["deps"]:
                ext_dependencies.add(targets[dep])
        # Add dependencies of all tests defined for this version
        if "smoke_tests" in entry:
            test_dependencies = set()
            for test in entry["smoke_tests"]:
                if "deps" in test:
                    for dep in test["deps"]:
                        test_dependencies.add(targets[dep])
        dependencies = ext_dependencies.union(test_dependencies)
        output[entry["version"]] = list(dependencies)
    
    # TODO: transitive dependencies (A depends on B, B depends on C)
    #print(output)
    return output


def create_buildozerfiles(parsed: list) -> dict:
    rule = ""
    name = ""
    build_file = ""
    sha256 = ""
    strip_prefix = ""
    urls_list = ""
    remotes_list = ""
    commit = ""
    targets_list = ""
    dependencies_list = ""

    output = {}

    for entry in parsed:
        if "version" not in entry:
            raise RuntimeError("You need to specify a version for every entry")
        elif entry["version"] in output:
            raise RuntimeError("Versions have to be unique")
        else:
            output[entry["version"]] = []

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
        if "urls" in entry:
            urls_list = entry["urls"]
        if "remotes" in entry:
            remotes_list = entry["remotes"]
        if "commit" in entry:
            commit = entry["commit"]
        if "targets" in entry:
            targets_list = [f"@{name}//:{target}" for target in entry["targets"]]
        if "deps" in entry:
            dependencies_list = entry["deps"]

        if rule == "new_http_archive":
            # automagic for some common hosts/tasks:

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

            # gitlab.com:
            # UNTESTED! (especially the "not named archive.bz2" part seems potentially problematic)
            # You can get a repository at a certain commit via
            # "https://gitlab.com/<user>/<repo>/repository/archive.tar.bz2?ref=<commit>"
            # Prefix to be stripped from this archive (named <repo>-<commit>-<commit>.tar.bz2 btw, not archive.tar.bz2):
            #  "<repo>-<commit>-<commit>"
            if len(remotes_list) == 1:
                if remotes_list[0].startswith(
                        "https://gitlab.com") or remotes_list[0].startswith(
                            "http://gitlab.com"):
                    gl_user = remotes_list[0].split("/")[3]
                    gl_repo = remotes_list[0].split("/")[4]
                    urls_list = [
                        f"https://gitlab.com/{gl_user}/{gl_repo}/repository/archive.tar.bz2?ref={commit}"
                    ]
                    strip_prefix = f"{gl_repo}-{commit}-{commit}"

            # Hash omitted in yaml file:
            if "sha256" not in entry:
                # get the first file in urls_list and calculate a sha256 hash
                print(f"Downloading {urls_list[0]}")
                r = requests.get(urls_list[0])
                # TODO: error handling
                print(f"Hashing {urls_list[0]} (size: {len(r.content)})")
                sha256 = hashlib.sha256(r.content).hexdigest()
                print(f"Hash: {sha256}")

            output[entry["version"]].append(f"new new_http_archive {name}|-:__pkg__\n")
            output[entry["version"]].append(f"comment name version\ {entry['version']}|-:{name}\n")
            output[entry["version"]].append(f"set build_file {build_file}|-:{name}\n")
            targets_string = ",\ ".join(targets_list)
            if dependencies_list == "":
                output[entry["version"]].append(f"comment build_file provides:\ {targets_string}|-:{name}\n")
            else:
                dependencies_string = ",\ ".join(dependencies_list)
                output[entry["version"]].append(f"comment build_file provides:\ {targets_string};\ depends\ on:\ {dependencies_string}|-:{name}\n")
            output[entry["version"]].append(f"set sha256 {sha256}|-:{name}\n")
            output[entry["version"]].append(f"set strip_prefix {strip_prefix}|-:{name}\n")
            urls_string = ",\ ".join(urls_list)
            output[entry["version"]].append(f"add urls {urls_string}|-:{name}\n")

        # WIP
        elif rule == "new_git_repository":
            # TODO: add skylark rules instead of native ones
            raise NotImplementedError

        else:
            raise NotImplementedError

    return output


def create_buildozertestfiles(parsed: list) -> dict:
    rule = ""
    name = ""
    dependencies_list = ""
    source_files_list = ""
    tests = {}

    output = {}

    target_name = ""

    for entry in parsed:
        if "version" not in entry:
            raise RuntimeError("You need to specify a version for every entry")
        elif entry["version"] in output:
            raise RuntimeError("Versions have to be unique")
        else:
            output[entry["version"]] = []

        # update whatever is already defined
        if "smoke_tests" in entry:
            tests = {index: {} for index in range(len(entry["smoke_tests"]))}
            for test_index, _ in enumerate(entry["smoke_tests"]):
                if "rule" in entry["smoke_tests"][test_index]:
                    rule = entry["smoke_tests"][test_index]["rule"]
                    tests[test_index]["rule"] = rule
                else:
                    rule = tests[test_index]["rule"]

                if "name" in entry["smoke_tests"][test_index]:
                    name = entry["smoke_tests"][test_index]["name"]
                    tests[test_index]["name"] = name
                else:
                    name = tests[test_index]["name"]

                if "deps" in entry["smoke_tests"][test_index]:
                    dependencies_list = entry["smoke_tests"][test_index]["deps"]
                    tests[test_index]["deps"] = dependencies_list
                else:
                    dependencies_list = tests[test_index]["deps"]

                if "source_files" in entry["smoke_tests"][test_index]:
                    source_files_list = entry["smoke_tests"][test_index]["source_files"]
                    tests[test_index]["source_files"] = source_files_list
                else:
                    source_files_list = tests[test_index]["source_files"]

                if rule == "cc_binary":
                    output[entry["version"]].append(f"new {rule} {name}|-:__pkg__\n")
                    dependencies_string = " ".join(dependencies_list)
                    output[entry["version"]].append(f"add deps {dependencies_string}|-:{name}\n")
                    source_files_string = " ".join(source_files_list)
                    output[entry["version"]].append(f"add srcs {source_files_string}|-:{name}\n")
                else:
                    raise NotImplementedError(f"Rule {rule} not yet implemented! {entry}")
        else:
            # use existing tests
            for test_index in range(len(tests)):
                rule = tests[test_index]["rule"]
                name = tests[test_index]["name"]
                dependencies_list = tests[test_index]["deps"]
                source_files_list = tests[test_index]["source_files"]

                if rule == "cc_binary":
                    output[entry["version"]].append(f"new {rule} {name}|-:__pkg__\n")
                    dependencies_string = " ".join(dependencies_list)
                    output[entry["version"]].append(f"add deps {dependencies_string}|-:{name}\n")
                    source_files_string = " ".join(source_files_list)
                    output[entry["version"]].append(f"add srcs {source_files_string}|-:{name}\n")
                else:
                    raise NotImplementedError(f"Rule {rule} not yet implemented! {entry}")
    return output


def main(arguments) -> int:
    mypath = pathlib.Path(arguments["<directory>"])
    # content of all yml files
    all_files = {}
    for yml_file in list(mypath.glob("**/*.yml")):
        print(f"Processing {yml_file}")
        with yml_file.open() as current_file:
            try:
                parsed = yaml.load(current_file)
            except yaml.YAMLError as exception:
                print(exception)
            all_files[yml_file] = parsed
    # Create WORKSPACE files
    for yml_file in all_files:
        parsed = all_files[yml_file]
        create_subfolders(parsed, yml_file.parent / "releases")
        # move relevant BUILD file
        move_build_files(parsed, yml_file.parent)
        # Write buildozerfiles for WORKSPACE
        buildozerfiles = create_buildozerfiles(parsed)
        for version in buildozerfiles:
            with yml_file.parent.joinpath("releases").joinpath(version).joinpath("buildozerfile").open(mode="w") as buildozerfile:
                buildozerfile.writelines(buildozerfiles[version])
    
    # Create tests
    targets = get_targets(all_files)
    for yml_file in all_files:
        parsed = all_files[yml_file]
        create_subfolders(parsed, yml_file.parent / "releases_tests")
        dependencies = get_dependencies(parsed, targets)
        # move relevant BUILD file(s)
        move_test_build_files(parsed, yml_file.parent, dependencies)

        # create buildozerfiles
        concat_buildozerfiles(yml_file.parent / "releases_tests", dependencies)
        
        # Write buildozertestfiles for BUILD files
        buildozertestfiles = create_buildozertestfiles(parsed)
        for version in buildozertestfiles:
            with yml_file.parent.joinpath("releases_tests").joinpath(version).joinpath("buildozertestfile").open(mode="w") as buildozertestfile:
                buildozertestfile.writelines(buildozertestfiles[version])
        # move relevant test files
        move_test_files(parsed, yml_file.parent)

    return 0


# run main() if called standalone
if __name__ == "__main__":
    arguments = docopt.docopt(__doc__)
    sys.exit(main(arguments))
