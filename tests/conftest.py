import pytest
import subprocess
import urllib.request


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
