import parse

def countSubstring(string, substring):
    count = 0
    start = 0

    # Search through the string until we reach the end of it.
    while start < len(string):
        # Check if a substring is present from start until the end.
        pos = string.find(substring, start)

        if pos != -1:
            # If a substring is present, move start to the next position from start of the substring.
            start = pos + 1

            # Increment the count
            count += 1
        else:
            # If no further substring is present
            break
    # return the value of count
    return count