cc_library(
    name = "concept_check",
    hdrs = glob([
        "include/boost/**/*.hpp",
    ]),
    strip_include_prefix = "include",
    visibility = ["//visibility:public"],
    deps = [
        "@boost_assert//:assert",
        "@boost_config//:config",
        "@boost_mpl//:mpl",
        "@boost_preprocessor//:preprocessor",
        "@boost_type_traits//:type_traits",
    ],
)
