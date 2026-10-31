#!/usr/bin/env python3
"""Create labels, milestones and issues from tools/issues.yaml.

Requires `gh` authenticated as a user who can write to the repo. The cloud
agent token used when the repo was set up could not (HTTP 403), which is why
docs/roadmap.md exists.

The script is safe to re-run: existing labels, milestones and issue titles
are left alone.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YAML_PATH = os.path.join(ROOT, "tools", "issues.yaml")
REPO = os.environ.get("GITHUB_REPO", "rastermanden/openCycloComputer")


def gh(*args, input_text=None):
    result = subprocess.run(
        ["gh", *args],
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(message or f"gh {' '.join(args)} failed")
    return result.stdout


def existing_labels():
    raw = gh("label", "list", "--repo", REPO, "--limit", "200", "--json", "name")
    return {item["name"] for item in json.loads(raw)}


def existing_milestones():
    raw = gh("api", f"repos/{REPO}/milestones?state=all&per_page=100")
    return {item["title"]: item["number"] for item in json.loads(raw)}


def existing_issue_titles():
    titles = set()
    page = 1
    while True:
        raw = gh(
            "issue",
            "list",
            "--repo",
            REPO,
            "--state",
            "all",
            "--limit",
            "100",
            "--page",
            str(page),
            "--json",
            "title",
        )
        batch = json.loads(raw)
        if not batch:
            break
        titles.update(item["title"] for item in batch)
        if len(batch) < 100:
            break
        page += 1
    return titles


def main():
    with open(YAML_PATH, encoding="utf-8") as handle:
        doc = yaml.safe_load(handle)

    print(f"Repo: {REPO}")
    have_labels = existing_labels()
    for label in doc["labels"]:
        if label["name"] in have_labels:
            print(f"label exists: {label['name']}")
            continue
        gh(
            "label",
            "create",
            label["name"],
            "--repo",
            REPO,
            "--color",
            label["color"],
            "--description",
            label["description"],
        )
        print(f"label created: {label['name']}")

    have_milestones = existing_milestones()
    for milestone in doc["milestones"]:
        if milestone["title"] in have_milestones:
            print(f"milestone exists: {milestone['title']}")
            continue
        created = json.loads(
            gh(
                "api",
                f"repos/{REPO}/milestones",
                "-f",
                f"title={milestone['title']}",
                "-f",
                f"description={milestone['description']}",
                "-f",
                "state=open",
            )
        )
        have_milestones[milestone["title"]] = created["number"]
        print(f"milestone created: {milestone['title']} -> {created.get('html_url', created['number'])}")

    have_titles = existing_issue_titles()
    for item in doc["issues"]:
        if item["title"] in have_titles:
            print(f"issue exists: {item['title']}")
            continue
        if item["milestone"] not in have_milestones:
            raise SystemExit(f"missing milestone {item['milestone']}")
        args = [
            "issue",
            "create",
            "--repo",
            REPO,
            "--title",
            item["title"],
            "--body",
            item["body"],
            "--milestone",
            item["milestone"],
        ]
        for label in item["labels"]:
            args.extend(["--label", label])
        url = gh(*args).strip()
        print(f"issue created: {url}")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as exc:
        print(f"Stopped: {exc}", file=sys.stderr)
        print(
            "Kunne ikke skrive til GitHub. Backloggen ligger i tools/issues.yaml og docs/roadmap.md.",
            file=sys.stderr,
        )
        sys.exit(1)
