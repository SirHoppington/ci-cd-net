# ci-cd-net

A repo to be used as a "Golden branch" for network device configuration as part of
a Network DevOps CI/CD pipeline.

Nornir CI/CD Pipeline workflow:

1. Engineer clones main repo and creates feature branch for the "changes" to be made -likely the reference of a change control.

2. Engineer modifies configuration in "/crq_changes" and pushes to the feature branch.

3. Github actions workflow file "dry_run.yaml" checks for configuration changes to any files with "/crq_changes" on the feature branch.
   - if changes are detected then nornir will run a dry-run of the changes to the respective hosts (text file name must match hostname in inventory hosts file).
4. When the engineer is happy withe changes ta Pull Request is opend to Main.
   - The "dry_run.yaml" workflow again detects changes and applys the dry-run.
   - If tests pass then the branch can be merged to main.
5. When the branch is merged to main the "integrate.yaml" workflow runs which applies the changes to the respective devices.

### To be added:
6. Golden_config file to be updated after each succesful push to main.
7. PyATS post test scripts run 
   1. pull request made to main branch
8. Peer review/CAB of proposed changes.
9 . On Pull Request both dry_run and on PR runs..dry_run runs dif from last commit, on PR runs diff to main.
