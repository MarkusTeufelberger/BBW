cc_library(
    name = "date_time",
    srcs = glob([
        "src/**/*.cpp",
        "src/**/*.hpp",
    ]),
    hdrs = glob([
        "include/boost/**/*.hpp",
        "include/boost/**/*.ipp",
    ]),
    strip_include_prefix = "include",
    visibility = ["//visibility:public"],
    deps = [
        "@boost_config//:config",
        "@boost_mpl//:mpl",
        "@boost_smart_ptr//:smart_ptr",
        "@boost_throw_exception//:throw_exception",
        "@boost_utility//:utility",
    ],
)
