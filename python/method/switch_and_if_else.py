
# 只有在 case 中的条件是连续数字或相隔不大时，编译器会使用表结构做优化，性能优于 if-else。

# 其他情况下，switch-case 其实就是逐个分支判断，性能与 if-else 无异。

# switch-case 中的 case 只能是常量，而 if-else 用途更广一些，本文仅讨论分支是常量的情况。