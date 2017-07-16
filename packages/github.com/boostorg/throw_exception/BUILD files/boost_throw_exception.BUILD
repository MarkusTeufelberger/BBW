cc_library(
    name = "throw_exception",
    hdrs = glob([
        "include/boost/**/*.hpp",
    ]),
    strip_include_prefix = "include",
    visibility = ["//visibility:public"],
    deps = [
        "@boost_assert//:assert",
        "@boost_config//:config",
    ],
)
