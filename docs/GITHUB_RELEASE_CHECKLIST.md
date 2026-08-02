# GitHub Release Checklist

1. Replace `USERNAME` in `CITATION.cff` and README badges.
2. Create a public repository named `DPT-Toolkit`.
3. Upload all files at repository root (not the enclosing folder).
4. Enable GitHub Actions and confirm tests pass on Python 3.10-3.12.
5. Create release `v1.0.0`; attach `DPT-Toolkit-v1.0.0.zip` and checksums.
6. Archive the GitHub release in Zenodo and add the DOI to README/CITATION.cff.
7. Protect the main branch and require tests before merge.
8. Use Issues for anchor revisions; never silently alter released scoring conventions.
