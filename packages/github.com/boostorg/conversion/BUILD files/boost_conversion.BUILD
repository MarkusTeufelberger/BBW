cc_library(
    name = "conversion",
    hdrs = glob([
        "include/boost/**/*.hpp",
    ]),
    strip_include_prefix = "include",
    visibility = ["//visibility:public"],
    deps = [
        "@boost_assert//:assert",
        "@boost_config//:config",
        "@boost_throw_exception//:throw_exception",
    ],
)
