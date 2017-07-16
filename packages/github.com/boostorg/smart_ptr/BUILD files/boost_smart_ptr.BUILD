cc_library(
    name = "smart_ptr",
    hdrs = glob([
        "include/boost/**/*.hpp",
    ]),
    strip_include_prefix = "include",
    visibility = ["//visibility:public"],
    deps = [
        "@boost_assert//:assert",
        "@boost_config//:config",
        "@boost_core//:core",
        "@boost_move//:move",
        "@boost_predef//:predef",
        "@boost_throw_exception//:throw_exception",
        "@boost_type_traits//:type_traits",
    ],
)
