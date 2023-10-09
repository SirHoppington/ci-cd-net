# ci-cd-net

A repo to be used as a "Golden branch" for network device configuration as part of a Network DevOps CI/CD pipeline.
Engineers will configure txt files with required changes, which will be tested via dry run (or dev env if available), a backup of the IOS config saved with the commit hash and after changes are pushed to prod the "golden config" is also updated.

## Nornir CI/CD Pipeline workflow:

1. Engineer clones main repo and creates feature branch for the "changes" to be made -likely the reference of a change control.

```
git clone https://github.com/SirHoppington/ci-cd-net

```

2. Engineer creates configuration in "/crq_changes" and pushes to the feature branch.

3. Github actions workflow file "dry_run.yaml" checks for configuration changes to any files with "/crq_changes" on the feature branch.
   - if changes are detected then nornir will run a dry-run of the changes to the respective hosts (text file name must match hostname in inventory hosts file).
4. When the engineer is happy with the changes a Pull Request is opend to Main.
   - The "dry_run.yaml" workflow again detects changes and applys the dry-run.
   - If tests pass then the branch can be merged to main.
5. When the branch is merged to main the "integrate.yaml" workflow runs
   - First a backup of each device is taken a saved under crq_backups/router-name/.
   - The configuration is pushed concurrently to the respective devices via nornir.
   - A backup of the post-change config is saved in the /golden_configs directory.

### To be added:
6. PyATS post test scripts run 
   1. pull request made to main branch
7. Peer review/CAB of proposed changes.
8 . On Pull Request both dry_run and on PR runs..dry_run runs dif from last commit, on PR runs diff to main.
