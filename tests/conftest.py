from typing import Any, List
import pytest
import subprocess
import urllib.request

NO_SKIP_OPTION = "--no-skip"


def pytest_addoption(parser):
    parser.addoption(
        NO_SKIP_OPTION,
        action="store_true",
        default=False,
        help="also run skipped tests",
    )


def pytest_collection_modifyitems(config, items: List[Any]):
    if config.getoption(NO_SKIP_OPTION):
        for test in items:
            test.own_markers = [
                marker
                for marker in test.own_markers
                if marker.name not in ("skip", "skipif")
            ]


@pytest.fixture(scope="session")
def orca_executable(tmpdir_factory):
    orca_path = tmpdir_factory.mktemp("orca")
    source_path = orca_path.join("orca.cpp")
    executable_path = orca_path.join("orca")
    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/thocevar/orca/e146a8b1a99a90f5e3096b7bcc2ab0ea246c3ca7/orca.cpp",
        source_path,
    )
    subprocess.run(
        ["g++", "-O2", "-std=c++11", "-o", str(executable_path), str(source_path)]
    )
    return executable_path
