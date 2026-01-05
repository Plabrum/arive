# Submit Changes

Create a feature branch, commit changes, push to remote, and open a pull request.

## Instructions

This command handles the complete git workflow for submitting changes:

### 1. Pre-Submission Checks (Optional but Recommended)

If changes are significant, run quality checks first:
```bash
make check-all  # Type checking + linting
make test       # Backend tests
cd frontend && pnpm run build  # Frontend build check
```

### 2. Analyze Changes

- Review all changes made in this session using `git status` and `git diff`
- Understand the scope and purpose of the changes
- Generate a descriptive feature name in kebab-case based on the changes

### 3. Create Branch, Commit, and PR

Follow the `/branch-and-pr` skill workflow:

1. **Get engineer's initials**:
   - Run `git config user.name` to get full name
   - Extract initials (e.g., "Phil Labrum" → "pl")
   - Convert to lowercase

2. **Generate branch name**:
   - Format: `<initials>/<feature-description-in-kebab-case>`
   - Examples:
     - `pl/add-user-authentication`
     - `jd/fix-payment-validation`
     - `sk/refactor-api-client`

3. **Create and checkout branch**:
   ```bash
   git checkout -b <branch-name>
   ```

4. **Stage all relevant changes**:
   ```bash
   git add .
   ```

5. **Create commit**:
   - Use clear, descriptive message in imperative mood
   - Include Claude Code attribution:
   ```bash
   git commit -m "$(cat <<'EOF'
   <descriptive-commit-message>

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
   EOF
   )"
   ```

6. **Handle pre-commit hooks**:
   - If commit fails due to hooks (ruff, prettier, etc.):
     - Let them auto-format the files
     - Re-stage: `git add -u`
     - Retry the same commit (it was never created)

7. **Push to remote**:
   ```bash
   git push -u origin <branch-name>
   ```

8. **Create pull request**:
   ```bash
   gh pr create --title "<title>" --body "$(cat <<'EOF'
   ## Summary
   - [Bullet describing change 1]
   - [Bullet describing change 2]

   ## Test Plan
   - [How to verify these changes]

   🤖 Generated with [Claude Code](https://claude.com/claude-code)
   EOF
   )"
   ```

9. **Display PR URL**:
   - Show the URL for user to review

## Notes

- **Branch naming**: `<initials>/<feature-description-in-kebab-case>`
- **Initials**: Always lowercase (e.g., "pl" not "PL")
- **Commit messages**: Imperative mood (e.g., "add feature" not "added feature")
- **PR description**: Be thorough but concise - focus on "why" and "what"
- **Base branch**: Always `main` (verify with `git status`)
- **Pre-commit hooks**: Let them run and auto-format, then re-stage and retry
- **Quality checks**: Run `make check-all` before submitting significant changes

## Files to Never Commit

Pre-commit hooks will catch these, but avoid:
- Lockfiles (unless intentionally updated): `package-lock.json`, `pnpm-lock.yaml`, `uv.lock`
- Environment files: `.env`, `.env.local`, etc.
- Terraform state: `terraform.tfstate`
- Generated artifacts (unless part of build process)

## See Also

- `/branch-and-pr` skill - Reusable git workflow logic
- `/linear-ticket` command - Full workflow for Linear tickets
- `/check-all` command - Run all quality checks
