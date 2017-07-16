cc_library(
    name = "lexical_cast",
    hdrs = glob([
        "include/boost/**/*.hpp",
    ]),
    strip_include_prefix = "include",
    visibility = ["//visibility:public"],
    deps = [
        "@boost_array//:array",
        "@boost_config//:config",
        "@boost_container//:container",
        "@boost_integer//:integer",
        "@boost_numeric_conversion//:numeric_conversion",
        "@boost_range//:range",
        "@boost_throw_exception//:throw_exception",
    ],
)
