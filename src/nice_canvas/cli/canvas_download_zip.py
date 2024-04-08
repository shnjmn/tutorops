import json
import os
from pathlib import Path


def parse_args():
    from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

    from nice_canvas.api import get_config_file

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=get_config_file(),
        help="config file for nice_canvas",
    )
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        required=True,
        help="https://canvas.nus.edu.sg/courses/:course_id/assignments/:id",
    )
    parser.add_argument(
        "-d",
        "--output",
        type=Path,
        default=Path("repo-zip"),
        help="directory to save zip files",
    )
    parser.add_argument(
        "-j",
        "--json",
        type=Path,
        default=Path("metainfo.json"),
        help="json file to save meta info",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="execute aria2c in quiet mode",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        default=False,
        help="execute aria2c in dry-run mode",
    )

    return parser.parse_args()


def parse_url(url: str):
    from urllib.parse import urlparse

    parsed = urlparse(url)
    parts = parsed.path.split("/")
    course_id = parts[2]
    assignment_id = parts[4]
    return {
        "course_id": int(course_id),
        "assignment_id": int(assignment_id),
    }


def main():
    from nice_canvas.api import Canvas, get_client
    from rich.progress import track

    args = parse_args()

    canvas = Canvas(http=get_client(args.config), **parse_url(args.url))

    repo = args.output
    if not repo.is_dir():
        repo.mkdir(exist_ok=True)

    aria_file = repo / ".index.aria2"

    data = []

    for sub in track(
        canvas.submissions.index(user=True),
        description="Fetching submission info from Canvas...",
    ):
        submission_history = max(sub["submission_history"], key=lambda h: h["attempt"])
        if not submission_history["submission_type"]:
            continue

        attachments = submission_history["attachments"]
        assert len(attachments) == 1
        attachment = attachments[0]

        meta = {
            "name": sub["user"]["sortable_name"],
            "matric_no": sub["user"]["integration_id"],
            "nusnet_id": sub["user"]["login_id"],
            "user_id": sub["user_id"],
            "submission_id": submission_history["id"],
            "attachment_id": attachment["id"],
        }

        file = canvas.files.show(attachment["id"])
        assert file["content-type"] in (
            "application/x-zip-compressed",
            "application/zip",
        ), file

        filename = "{}.zip".format(meta["matric_no"])
        with open(aria_file, "a") as fp:
            fp.write(
                "\n".join(
                    [
                        file["url"],
                        f"  out={filename}",
                        f"  dir={repo.absolute()}",
                    ]
                )
            )
            fp.write("\n\n")

        data.append(meta)

    with open(args.json, "w") as fp:
        json.dump(data, fp, indent=2)

    os.execlp(
        "aria2c",
        "aria2c",
        "--input-file",
        aria_file,
        "--quiet" if args.quiet else "",
        "--dry-run" if args.dry_run else "",
    )


if __name__ == "__main__":
    main()
