import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from logging_module import get_logger

logger = get_logger("")


def setup_parser(parser):
    subparsers = parser.add_subparsers(help="choose command")

    full_parser = subparsers.add_parser(
        "full_parser",
        help="full python code parser",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    full_parser.add_argument(
        "-n", "--nuclide",
        help="nuclide number need to start machine learning model",
        required=True,
        dest="nuclide",
        type=int,
    )

    full_parser.add_argument(
        "-t", "--temperature",
        help="temperature need to start machine learning model",
        required=True,
        dest="temperature",
        type=int,
    )

    full_parser.add_argument(
        "-m", "--metric",
        help="metric of model",
        dest="metric",
        type=str,
        default="accuracy",
    )


def parser():
    parser = ArgumentParser(
        description="parse arguments of model PLASMA",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    setup_parser(parser)
    arguments = parser.parse_args()
    return arguments