cc_library(
    name = "chrono",
    srcs = glob([
        "src/**/*.cpp",
    ]),
    hdrs = glob([
        "include/boost/**/*.hpp",
    ]),
    strip_include_prefix = "include",
    visibility = ["//visibility:public"],
    deps = [
        "@boost_config//:config",
        "@boost_move//:move",
        "@boost_mpl//:mpl",
        "@boost_predef//:predef",
        "@boost_ratio//:ratio",
        "@boost_system//:system",
        "@boost_throw_exception//:throw_exception",
        "@boost_utility//:utility",
    ],
)
