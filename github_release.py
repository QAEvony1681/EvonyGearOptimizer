"""
github_release.py — Upload a new release to GitHub.

Run this from the evony_tool folder AFTER completing both build steps:
    1. py -3.11 -m PyInstaller evony_tool.spec --clean
    2. Inno Setup compile of evony_installer.iss

Usage:
    py -3.11 github_release.py               # full release (new version)
    py -3.11 github_release.py --data-only   # update data file only, no new release

What it does:
    1. Reads the current version from app.py
    2. Creates a GitHub Release tagged v{version}
    3. Uploads the installer .exe as a release asset
    4. Uploads evony_data.xlsx to the main branch (so data auto-sync works)
    5. Prints the release URL when done

Requirements:
    py -3.11 -m pip install requests PyGithub

You will be prompted for your GitHub Personal Access Token on first run.
The token is saved to token.txt in this folder (never committed to GitHub).
"""

import os
import sys
import re
import json

GITHUB_USER  = 'QAEvony1681'
GITHUB_REPO  = 'EvonyGearOptimizer'
TOKEN_FILE   = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token.txt')
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))

# Set to True if your repo is private.
# Release assets (installer .exe) are always publicly downloadable
# even from private repos when linked directly.
# The data file URL must be public for the app's silent sync to work —
# if the repo is private, we upload the data file as a release ASSET
# instead of committing it to the main branch.
PRIVATE_REPO = True


def get_version():
    """Read current version from app.py."""
    app_py = os.path.join(SCRIPT_DIR, 'app.py')
    with open(app_py) as f:
        for line in f:
            m = re.search(r"APP_VERSION\s*=\s*'([^']+)'", line)
            if m:
                return m.group(1)
    raise RuntimeError("Could not find APP_VERSION in app.py")


def get_token():
    """Load token from file, or prompt user and save it."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            token = f.read().strip()
        if token:
            return token

    print()
    print("=" * 60)
    print("  GitHub Personal Access Token required")
    print("=" * 60)
    print()
    print("To create a token:")
    print("  1. Go to github.com → Settings → Developer settings")
    print("  2. Personal access tokens → Tokens (classic)")
    print("  3. Generate new token (classic)")
    print("  4. Give it a name like 'EvonyGearOptimizer'")
    print("  5. Check: repo (full control)")
    print("  6. Click Generate token")
    print("  7. Copy the token (starts with ghp_...)")
    print()
    token = input("Paste your token here: ").strip()
    if not token:
        raise RuntimeError("No token provided.")

    with open(TOKEN_FILE, 'w') as f:
        f.write(token)
    print(f"Token saved to {TOKEN_FILE}")
    print("(Keep this file private — do not share or commit it)")
    return token


def find_installer(version):
    """Find the installer .exe in installer_output/."""
    out_dir = os.path.join(SCRIPT_DIR, 'installer_output')
    expected = f'EvonyGearOptimizer_v{version}_Setup.exe'
    path = os.path.join(out_dir, expected)
    if os.path.exists(path):
        return path
    # Try any .exe in the folder
    if os.path.isdir(out_dir):
        exes = [f for f in os.listdir(out_dir) if f.endswith('.exe')]
        if exes:
            chosen = os.path.join(out_dir, sorted(exes)[-1])
            print(f"Warning: expected {expected}, using {exes[-1]} instead")
            return chosen
    raise FileNotFoundError(
        f"Installer not found at {path}\n"
        f"Make sure you have compiled evony_installer.iss with Inno Setup first."
    )


def main():
    print()
    print("Evony Gear Optimizer — GitHub Release Script")
    print("=" * 50)

    # Check dependencies
    try:
        import requests
        from github import Github, GithubException
    except ImportError:
        print("Installing required packages...")
        os.system(f'"{sys.executable}" -m pip install requests PyGithub')
        import requests
        from github import Github, GithubException

    try:
        version = get_version()
    except Exception as e:
        print(f"ERROR reading version from app.py: {e}")
        print("Make sure you are running this from the evony_tool folder.")
        sys.exit(1)

    tag = f'v{version}'
    print(f"Version:    {version}")
    print(f"Tag:        {tag}")
    print(f"Repository: {GITHUB_USER}/{GITHUB_REPO}")
    print(f"Private:    {PRIVATE_REPO}")
    print()

    token = get_token()
    print()

    # Connect to GitHub
    print("Connecting to GitHub...")
    try:
        g    = Github(token)
        user = g.get_user()
        print(f"Authenticated as: {user.login}")
    except Exception as e:
        print(f"ERROR: Authentication failed: {e}")
        print("Your token may be invalid or expired.")
        print("Delete token.txt and run the script again to re-enter your token.")
        sys.exit(1)

    print(f"Getting repository {GITHUB_USER}/{GITHUB_REPO}...")
    try:
        repo = g.get_repo(f'{GITHUB_USER}/{GITHUB_REPO}')
        print(f"Connected: {repo.full_name}")
    except Exception as e:
        print(f"ERROR: Could not access repository: {e}")
        print(f"Check that '{GITHUB_REPO}' exists under account '{GITHUB_USER}'.")
        sys.exit(1)

    # Check for existing release with this tag
    try:
        existing = repo.get_release(tag)
        overwrite = input(
            f"\nRelease {tag} already exists. Overwrite? (y/n): "
        ).strip().lower()
        if overwrite != 'y':
            print("Aborted.")
            return
        print(f"Deleting existing release {tag}...")
        existing.delete_release()
        # Also delete the tag
        try:
            ref = repo.get_git_ref(f'tags/{tag}')
            ref.delete()
        except Exception:
            pass
    except Exception:
        pass   # No existing release — good

    # Find installer
    print("Looking for installer...")
    try:
        installer_path = find_installer(version)
        installer_name = os.path.basename(installer_path)
        installer_size = os.path.getsize(installer_path)
        print(f"Installer: {installer_name} ({installer_size/1024/1024:.1f} MB)")
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # Upload evony_data.xlsx
    data_path = os.path.join(SCRIPT_DIR, 'evony_data.xlsx')
    if os.path.exists(data_path):
        with open(data_path, 'rb') as f:
            data_bytes = f.read()

        if PRIVATE_REPO:
            # Private repo: data file will be uploaded as a release asset below.
            # The app's GITHUB_DATA_URL must point to the release asset URL.
            # We handle this after creating the release.
            print("Private repo: evony_data.xlsx will be uploaded as a release asset")
            _data_bytes_for_release = data_bytes
        else:
            # Public repo: commit to main branch so raw URL works for silent sync
            print("Uploading evony_data.xlsx to main branch...")
            try:
                existing_file = repo.get_contents('evony_data.xlsx', ref='main')
                repo.update_file(
                    path='evony_data.xlsx', message=f'Update data file for {tag}',
                    content=data_bytes, sha=existing_file.sha, branch='main')
                print("  evony_data.xlsx updated on main branch")
            except Exception:
                try:
                    repo.create_file(
                        path='evony_data.xlsx', message=f'Add data file for {tag}',
                        content=data_bytes, branch='main')
                    print("  evony_data.xlsx created on main branch")
                except Exception as e:
                    print(f"  Warning: could not upload data file: {e}")
            _data_bytes_for_release = None
    else:
        print("Warning: evony_data.xlsx not found — skipping data upload")
        _data_bytes_for_release = None

    # Ensure repo has at least one commit (GitHub requires this before releases)
    print("Checking repository state...")
    try:
        list(repo.get_commits())
    except Exception:
        print("Repository is empty — creating initial commit...")
        for branch in ('main', 'master'):
            try:
                repo.create_file(
                    path    = 'README.md',
                    message = 'Initial commit',
                    content = f'# Evony Gear Optimizer\n\nSee Releases tab for downloads.',
                    branch  = branch,
                )
                print(f"  Initial commit created on {branch} branch OK")
                break
            except Exception as e:
                continue

    # Create the release
    print(f"\nCreating GitHub release {tag}...")
    release_notes = f"""## Evony Gear Optimizer {tag}

### Installation
Download and run `{installer_name}` to install or upgrade.
The installer will preserve your existing gear data and settings.

### What's New
See the full changelog in the repository README.
"""
    release = repo.create_git_release(
        tag     = tag,
        name    = f'Evony Gear Optimizer {tag}',
        message = release_notes,
        draft   = False,
        prerelease = False,
    )
    print(f"  Release created: {release.html_url}")

    # Upload the installer
    print(f"Uploading {installer_name} ({installer_size/1024/1024:.1f} MB)...")
    with open(installer_path, 'rb') as f:
        release.upload_asset(
            path         = installer_path,
            label        = installer_name,
            content_type = 'application/octet-stream',
        )
    print("  Upload complete!")

    # For public repos: also upload data file as release asset
    # (always upload regardless of PRIVATE_REPO since we're now public)
    if _data_bytes_for_release is not None:
        import tempfile, shutil as _su
        print("Uploading evony_data.xlsx as release asset...")
        tmp_dir3 = tempfile.mkdtemp()
        tmp_data = os.path.join(tmp_dir3, 'evony_data.xlsx')
        with open(tmp_data, 'wb') as f:
            f.write(_data_bytes_for_release)
        try:
            asset = release.upload_asset(
                path=tmp_data,
                label='evony_data.xlsx',
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
            print(f"  evony_data.xlsx uploaded ({asset.size:,} bytes)")
            print(f"  Asset name on GitHub: {asset.name}")
        finally:
            _su.rmtree(tmp_dir3, ignore_errors=True)

    print()
    print("=" * 60)
    print(f"  Release {tag} published successfully!")
    print(f"  URL: {release.html_url}")
    print("=" * 60)
    print()
    if PRIVATE_REPO:
        print("NOTE: Your repository is private.")
        print("Share the release URL directly with your users.")
        print()
        print("IMPORTANT: For data auto-sync to work from a private repo,")
        print("update GITHUB_DATA_URL in app.py to point to the release asset URL.")
        print("The asset URL looks like:")
        print(f"  https://github.com/{GITHUB_USER}/{GITHUB_REPO}/releases/download/{tag}/evony_data.xlsx")
        print()
        print("This only needs updating if the data sync URL has changed.")
    else:
        print("Users running v1.2.0+ will be notified of this update")
        print("on their next startup check (within 7 days or 10 startups).")
        print()
        print("The updated evony_data.xlsx is now live on the main branch.")
        print("Installed apps will sync it silently on next startup.")


def data_only():
    """Upload just evony_data.xlsx to GitHub — no new release created."""
    print()
    print("Evony Gear Optimizer — Data File Update")
    print("=" * 50)

    try:
        import requests
        from github import Github
    except ImportError:
        print("Installing required packages...")
        os.system(f'"{sys.executable}" -m pip install requests PyGithub')
        from github import Github

    token = get_token()
    print()

    print("Connecting to GitHub...")
    try:
        g    = Github(token)
        repo = g.get_repo(f'{GITHUB_USER}/{GITHUB_REPO}')
        print(f"Connected: {repo.full_name}")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    data_path = os.path.join(SCRIPT_DIR, 'evony_data.xlsx')
    if not os.path.exists(data_path):
        print(f"ERROR: evony_data.xlsx not found at {data_path}")
        sys.exit(1)

    with open(data_path, 'rb') as f:
        data_bytes = f.read()

    # Step 1: Update main branch
    print("\nUpdating evony_data.xlsx on main branch...")
    try:
        existing = repo.get_contents('evony_data.xlsx', ref='main')
        repo.update_file(
            path    = 'evony_data.xlsx',
            message = 'Update gear data',
            content = data_bytes,
            sha     = existing.sha,
            branch  = 'main',
        )
        print("  Main branch updated OK")
    except Exception as e:
        try:
            repo.create_file(
                path    = 'evony_data.xlsx',
                message = 'Add gear data',
                content = data_bytes,
                branch  = 'main',
            )
            print("  Created on main branch OK")
        except Exception as e2:
            print(f"  WARNING: Could not update main branch: {e2}")

    # Step 2: Update the release asset on the latest release
    print("Updating evony_data.xlsx on latest release...")
    try:
        release = repo.get_latest_release()
        print(f"  Found release: {release.tag_name}")

        # Remove existing data asset if present
        for asset in release.get_assets():
            if asset.name == 'evony_data.xlsx':
                asset.delete_asset()
                print("  Removed old asset")
                break

        # Upload new asset
        import tempfile, shutil as _shutil2
        tmp_dir2 = tempfile.mkdtemp()
        tmp      = os.path.join(tmp_dir2, 'evony_data.xlsx')
        with open(tmp, 'wb') as f:
            f.write(data_bytes)
        try:
            uploaded = release.upload_asset(
                path         = tmp,
                label        = 'evony_data.xlsx',
                content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
            print(f"  New asset uploaded OK ({uploaded.size:,} bytes)")
            print(f"  Download URL: {uploaded.browser_download_url}")
        finally:
            _shutil2.rmtree(tmp_dir2, ignore_errors=True)

    except Exception as e:
        print(f"  WARNING: Could not update release asset: {e}")
        print("  The main branch was still updated.")
        print("  Run the full release script to properly attach the data file.")

    print()
    print("=" * 50)
    print("  Data file updated successfully!")
    print("  Installed apps will sync it silently on next startup.")
    print("=" * 50)


if __name__ == '__main__':
    try:
        if '--data-only' in sys.argv:
            data_only()
        else:
            main()
    except KeyboardInterrupt:
        print("\nCancelled.")
    except SystemExit:
        raise
    except Exception as e:
        print()
        print(f"UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        print()
        print("Please share the above error when reporting this issue.")
    input("\nPress Enter to close...")
