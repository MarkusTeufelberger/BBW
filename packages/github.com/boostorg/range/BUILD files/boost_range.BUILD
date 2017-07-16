cc_library(
    name = "range",
    hdrs = glob([
        "include/boost/**/*.hpp",
    ]),
    strip_include_prefix = "include",
    visibility = ["//visibility:public"],
    deps = [
        "@boost_concept_check//:concept_check",
        "@boost_config//:config",
        "@boost_iterator//:iterator",
        "@boost_mpl//:mpl",
        "@boost_preprocessor//:preprocessor",
        "@boost_type_traits//:type_traits",
        "@boost_utility//:utility",
    ],
)
