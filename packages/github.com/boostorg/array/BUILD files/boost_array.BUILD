cc_library(
    name = "array",
    hdrs = glob([
        "include/boost/**/*.hpp",
    ]),
    strip_include_prefix = "include",
    visibility = ["//visibility:public"],
    deps = [
        "@boost_assert//:assert",
        "@boost_config//:config",
        "@boost_core//:core",
        "@boost_static_assert//:static_assert",
        "@boost_throw_exception//:throw_exception",
    ],
)
