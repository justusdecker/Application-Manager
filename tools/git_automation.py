import os, subprocess, sys
def run_git_command(command_list):
    """Runs a git command and returns the output."""
    try:
        result = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            check=False,
            cwd=os.getcwd()
        )
        return result.stdout.strip() + result.stderr.strip(), result.returncode
    except FileNotFoundError:
        err("Error: 'git' command not found. Ensure Git is installed and in your PATH.")
        exit(1)
def err(text: str) -> str:
    return f'\033[33m{text}\033[0m'
def custom_rules(fp: str) -> bool:
    fp = fp.replace('\\','/')
    print(fp)
    if fp == 'src/version.py':
        return '[auto] update version'
    if fp == 'docs/auto-docs.md':
        return '[auto] update docs'
    if fp == 'docs/docs-progress.md':
        return '[auto] update doc-progress'

def main():
    for root, _, files in os.walk(os.getcwd()):
        if '.git' in root:
            
            continue
                
        for file_name in files:
            file_path = os.path.join(root, file_name)

            relative_path = os.path.relpath(file_path, os.getcwd())

            run_git_command(["git", "add", relative_path])

            gi, returncode = run_git_command(["git", "diff", "--cached", "--quiet", relative_path])
            if '.gitignore' in gi:
                err(f"SKIP: {relative_path} is in .gitignore")
            if returncode == 0: 
                err(f"SKIP: No changes detected for '{relative_path}' since last commit.")
                continue
            cr = custom_rules(relative_path)
            if not cr:
                
                while True:
                    commit_msg = input(f"Enter commit message for '\033[36m{relative_path}\033[0m': \033[32m").strip()
                    print('\033[0m',end='')
                    if commit_msg:
                        break
                    err("Commit message cannot be empty.")
            else:
                commit_msg = cr
                print(f'\033[30mAuto Commit for: {relative_path}\033[0m')
            _, returncode = run_git_command([
                "git", "commit", "-m", commit_msg, relative_path
            ])

    yn = input(f"Push all changes?[\033[36my/any\033[0m]\033[32m").strip()
    print('\033[0m',end='')
    if yn =='y':
        _, returncode = run_git_command(["git", "push"])


main()