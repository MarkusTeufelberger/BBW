cc_library(
    # src/alloc_lib.c includes this c file:
    name = "dlmalloc_c",
    hdrs = glob([
        "src/**/dlmalloc_*.c",
    ]),
    visibility = ["//visibility:private"],
)

cc_library(
    name = "container",
    srcs = glob([
        "src/**/*.c",
        "src/**/*.cpp",
    ]),
    hdrs = glob([
        "include/boost/**/*.h",
        "include/boost/**/*.hpp",
    ]),
    strip_include_prefix = "include",
    visibility = ["//visibility:public"],
    deps = [
        ":dlmalloc_c",
        "@boost_config//:config",
        "@boost_intrusive//:intrusive",
        "@boost_move//:move",
    ],
)
