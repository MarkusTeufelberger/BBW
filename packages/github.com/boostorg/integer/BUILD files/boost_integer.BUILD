cc_library(
    name = "integer",
    hdrs = glob([
        "include/boost/**/*.hpp",
    ]),
    strip_include_prefix = "include",
    visibility = ["//visibility:public"],
    deps = [
        "@boost_config//:config",
        "@boost_static_assert//:static_assert",
    ],
)
