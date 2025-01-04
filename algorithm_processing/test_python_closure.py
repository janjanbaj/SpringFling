def f1():
    success = False

    def f2():
        success = True
        print(success)

    print(success)
    f2()
    print(success)


def f3(success):
    success = True
    return success


# f1()

success = False
print(success)
f3(success)
print(success)
