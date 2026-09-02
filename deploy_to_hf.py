"""Hugging Face Model Hub Automated Deployer & Packager.

Features:
1. Automated ZIP bundle packaging (aloha_sim_bundle.zip)
2. Hugging Face Model Hub creation and clean asset uploading (filtering dev/governance docs)
3. Model Card (README.md) synchronization with Hwihwa-Lab metadata

Usage:
  python deploy_to_hf.py --repo_name aloha-14dof-transfer-cube
  python deploy_to_hf.py --bundle_only  # Just create the ZIP bundle
"""

import os
import sys
import zipfile
import argparse
from pathlib import Path
from huggingface_hub import HfApi

def create_bundle(root_dir: Path, output_zip: Path):
    """Packages all core simulation and model assets into a clean ZIP archive."""
    print(f"\n[*] Creating production bundle archive: {output_zip.name} ...")
    
    include_files = [
        "aloha_env.py",
        "policy_runner.py",
        "metrics_tracker.py",
        "telemetry_hud.py",
        "run_aloha_sim.py",
        "requirements.txt",
        "README.md",
        "README_KR.md",
        "LICENSE"
    ]
    
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f_name in include_files:
            file_path = root_dir / f_name
            if file_path.exists():
                zipf.write(file_path, arcname=f_name)
                print(f"  + Added: {f_name}")
            else:
                print(f"  ! Warning: {f_name} not found, skipping.")

    size_kb = output_zip.stat().st_size / 1024
    print(f"[OK] Production bundle created: {output_zip.name} ({size_kb:.1f} KB)")

def parse_args():
    parser = argparse.ArgumentParser(description="Aloha 14-DOF LeRobot Hugging Face Deployer")
    parser.add_argument("--repo_name", type=str, default="act-aloha-sim-transfer-cube", help="Hugging Face repo name")
    parser.add_argument("--repo_type", type=str, default="model", choices=["model", "dataset", "space"])
    parser.add_argument("--token", type=str, default=None, help="Hugging Face API token (or uses cached login)")
    parser.add_argument("--private", action="store_true", help="Set repository to private")
    parser.add_argument("--bundle_only", action="store_true", help="Only create ZIP bundle without uploading")
    return parser.parse_args()

def main():
    args = parse_args()
    root_dir = Path(__file__).resolve().parent
    bundle_zip_path = root_dir / "aloha_sim_bundle.zip"

    # Step 1: Create ZIP bundle
    create_bundle(root_dir, bundle_zip_path)

    if args.bundle_only:
        print("\n[COMPLETE] Bundle created successfully (--bundle_only mode).")
        return

    # Step 2: Authenticate with Hugging Face Hub
    print("\n" + "=" * 65)
    print("  Aloha 14-DOF LeRobot // Hugging Face Deployment Pipeline")
    print("=" * 65)

    try:
        api = HfApi(token=args.token)
        user_info = api.whoami()
        username = user_info["name"]
    except Exception as e:
        print(f"[ERROR] Hugging Face authentication failed: {e}")
        print("Tip: Run 'huggingface-cli login' or pass --token YOUR_TOKEN")
        sys.exit(1)

    repo_id = f"{username}/{args.repo_name}"
    print(f" [*] Target User : {username}")
    print(f" [*] Repo ID     : {repo_id}")
    print(f" [*] Repo Type   : {args.repo_type}")
    print(f" [*] Visibility  : {'Private' if args.private else 'Public'}")
    print("=" * 65)

    # Step 3: Create or connect to repository
    try:
        print(f"\n[1/2] Connecting/Creating repository on Hugging Face: {repo_id} ...")
        repo_url = api.create_repo(
            repo_id=repo_id,
            repo_type=args.repo_type,
            private=args.private,
            exist_ok=True
        )
        print(f"  --> Repository ready: {repo_url}")
    except Exception as e:
        print(f"[ERROR] Repository creation failed: {e}")
        sys.exit(1)

    # Step 4: Upload project assets (filtering out internal dev/AI docs)
    print(f"\n[2/2] Uploading simulation assets and bundle to {repo_id} ...")

    ignore_patterns = [
        "__pycache__/*",
        "*.pyc",
        ".git/*",
        ".gitignore",
        ".venv/*",
        "venv/*",
        "env/*",
        "*.log",
        ".system_generated/*",
        ".cursor/*",
        ".cursorrules*",
        ".agents/*",
        "DOCS_*",
        "MEMORY.md",
        ".vscode/*",
        "*.tmp",
        "*.tmp.md"
    ]

    try:
        api.upload_folder(
            folder_path=str(root_dir),
            repo_id=repo_id,
            repo_type=args.repo_type,
            ignore_patterns=ignore_patterns,
            commit_message="feat: upload Aloha 14-DOF MuJoCo simulator, ACT policy, HUD and production bundle"
        )
        print("  --> All assets uploaded successfully!")
    except Exception as e:
        print(f"[ERROR] File upload failed: {e}")
        sys.exit(1)

    print("\n" + "=" * 65)
    print("  DEPLOYMENT COMPLETED SUCCESSFULLY!")
    print("=" * 65)
    print(f"  Hugging Face URL: https://huggingface.co/{repo_id}")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    main()
