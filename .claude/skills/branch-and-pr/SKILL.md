---
name: branch-and-pr
description: Reusable git workflow for creating branches, commits, and pull requests. Handles branch naming with initials, commit creation with pre-commit hook handling, and PR generation.
---

# Branch, Commit, and Pull Request Workflow

Shared workflow for creating feature branches, committing changes, and opening pull requests.

## When to use this skill

- After completing implementation work that needs to be submitted
- When you need to create a branch, commit, and PR in one flow
- From other commands/skills like `/submit` or `/linear-ticket`

## Workflow Steps

1. **Determine engineer's initials**
   - Run `git config user.name` to get full name
   - Extract initials from the name (e.g., "Phil Labrum" → "pl")
   - Convert to lowercase for consistency

2. **Generate branch name**
   - Use format: `<initials>/<feature-description-in-kebab-case>`
   - For Linear tickets: `<initials>/<ticket-id>/<feature-description>`
   - Examples:
     - `pl/add-user-authentication`
     - `pl/ARI-36/fix-campaign-validation`
     - `sk/refactor-api-client`

3. **Create and checkout branch**
   ```bash
   git checkout -b <branch-name>
   ```

4. **Stage all relevant changes**
   ```bash
   git add .
   ```
   Or stage specific files as needed

5. **Create commit**
   - Generate descriptive commit message:
     - For general work: Use imperative mood (e.g., "add user authentication")
     - For Linear tickets: `<TICKET-ID>: <description>` (e.g., "ARI-36: add user authentication")
   - Create commit with Claude Code attribution:
   ```bash
   git commit -m "$(cat <<'EOF'
   <commit-message>

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
   EOF
   )"
   ```

6. **Handle pre-commit hooks**
   - If commit fails due to pre-commit hooks:
     - Check if hooks auto-formatted files (e.g., ruff, prettier)
     - If so, stage the reformatted files: `git add -u`
     - Retry the same commit command (commit never happened, so just create it fresh)
   - Continue until commit succeeds

7. **Push to remote**
   ```bash
   git push -u origin <branch-name>
   ```

8. **Create pull request**
   - Use `gh pr create` with detailed description
   - PR title should match commit message
   - PR body should include:
     ```
     ## Summary
     [2-3 bullet points describing changes]

     ## Test plan
     [Bulleted markdown checklist of verification steps]

     🤖 Generated with [Claude Code](https://claude.com/claude-code)
     ```
   - For Linear tickets, also include:
     ```
     Closes https://linear.app/arive/issue/<TICKET-ID>
     ```

9. **Return PR URL**
   - Display the PR URL so it can be used by calling command
   - For Linear tickets, the URL will be used to update the ticket

## Parameters (Conceptual)

This skill can be adapted based on context:

- **Feature name**: Generated from work done or provided explicitly
- **Ticket ID**: Optional, if working on a Linear ticket
- **Commit message**: Generated from changes or provided explicitly
- **PR description**: Generated from context or provided explicitly

## Best Practices

- **Branch naming**: Always use `<initials>/` prefix followed by kebab-case
- **Initials**: Always lowercase (e.g., "pl" not "PL")
- **Commit messages**: Use imperative mood (e.g., "add feature" not "added feature")
- **PR descriptions**: Be thorough but concise - focus on the "why" and "what"
- **Base branch**: Always use `main` (verify with `git status`)

## Error Handling

- **Pre-commit hooks fail**: Re-stage files and retry (don't skip)
- **Push fails**: Check if branch already exists remotely
- **PR creation fails**: Verify gh CLI is authenticated (`gh auth status`)
- **Merge conflicts**: Stash or commit changes before switching branches

## Integration with Other Commands

This skill is designed to be called from:
- `/submit` - For general feature work
- `/linear-ticket` - For Linear ticket workflow
- Other custom commands that need git workflow

The calling command should:
1. Complete all implementation and quality checks first
2. Prepare context (feature name, ticket ID if applicable)
3. Invoke this skill to handle git operations
4. Use the returned PR URL for any follow-up actions (e.g., updating Linear)

## Notes

- Don't commit lockfiles, env files, or generated artifacts (pre-commit hooks will catch these)
- Run `make check-all` before using this skill if changes are significant
- The PR will automatically include Claude Code attribution footer
- Git user config must be set (`git config user.name`)
