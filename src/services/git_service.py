import os
from git import Repo, GitCommandError
import logging
import subprocess

class GitService:
    def __init__(self):
        """Initialize the GitService."""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def create_remote_branch(self, git_repo_url, branch_name):
        """
        Simulate creating a remote branch on the specified repository.
        
        Since we don't have authentication credentials for pushing to the repository,
        this method will determine the default branch and return the commands needed
        to create and push the branch manually.
        
        Args:
            git_repo_url (str): The URL of the Git repository.
            branch_name (str): The name of the branch to create.
            
        Returns:
            tuple: (success, message) where success is a boolean indicating if the operation was successful,
                  and message is a string with details about the operation.
        """
        try:
            # Validate inputs
            if not git_repo_url or not branch_name:
                return False, "Repository URL and branch name are required"
            
            # Create a temporary directory for the operation
            temp_dir = os.path.join(os.getcwd(), "temp_git_" + branch_name)
            
            # Check if the directory already exists and remove it if it does
            if os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)
            
            # Clone the repository
            self.logger.info(f"Cloning repository {git_repo_url} to {temp_dir}")
            repo = Repo.clone_from(git_repo_url, temp_dir)
            
            # Determine the default branch name
            self.logger.info("Determining default branch name")
            default_branch = None
            
            # Method 1: Check if HEAD is a symbolic reference
            try:
                default_branch = repo.git.symbolic_ref("--short", "HEAD").strip()
                self.logger.info(f"Default branch from symbolic ref: {default_branch}")
            except GitCommandError:
                self.logger.info("Could not determine default branch from symbolic ref")
            
            # Method 2: Check remote HEAD reference
            if not default_branch:
                try:
                    remote_refs = repo.git.ls_remote("--symref", "origin", "HEAD").split('\n')
                    for line in remote_refs:
                        if "ref:" in line and "HEAD" in line:
                            # Extract branch name from something like "ref: refs/heads/main\tHEAD"
                            parts = line.split()
                            if len(parts) >= 2:
                                ref_path = parts[1]
                                default_branch = ref_path.replace("refs/heads/", "")
                                self.logger.info(f"Default branch from remote HEAD: {default_branch}")
                                break
                except GitCommandError:
                    self.logger.info("Could not determine default branch from remote HEAD")
            
            # Method 3: Try common branch names
            if not default_branch:
                common_branches = ["main", "master", "develop", "trunk"]
                for branch in common_branches:
                    try:
                        if branch in repo.refs:
                            default_branch = branch
                            self.logger.info(f"Default branch from common names: {default_branch}")
                            break
                    except Exception:
                        continue
            
            # If we still don't have a default branch, use the first branch we find
            if not default_branch and len(repo.refs) > 0:
                for ref in repo.refs:
                    if not ref.name.startswith("origin/"):
                        default_branch = ref.name
                        self.logger.info(f"Using first available branch: {default_branch}")
                        break
            
            # Method 4: Use subprocess to run git commands directly
            if not default_branch:
                try:
                    # Change to the repository directory
                    current_dir = os.getcwd()
                    os.chdir(temp_dir)
                    
                    # Run git command to list all branches
                    result = subprocess.run(
                        ['git', 'branch', '-a'], 
                        capture_output=True, 
                        text=True, 
                        check=True
                    )
                    
                    # Parse the output to find branches
                    branches = result.stdout.strip().split('\n')
                    self.logger.info(f"Available branches: {branches}")
                    
                    # Look for common branch names
                    common_branches = ["main", "master", "develop", "trunk"]
                    for branch in common_branches:
                        for line in branches:
                            if branch in line:
                                default_branch = branch
                                self.logger.info(f"Default branch from subprocess: {default_branch}")
                                break
                        if default_branch:
                            break
                            
                    # Change back to the original directory
                    os.chdir(current_dir)
                except Exception as e:
                    self.logger.error(f"Error using subprocess to find default branch: {str(e)}")
                    os.chdir(current_dir)
            
            # If we still don't have a default branch, use 'master' as a fallback
            if not default_branch:
                default_branch = "master"
                self.logger.info(f"Using fallback branch: {default_branch}")
            
            # Clean up - remove the temporary directory
            import shutil
            shutil.rmtree(temp_dir)
            
            # Generate commands for the user to create and push the branch
            commands = [
                f"git checkout {default_branch}",
                f"git pull origin {default_branch}",
                f"git checkout -b {branch_name}",
                f"git push -u origin {branch_name}"
            ]
            
            return True, {
                "message": f"Here are the commands to create and push branch '{branch_name}' from '{default_branch}' on repository '{git_repo_url}'",
                "commands": commands
            }
            
        except GitCommandError as e:
            self.logger.error(f"Git command error: {str(e)}")
            return False, f"Git command error: {str(e)}"
        except Exception as e:
            self.logger.error(f"Error determining branch information: {str(e)}")
            return False, f"Error determining branch information: {str(e)}"
