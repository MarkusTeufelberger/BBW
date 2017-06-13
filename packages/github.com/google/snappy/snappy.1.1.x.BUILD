genrule(
    name = "generated_headers",
    srcs = glob([
        "autogen.sh",
        "configure.ac",
        "Makefile.am",
        "AUTHORS",
        "ChangeLog",
        "COPYING",
        "NEWS",
        "README",
        "m4/*",
        "*.in",
    ]),
    outs = [
        "config.h",
        "snappy-stubs-public.h",
    ],
    cmd = "pushd $$(dirname $(location autogen.sh)) && \
    ./autogen.sh && \
    ./configure && \
    popd && \
    mv $$(dirname $(location autogen.sh))/config.h $(location config.h) && \
    mv $$(dirname $(location autogen.sh))/snappy-stubs-public.h $(location snappy-stubs-public.h)",
)

cc_library(
    name = "snappy",
    srcs = glob(
        ["*.cc"],
        exclude = [
            "snappy-test.cc",
            "snappy_unittest.cc",
        ],
    ),
    hdrs = [":generated_headers"] + glob(["*.h"]),
    visibility = ["//visibility:public"],
)
