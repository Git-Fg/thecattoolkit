import argparse
import sys

try:
    from gitingest import ingest
except ImportError:
    print(
        "Error: gitingest not installed. Run with 'uv run --with gitingest scripts/ingest.py ...'"
    )
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Ingest a git repository into a structured digest."
    )
    parser.add_argument("source", help="URL or local path of the repository")
    parser.add_argument("--include", "-i", action="append", help="Include patterns")
    parser.add_argument("--exclude", "-e", action="append", help="Exclude patterns")
    parser.add_argument("--max-size", "-s", type=int, help="Maximum file size in bytes")

    args = parser.parse_args()

    # Construct kwargs for ingest function
    # Note: gitingest API signature might vary, assuming standard usage based on documentation.
    # If API differs, this script acts as a reference implementation.

    try:
        if args.source.startswith("http") or args.source.startswith("git@"):
            # Remote ingestion
            summary, tree, content = ingest(
                args.source,
                include_patterns=args.include,
                exclude_patterns=args.exclude,
                max_file_size=args.max_size,
            )
        else:
            # Local ingestion (if supported by library, otherwise might need adaptation)
            summary, tree, content = ingest(
                args.source,
                include_patterns=args.include,
                exclude_patterns=args.exclude,
                max_file_size=args.max_size,
            )

        print(summary)
        print(tree)
        print(content)

    except Exception as e:
        print(f"Error executing ingestion: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
