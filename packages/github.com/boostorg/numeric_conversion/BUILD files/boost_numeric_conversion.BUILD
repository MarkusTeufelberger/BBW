cc_library(
    name = "numeric_conversion",
    hdrs = glob([
        "include/boost/**/*.hpp",
    ]),
    strip_include_prefix = "include",
    visibility = ["//visibility:public"],
    deps = [
        "@boost_conversion//:conversion",
        "@boost_core//:core",
        "@boost_mpl//:mpl",
        "@boost_type_traits//:type_traits",
    ],
)
