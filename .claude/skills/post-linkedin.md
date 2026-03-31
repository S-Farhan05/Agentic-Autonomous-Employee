---
name: post-linkedin
description: Create and post LinkedIn content for business development
trigger: /post-linkedin
---

# Post LinkedIn Skill

This skill creates professional LinkedIn posts for business development and lead generation with approval workflow.

## What This Skill Does

1. Analyzes business context and goals
2. Creates engaging LinkedIn post drafts
3. Follows LinkedIn best practices
4. Creates approval requests for posts
5. Posts approved content via LinkedIn API/MCP
6. Tracks engagement and results
7. Updates Dashboard with posting activity

## Usage

```bash
/post-linkedin --topic "project success" --draft
```

Or post from approval:

```bash
/post-linkedin --from-approval POST_linkedin_123
```

## Instructions for Claude

When this skill is invoked:

1. **Analyze Business Context**

   a. **Read Business Goals**
   - Check AI_Employee_Vault/Business_Goals.md
   - Understand target audience
   - Identify key messages

   b. **Review Recent Activity**
   - Check Done/ folder for completed projects
   - Look for achievements to highlight
   - Find client success stories

2. **Create LinkedIn Post**

   **Post Structure:**
   ```
   [Hook - attention-grabbing first line]

   [Context - 2-3 sentences about the topic]

   [Value - key insight or lesson]

   [Call to action - what you want readers to do]

   [Hashtags - 3-5 relevant tags]
   ```

   **Example Post:**
   ```
   Just completed a challenging project that taught me valuable lessons about [topic].

   Working with [Client/Industry], we faced [challenge]. Here's what made the difference:

   → [Key point 1]
   → [Key point 2]
   → [Key point 3]

   The result? [Specific outcome/metric]

   What's your experience with [topic]? Drop a comment below.

   #SoftwareDevelopment #ProjectManagement #TechConsulting
   ```

3. **LinkedIn Best Practices**

   - **Length**: 150-300 words (sweet spot for engagement)
   - **Hook**: First line must grab attention
   - **Formatting**: Use line breaks and bullets
   - **Hashtags**: 3-5 relevant, not spammy
   - **CTA**: Ask a question or invite discussion
   - **Tone**: Professional but conversational
   - **Value**: Always provide insight or lesson

4. **Create Approval Request**

   ```markdown
   # Pending_Approval/POST_linkedin_[date].md
   ---
   type: approval_request
   action: post_linkedin
   platform: LinkedIn
   priority: medium
   created: 2026-03-31T10:00:00Z
   expires: 2026-04-02T10:00:00Z
   ---

   ## LinkedIn Post Draft

   ---

   [Post content here]

   ---

   ## Post Details
   - **Estimated reach**: [based on your network]
   - **Target audience**: [who this is for]
   - **Goal**: [lead generation/brand awareness/thought leadership]
   - **Hashtags**: #Tag1 #Tag2 #Tag3

   ## Context
   This post highlights [recent achievement/insight] to generate leads in [industry].

   ## To Approve
   Move this file to /Approved folder

   ## To Reject or Edit
   Move to /Rejected or edit content and re-submit
   ```

5. **Post to LinkedIn**

   When processing from Approved folder:

   a. **Read Approval**
   - Parse post content
   - Verify approval timestamp
   - Check for any edits

   b. **Post via API/MCP**
   ```python
   # Pseudo-code for LinkedIn posting
   linkedin_mcp.create_post({
       'content': post_text,
       'visibility': 'PUBLIC'
   })
   ```

   c. **Log Activity**
   ```json
   {
     "timestamp": "2026-03-31T10:30:00Z",
     "action": "linkedin_post",
     "content_preview": "Just completed a challenging...",
     "post_id": "urn:li:share:123456",
     "approved_by": "human",
     "result": "success"
   }
   ```

   d. **Track Engagement** (optional for Silver Tier)
   - Monitor likes, comments, shares
   - Log engagement metrics
   - Report in Dashboard

## Post Types

### Project Success Story
```
🎯 Just wrapped up a project that exceeded expectations.

[Client/Industry] needed [solution]. We delivered:
→ [Result 1]
→ [Result 2]
→ [Result 3]

Key takeaway: [Lesson learned]

Working on similar challenges? Let's connect.

#ProjectSuccess #Consulting
```

### Industry Insight
```
Here's something I've noticed in [industry] lately:

[Observation or trend]

Why this matters:
→ [Impact 1]
→ [Impact 2]

What are you seeing in your work?

#IndustryTrends #TechInsights
```

### Problem-Solution
```
Common problem I see: [Problem statement]

Here's how we solved it:

[Brief story of solution]

The approach:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Result: [Outcome]

Facing similar challenges? Drop a comment.

#ProblemSolving #Solutions
```

## Content Calendar (Silver Tier)

Suggested posting frequency:
- **2-3 times per week**: Optimal for engagement
- **Best times**: Tuesday-Thursday, 8-10 AM or 12-1 PM
- **Mix content types**: 40% insights, 30% projects, 30% engagement

## Safety Rules

- NEVER post without approval
- ALWAYS review for sensitive information
- CHECK for client confidentiality
- VERIFY facts and claims
- AVOID controversial topics
- MAINTAIN professional tone

## Output Format

**Draft Mode:**
```
LinkedIn post draft created: POST_linkedin_[date].md

Preview: [First 50 characters...]
Status: Pending approval in /Pending_Approval

Move to /Approved to post.
```

**Post Mode:**
```
LinkedIn post published successfully!

Post ID: urn:li:share:123456
Posted at: 2026-03-31 10:30
Preview: [First 100 characters...]

View post: [LinkedIn URL]
Dashboard updated.
```

## MCP Server Configuration

Requires LinkedIn MCP or API integration:

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "node",
      "args": ["path/to/linkedin-mcp/index.js"],
      "env": {
        "LINKEDIN_ACCESS_TOKEN": "your_token"
      }
    }
  }
}
```

## Integration Points

- **Business_Goals.md**: Content strategy and targets
- **Done/ folder**: Source of success stories
- **LinkedIn API/MCP**: Posting mechanism
- **Approval Workflow**: Human review
- **Dashboard**: Activity tracking
