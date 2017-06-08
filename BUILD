# Dummy rules

filegroup(
    name = "dummy_snappy_rule",
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

filegroup(
    name = "dummy_sqlite_rule",
    srcs = [
        # Some files are apparently not available on the sqlite.org web server in their expected place.
        # Might be worth looking into generating them from fossil
        "@sqlite_3_19_3//:sqlite",
        "@sqlite_3_19_2//:sqlite",
        "@sqlite_3_19_1//:sqlite",
        "@sqlite_3_19_0//:sqlite",
        "@sqlite_3_18_0//:sqlite",
        "@sqlite_3_17_0//:sqlite",
        "@sqlite_3_16_2//:sqlite",
        "@sqlite_3_16_1//:sqlite",
        "@sqlite_3_16_0//:sqlite",
        "@sqlite_3_15_2//:sqlite",
        "@sqlite_3_15_1//:sqlite",
        "@sqlite_3_15_0//:sqlite",
        "@sqlite_3_14_2//:sqlite",
        "@sqlite_3_14_1//:sqlite",
        "@sqlite_3_14//:sqlite",
        "@sqlite_3_13_0//:sqlite",
        "@sqlite_3_12_2//:sqlite",
        # "@sqlite_3_12_1//:sqlite",
        # "@sqlite_3_12_0//:sqlite",
        "@sqlite_3_11_1//:sqlite",
        "@sqlite_3_11_0//:sqlite",
        "@sqlite_3_10_2//:sqlite",
        "@sqlite_3_10_1//:sqlite",
        "@sqlite_3_10_0//:sqlite",
        # "@sqlite_3_9_3//:sqlite",
        "@sqlite_3_9_2//:sqlite",
        "@sqlite_3_9_1//:sqlite",
        "@sqlite_3_9_0//:sqlite",
    ],
)
