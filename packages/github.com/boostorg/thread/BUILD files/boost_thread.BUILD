cc_library(
    # src/pthread/once.cpp includes this cpp file:
    name = "once_atomic_cpp",
    hdrs = ["src/pthread/once_atomic.cpp"],
    visibility = ["//visibility:private"],
)

cc_library(
    name = "thread",
    srcs = glob([
        "src/**/*.cpp",
    ]),
    hdrs = glob([
        "include/boost/**/*.hpp",
    ]),
    strip_include_prefix = "include",
    visibility = ["//visibility:public"],
    deps = [
        ":once_atomic_cpp",
        "@boost_core//:core",
        "@boost_move//:move",
        "@boost_system//:system",
        "@boost_type_traits//:type_traits",
        "@boost_winapi//:winapi",
    ],
)
