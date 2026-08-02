from __future__ import annotations
import argparse, json, shutil
from pathlib import Path
from .workflow import run_workflow
from .anchors import ANCHORS, DOMAIN_NOTES

def main():
    p = argparse.ArgumentParser(prog="dpt", description="DPT Toolkit — auditable 30-step research-question screening")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("project")
    r.add_argument("-o", "--out", default="dpt-results")
    a = sub.add_parser("anchors")
    a.add_argument("--domain", default="generic")
    a.add_argument("--json", action="store_true")
    i = sub.add_parser("init")
    i.add_argument("directory", nargs="?", default="my-dpt-project")
    args = p.parse_args()
    if args.cmd == "run":
        rep = run_workflow(args.project, args.out)
        print(f"Completed 30-step DPT audit. Selected: {[x['id'] for x in rep['selected']]}. Results: {args.out}")
    elif args.cmd == "anchors":
        if args.json:
            print(json.dumps({"anchors": ANCHORS, "domain_note": DOMAIN_NOTES.get(args.domain, DOMAIN_NOTES["generic"])}, indent=2))
        else:
            print("Domain note:", DOMAIN_NOTES.get(args.domain, DOMAIN_NOTES["generic"]))
            for component, rows in ANCHORS.items():
                print("\n" + component.upper())
                for item in rows:
                    print(f" {item['score']}: {item['label']} — {item['anchor']}")
    elif args.cmd == "init":
        d = Path(args.directory)
        d.mkdir(parents=True, exist_ok=True)
        src = Path(__file__).resolve().parents[2] / "examples" / "energy_case" / "project.yaml"
        if src.exists():
            shutil.copy(src, d / "project.yaml")
        else:
            (d / "project.yaml").write_text("project:\n  title: My DPT Project\n", encoding="utf-8")
        print("Created", d)

if __name__ == "__main__":
    main()
