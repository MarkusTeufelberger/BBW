cc_library(
    name = "system",
    srcs = glob([
        "src/**/*.cpp",
    ]),
    hdrs = glob([
        "include/boost/**/*.hpp",
        "include/boost/**/*.ipp",
    ]),
    strip_include_prefix = "include",
    visibility = ["//visibility:public"],
    deps = [
        "@boost_assert//:assert",
        "@boost_config//:config",
        "@boost_core//:core",
        "@boost_predef//:predef",
    ],
)
