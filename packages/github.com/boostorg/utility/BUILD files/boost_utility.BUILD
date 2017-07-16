cc_library(
    name = "utility",
    hdrs = glob([
        "include/boost/**/*.hpp",
    ]),
    strip_include_prefix = "include",
    visibility = ["//visibility:public"],
    deps = [
        "@boost_core//:core",
        "@boost_preprocessor//:preprocessor",
        "@boost_type_traits//:type_traits",
    ],
)
