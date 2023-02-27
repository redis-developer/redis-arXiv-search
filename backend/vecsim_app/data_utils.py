import json
import re


def _process(paper: dict, year_pattern: str):
    paper = json.loads(paper)
    if paper["journal-ref"]:
        years = [int(year) for year in re.findall(year_pattern, paper["journal-ref"])]
        years = [year for year in years if (year <= 2022 and year >= 1991)]
        year = min(years) if years else None
    else:
        year = None
    return {
        "id": paper["id"],
        "title": paper["title"],
        "year": year,
        "authors": paper["authors"],
        "categories": ",".join(paper["categories"].split(" ")),
        "abstract": paper["abstract"],
    }


def papers(
    data_path: str, year_cutoff: int, year_pattern: str, ml_category: str = None
):
    with open(data_path, "r") as f:
        for paper in f:
            paper = _process(paper, year_pattern)
            if paper["year"]:
                m = ml_category
                ml_category_condition = (
                    m is not None and m in paper["categories"] or m is None
                )
                if paper["year"] >= year_cutoff and ml_category_condition:
                    yield paper
