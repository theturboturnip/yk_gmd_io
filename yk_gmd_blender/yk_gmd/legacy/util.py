from typing import List, Tuple


def false_ranges_in(bools: List[bool]) -> List[Tuple[int, int]]:
    i = 1
    range_start = None
    false_ranges = []
    for i in range(1, len(bools)):
        if bools[i - 1] and not bools[i]:
            range_start = i
            # print(f"0x{i:06x}: Entering untouched range")
        elif bools[i] and not bools[i - 1]:
            false_ranges.append((range_start, i))
            range_start = None
            # print(f"0x{i:06x}: Exiting untouched range")
        i += 1

    if range_start is not None:
        false_ranges.append((range_start, len(bools)))

    return false_ranges