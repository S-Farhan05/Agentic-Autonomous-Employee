---
name: create-plan
description: Create multi-step execution plans for complex tasks
trigger: /create-plan
---

# Create Plan Skill

This skill analyzes complex tasks and creates detailed execution plans with checkboxes for tracking progress.

## What This Skill Does

1. Analyzes task complexity and requirements
2. Breaks down into discrete, actionable steps
3. Identifies dependencies between steps
4. Determines which steps require approval
5. Creates Plan.md file in Plans/ folder
6. Updates Dashboard with plan status

## Usage

```bash
/create-plan
```

Or for a specific task:

```bash
/create-plan --task "Generate invoice and send to client"
```

## Instructions for Claude

When this skill is invoked:

1. **Identify Complex Tasks**
   - Read tasks from Needs_Action folder
   - Determine if task requires multiple steps
   - Check if task involves external actions
   - Look for keywords: "and", "then", "after", "multiple", "workflow"

2. **Analyze Task Requirements**
   - What is the end goal?
   - What are the intermediate steps?
   - What dependencies exist?
   - What requires human approval?
   - What can be automated?

3. **Create Plan Structure**
   ```markdown
   # Plans/PLAN_[task_name].md
   ---
   created: [timestamp]
   task_id: [original_task_id]
   priority: [high/medium/low]
   status: in_progress
   estimated_time: [hours]
   ---

   ## Objective
   [Clear statement of what needs to be accomplished]

   ## Steps
   - [ ] Step 1: [Action] (auto-approved)
   - [ ] Step 2: [Action] (REQUIRES APPROVAL)
   - [ ] Step 3: [Action] (auto-approved)

   ## Dependencies
   - Step 2 depends on Step 1 completion
   - Step 3 requires approval from Step 2

   ## Status
   [Current progress and blockers]
   ```

4. **Categorize Steps**
   - **Auto-Approved**: Reading, analyzing, drafting, organizing
   - **Requires Approval**: Sending, posting, paying, deleting
   - Mark each step clearly

5. **Update Dashboard**
   - Add plan to Recent Activity
   - Update Pending Actions with plan steps
   - Set alerts for approval-required steps

## Example Plans

### Invoice Workflow
```markdown
## Objective
Generate and send invoice to Client A for $2,500

## Steps
- [x] Read client details from vault
- [x] Calculate amount: $2,500 for 50 hours
- [ ] Generate invoice PDF (auto-approved)
- [ ] Draft email with invoice (auto-approved)
- [ ] REQUIRES APPROVAL: Send email to client
- [ ] Log transaction in accounting
- [ ] Set 7-day follow-up reminder

## Status
Waiting for approval to send email
```

### Social Media Campaign
```markdown
## Objective
Create and post LinkedIn content for lead generation

## Steps
- [x] Research trending topics in industry
- [x] Draft 3 post options
- [ ] REQUIRES APPROVAL: Select post to publish
- [ ] REQUIRES APPROVAL: Post to LinkedIn
- [ ] Monitor engagement for 24 hours
- [ ] Respond to comments (each requires approval)

## Status
Draft posts ready for review
```

## When to Create Plans

**Create Plan For:**
- Tasks with 3+ distinct steps
- Tasks involving external actions (email, post, payment)
- Tasks with dependencies
- Tasks requiring approval at multiple stages
- Project-based work

**Don't Create Plan For:**
- Simple file reviews
- Single-action tasks
- Routine categorization
- Reading/analyzing only

## Plan Lifecycle

1. **Created**: Plan.md written to Plans/ folder
2. **In Progress**: Steps being executed
3. **Blocked**: Waiting for approval
4. **Completed**: All steps done, moved to Done/
5. **Cancelled**: Task no longer needed

## Output Format

After creating plan:

```
Plan created: PLAN_[task_name].md

Objective: [Brief description]
Total steps: X
Auto-approved: Y
Requires approval: Z

Next action: [What needs to happen next]
```

## Integration with Other Skills

- Use `/process-tasks` to execute plan steps
- Use `/process-approvals` for approval-required steps
- Use `/send-email` or other action skills for execution
