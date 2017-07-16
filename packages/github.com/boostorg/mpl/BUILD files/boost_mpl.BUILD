cc_library(
    name = "mpl",
    hdrs = glob([
        "include/boost/**/*.hpp",
    ]),
    strip_include_prefix = "include",
    visibility = ["//visibility:public"],
    deps = [
        "@boost_config//:config",
        "@boost_preprocessor//:preprocessor",
    ],
)
