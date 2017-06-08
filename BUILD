# Dummy rule

filegroup(
    name = "dummy_rule",
    srcs = [
        "@snappy_1_1_4//:snappy",
        "@snappy_1_1_3//:snappy",
        "@snappy_1_1_2//:snappy",
        "@snappy_1_1_1//:snappy",
        "@snappy_1_1_0//:snappy",

        # 1.0.5 and earlier:
        # The following line in configure.ac is problematic:
        # AM_INIT_AUTOMAKE([-Wall -Werror])
        # The -Werror part means the warning
        # "warning: 'libsnappy.la': linking libtool libraries using a non-POSIX archiver requires 'AM_PROG_AR' in 'configure.ac'"
        # makes the whole build fail

        # This is fixed by removing the option via sed
        "@snappy_1_0_5//:snappy",
        "@snappy_1_0_4//:snappy",
        "@snappy_1_0_3//:snappy",
        "@snappy_1_0_2//:snappy",
        "@snappy_1_0_1//:snappy",
    ],
)
