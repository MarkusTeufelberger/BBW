cc_library(
    name = "lz4",
    srcs = [
        "lz4.c",
    ],
    hdrs = [
        "lz4.h",
    ],
    visibility = ["//visibility:public"],
)

cc_library(
    name = "lz4_hc",
    srcs = [
        "lz4hc.c",
    ],
    hdrs = [
        "lz4hc.h",
    ],
    deps = [
        ":lz4",
    ],
    visibility = ["//visibility:public"],
)

cc_library(
    name = "lz4_frame",
    srcs = [
        "lz4frame.c",
        "xxhash.h"
    ],
    hdrs = [
        "lz4frame.h",
    ],
    deps = [
        ":lz4",
        ":lz4_hc",
    ],
    visibility = ["//visibility:public"],
)