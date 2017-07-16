cc_library(
    name = "ratio",
    hdrs = glob([
        "include/boost/**/*.hpp",
    ]),
    strip_include_prefix = "include",
    visibility = ["//visibility:public"],
    deps = [
        "@boost_config//:config",
        "@boost_integer//:integer",
        "@boost_mpl//:mpl",
        "@boost_type_traits//:type_traits",
    ],
)
