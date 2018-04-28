import argparse
import timeit

parser = argparse.ArgumentParser(description="Find the nth fibonacci numbers.",
                                 usage="fib.py -n <nth> [-c]")
parser.add_argument("-n", "--number", default=100, type=int, required=False, help="nth fibonacci number to calculate")
parser.add_argument("-c", "--clean", help="Not displaying the fibonachi number", action="store_true")


def fib_recursive(number):
    if number <= 1:
        return number
    else:
        return fib(number - 1) + fib(number - 2)


def fib(number):
    cur, next = 0, 1;
    for i in range(number):
        cur, next = next, cur + next;
    return cur


def main(args):
    impls = (fib, fib_recursive)
    for impl in impls:
        print("Using {} to calculate the {}th fibonacci number ...".format(impl.__name__, args.number))
        start = timeit.default_timer()
        nth = impl(args.number)
        stop = timeit.default_timer()
        if not args.clean:
            print("The {}th fibonacci number is {}".format(args.number, nth))
        print("Toal time taken: {}\n".format(stop - start))


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
