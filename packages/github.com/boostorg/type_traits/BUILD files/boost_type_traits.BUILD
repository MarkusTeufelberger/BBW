cc_library(
    name = "type_traits",
    hdrs = glob([
        "include/boost/**/*.hpp",
    ]),
    strip_include_prefix = "include",
    visibility = ["//visibility:public"],
    deps = [
        "@boost_config//:config",
        "@boost_core//:core",
        "@boost_static_assert//:static_assert",
    ]
)
