genrule(
    # Remove the -Werror switch in configure.ac
    name = "configure_ac_mod",
    srcs = ["configure.ac"],
    outs = ["configure.ac.mod"],
    cmd = "sed \"s|AM_INIT_AUTOMAKE(\[-Wall -Werror\])|AM_INIT_AUTOMAKE(\[-Wall\])|\" $< > $@",
)

genrule(
    name = "generated_headers",
    srcs = [":configure_ac_mod"] + glob([
        "autogen.sh",
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
    cmd = "mv $(location :configure_ac_mod) $$(dirname $(location autogen.sh))/configure.ac && \
    pushd $$(dirname $(location autogen.sh)) && \
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
