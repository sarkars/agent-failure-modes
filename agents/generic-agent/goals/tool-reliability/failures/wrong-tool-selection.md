# Wrong Tool Selection

## Issue: Agent Selects Inappropriate Tool for Task

**Frequency**: Common

**Symptoms**
- Agent uses read tool when write is needed
- Similar tools confused (search vs. lookup)
- Agent uses complex tool when simple one suffices
- Tool selection doesn't match user intent

**Root Cause**
- Too many similar tools available
- Poor tool naming or descriptions
- Agent doesn't understand tool capabilities
- Tools with overlapping functionality

**Example**
```
User: "Delete the file"

Available tools: 
- file_read: Read file contents
- file_write: Write to file (overwrites)
- file_delete: Delete file

Agent selects: file_write with empty content

Result: File emptied but not deleted, takes up space
```

**Mitigation Strategies**
1. **Clear tool descriptions**: Explain when to use each tool
2. **Reduce tool overlap**: Combine similar tools or clarify differences
3. **Tool categories**: Group tools logically
4. **Intent-based routing**: Pre-classify intent before tool selection
5. **Negative examples**: Document when NOT to use each tool
6. **Tool selection verification**: Confirm selection for destructive actions

**Detection**
- Track tool usage vs. task type
- Monitor user corrections of tool selection
- Log sequences where wrong tool preceded correct one
- Compare tool selection across similar tasks
