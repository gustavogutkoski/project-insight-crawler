import argparse

from runner import run_crawler


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the Java project crawler and extract class/method information."
    )
    parser.add_argument("project_path", type=str, help="Path to the Java project directory")

    args = parser.parse_args()

    run_crawler(args.project_path)


if __name__ == "__main__":
    main()
