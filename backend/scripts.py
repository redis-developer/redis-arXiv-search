import subprocess


def load_data():
    subprocess.run(["python", "-m", "arxivsearch.db.load"], check=True)


def start_app():
    # load data
    subprocess.run(["python", "-m", "arxivsearch.db.load"], check=True)
    # start app
    subprocess.run(
        ["uvicorn", "arxivsearch.main:app", "--port", "8888", "--host", "0.0.0.0"],
        check=True,
    )
    # subprocess.run(["python", "-m", "arxivsearch.main"], check=True)


def format():
    subprocess.run(
        ["isort", "./arxivsearch", "./tests/", "--profile", "black"], check=True
    )
    subprocess.run(["black", "./arxivsearch"], check=True)


def check_format():
    subprocess.run(["black", "--check", "./arxivsearch"], check=True)


def sort_imports():
    subprocess.run(
        ["isort", "./arxivsearch", "./tests/", "--profile", "black"], check=True
    )


def check_sort_imports():
    subprocess.run(
        ["isort", "./arxivsearch", "--check-only", "--profile", "black"], check=True
    )


def check_lint():
    subprocess.run(["pylint", "--rcfile=.pylintrc", "./arxivsearch"], check=True)


def mypy():
    subprocess.run(["python", "-m", "mypy", "./arxivsearch"], check=True)


def test():
    subprocess.run(
        ["python", "-m", "pytest", "arxivsearch", "--log-level=CRITICAL"], check=True
    )


def test_cov():
    subprocess.run(
        [
            "python",
            "-m",
            "pytest",
            "-vv",
            "--cov=./arxivsearch",
            "--cov-report=xml",
            "--log-level=CRITICAL",
        ],
        check=True,
    )


def cov():
    subprocess.run(["coverage", "html"], check=True)
    print("If data was present, coverage report is in ./htmlcov/index.html")
