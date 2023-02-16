__version__ = "{{ cookiecutter.semantic_version }}"

# keep this ``if __name__ == "__main__"``, don't delete!
# this is used by automation script to detect the project version
if __name__ == "__main__":  # pragma: no cover
    print(__version__)
