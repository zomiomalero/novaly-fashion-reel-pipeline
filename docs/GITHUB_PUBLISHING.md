# Publishing the finished pipeline to a new GitHub repository

The archive is intentionally self-contained. The GitHub connector used during development could read the source repository and discover the authenticated account, but did not expose a **create-repository operation**, so it could not publish a new repository autonomously. Do not mistake a proposed URL for an existing live repository.

Suggested repository name: `novaly-fashion-reel-pipeline`.
Requested visibility: `public`. Review all contents before running the publisher: everything committed will be visible to anyone.

## One-time steps on your Mac

1. Extract the **public-ready V2** ZIP (not the full offline/private research ZIP) to your preferred drive.
2. If necessary, install Git and the GitHub CLI: `brew install git gh`.
3. Run `gh auth login` and complete browser authorization. Verify with `gh auth status`.
4. Inside the extracted folder, execute:

```bash
./scripts/publish_to_github.sh novaly-fashion-reel-pipeline zomiomalero
```

The helper initializes a Git repo if absent, stages source and docs, blocks private reference folders, all video/audio source media, and any image outside the two approved original study-asset folders, commits, then creates a new **public** repository in the specified authenticated account and pushes `main`. It refuses to overwrite an existing `origin` remote.

The helper uses GitHub's command-line authentication; do not paste tokens or passwords into chat, scripts or environment files. It configures local Git author information from your GitHub account if none is set, using your GitHub no-reply email.

The public URL after a successful push will be `https://github.com/zomiomalero/novaly-fashion-reel-pipeline`. It is **not live** until `gh repo create` succeeds.

## If you prefer the website

Create a **new empty public repository** named `novaly-fashion-reel-pipeline` at GitHub. Extract the ZIP locally and push using normal Git commands or GitHub Desktop. Do not upload the ZIP itself as a single file and expect GitHub to unpack a usable source tree.

## Keeping private reference files private

The **public-ready** repository ZIP contains original procedural textile studies and original technical diagram plates, but no uploaded Facebook/other reference MP4 files, no downloaded-reference frames, no real-person model identity photographs and no credentials. The **full offline** ZIP deliberately includes a `private_reference_lab/` with source-derived contact sheets and keyframes; do not push that folder or upload it into a public AI context. A separate personal local analysis folder may be retained for study. Do not add that folder or final generated footage to the code repository without reviewing licensing, likeness and permission.
