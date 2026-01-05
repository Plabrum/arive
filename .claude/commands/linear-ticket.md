# Linear Ticket Workflow

Complete end-to-end workflow for implementing a Linear ticket from planning to pull request.

## Usage

```
/linear-ticket ARI-36
```

## Instructions

This command automates the entire development workflow for a Linear ticket:

### 1. Fetch Ticket from Linear

- Extract ticket ID from the command arguments (e.g., "ARI-36")
- Use `mcp__plugin_linear_linear__get_issue` to fetch ticket details
- Display ticket information:
  - Title
  - Description
  - Current status
  - Assignee
  - Labels
  - Related issues/blockers
  - Linked documents or resources

### 2. Create Implementation Plan

- Analyze the ticket requirements thoroughly
- Use the Task tool with `subagent_type=Explore` to understand relevant codebase areas
- Create a detailed implementation plan using TodoWrite:
  - Break down the work into specific, actionable steps
  - Identify files that need to be modified
  - Note any dependencies or prerequisites
  - Include quality check steps (type checking, linting, tests, build)

### 3. Implement the Changes

- Execute the implementation plan step by step
- Mark todos as `in_progress` before starting each step
- Mark todos as `completed` immediately after finishing each step
- Follow existing code patterns and conventions from the codebase
- Make necessary changes to backend and/or frontend
- Run related tests frequently during implementation

### 4. Database & API Changes (if applicable)

- **If SQLAlchemy models were modified**:
  - Run `make db-migrate` to create Alembic migration
  - Review the generated migration file
  - Run `make db-upgrade` to apply migration
  - Run tests to verify schema changes

- **If backend routes or schemas were modified**:
  - Run `make codegen` to regenerate TypeScript API client
  - Verify frontend types are updated
  - Fix any TypeScript errors in frontend

### 5. Run Quality Checks

Run all quality checks and fix any errors:

```bash
# Type checking
make check-backend   # basedpyright for Python
make check-frontend  # TypeScript compiler

# Linting
make lint-backend    # ruff check and format
make lint-frontend   # ESLint

# Tests
make test            # pytest for backend

# Build verification
cd frontend && pnpm run build  # Production build check
```

Fix any errors that occur before proceeding.

### 6. Final Verification

- Run `make check-all` to ensure everything passes
- Verify all todos are marked as completed
- Review all changes with `git diff`
- Ensure no unintended files are staged

### 7. Create Branch, Commit, and PR

Use the `/branch-and-pr` skill (or implement inline):

- Get engineer's initials from `git config user.name` (e.g., "Phil Labrum" → "pl")
- Generate branch name: `<initials>/<ticket-id>/<feature-description>`
  - Example: `pl/ARI-36/add-user-authentication`
  - Feature description should be kebab-case and descriptive
- Create and checkout branch: `git checkout -b <branch-name>`
- Stage changes: `git add .`
- Create commit with message: `<TICKET-ID>: <description>`
  - Example: `ARI-36: add user authentication system`
  - Include Claude Code attribution footer
- Handle pre-commit hooks (re-stage if auto-formatted)
- Push to remote: `git push -u origin <branch-name>`
- Create PR using `gh pr create` with description:

```markdown
## Summary

Closes https://linear.app/arive/issue/<TICKET-ID>

- [Bullet point describing change 1]
- [Bullet point describing change 2]
- [Bullet point describing change 3]

## Implementation Details

[Brief technical overview of the approach taken]

## Test Plan

- [x] Type checking passes (backend + frontend)
- [x] Linting passes (backend + frontend)
- [x] Tests pass (backend)
- [x] Production build succeeds (frontend)
- [ ] Manual testing completed
- [ ] Reviewed by team

## Linear Ticket

https://linear.app/arive/issue/<TICKET-ID>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### 8. Update Linear Ticket

- Use `mcp__plugin_linear_linear__create_comment` to add comment to ticket
- Comment body should include:
  ```
  Pull request created: <pr-url>

  Implementation complete and ready for review.
  ```
- Display the PR URL for the user

## Example Flow

```
User: /linear-ticket ARI-36

Claude:
1. Fetching Linear ticket ARI-36...
   - Title: Add user authentication system
   - Status: In Progress
   - Assignee: Phil

2. Creating implementation plan...
   [Todo list with implementation steps]

3. Implementing changes...
   [Step-by-step implementation]

4. Running quality checks...
   ✓ Type checking passed
   ✓ Linting passed
   ✓ Tests passed
   ✓ Build succeeded

5. Creating branch: pl/ARI-36/add-user-authentication
6. Committing changes: "ARI-36: add user authentication system"
7. Creating pull request...
   PR created: https://github.com/org/repo/pull/123

8. Updating Linear ticket with PR link...
   ✓ Comment added to ARI-36
```

## Notes

- **Prerequisites**:
  - Linear MCP plugin must be connected (`/mcp` to verify)
  - GitHub CLI must be authenticated (`gh auth status`)
  - Git user config must be set (`git config user.name`)
  - Development services should be stopped before running checks

- **Branch naming**: `<initials>/<ticket-id>/<feature-description>`
- **Commit format**: `<TICKET-ID>: <imperative description>`
- **Base branch**: Always `main`
- **Linear URL format**: `https://linear.app/arive/issue/<TICKET-ID>`

## Error Handling

If any step fails:
1. Stop the workflow at the failed step
2. Display the error clearly to the user
3. Provide guidance on how to fix the issue
4. Don't proceed until the error is resolved
5. **Never skip quality checks** - they must pass before committing

Common errors:
- **Linear ticket not found**: Verify ticket ID is correct and accessible
- **Type checking fails**: Fix TypeScript/Python type errors
- **Tests fail**: Fix failing tests, don't skip them
- **Build fails**: Fix build errors in frontend
- **Pre-commit hooks fail**: Let them auto-format, re-stage, and retry
- **PR creation fails**: Check gh CLI authentication

## Advanced Usage

### Skipping Steps (Not Recommended)

This workflow is designed to be comprehensive. Skipping steps is not recommended, but if absolutely necessary:
- Document why the step was skipped
- Ensure it's communicated in the PR description
- Add follow-up tasks if needed

### Working on Existing Branch

If a branch for the ticket already exists:
1. Check out the existing branch
2. Continue with implementation
3. Amend or create new commits as appropriate
4. Update existing PR instead of creating a new one

### Multiple Tickets

For working on multiple related tickets:
1. Run `/linear-ticket` for each ticket separately
2. Each gets its own branch and PR
3. Link PRs together in descriptions if dependent
4. Coordinate merge order if there are dependencies