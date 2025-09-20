import os
import sys

from tree_sitter import Language

LIB_PATH = os.path.join("build", "java-languages.so")

JAVA_GRAMMAR_PATH = os.environ.get("TREE_SITTER_JAVA_PATH")

if not JAVA_GRAMMAR_PATH:
    print(
        "ERROR: define the TREE_SITTER_JAVA_PATH environment variable "
        "pointing to the tree-sitter-java repository"
    )
    sys.exit(1)


def main() -> None:
    os.makedirs("build", exist_ok=True)
    if JAVA_GRAMMAR_PATH:
        Language.build_library(LIB_PATH, [JAVA_GRAMMAR_PATH])
    print(f"Grammar compiled in {LIB_PATH}")
