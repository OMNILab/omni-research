---
name: omr-research-archive
description: Snapshot current research state for preservation or rollback. Creates timestamped archive of all artifacts, generates archive index, and preserves version metadata. Can be triggered manually or automatically during reconciliation. Enables rollback to previous state if needed. Use when user wants to "archive research", "save snapshot", "preserve state", or before risky changes.
---

# omr-research-archive: Snapshot Research Progress

## Purpose

Snapshot current research state for preservation, historical record, or rollback capability. This skill creates timestamped archives of all artifacts, ensuring research progress is never lost and enabling rollback to previous states if needed.

## Trigger

```
/omr-research-archive [--reason "<reason>"]
```

**Optional argument:** `--reason "<reason>"` - Archive reason

**Examples:**
- `/omr-research-archive` (manual snapshot)
- `/omr-research-archive --reason "Before risky pivot"`
- `/omr-research-archive --reason "Gate D safety snapshot"`

**Automatic triggers:**
- During `omr-reconcile`: Superseded artifacts archived automatically
- Before Gate D (optional): User may request safety snapshot
- After synthesis publication (optional): Preserve milestone

## What This Skill Does

### 1. Collect Current Artifacts

**Artifact collection:**

Scan for all artifacts in workspace:
- `docs/plans/*.md` (brief, evidence, judgment, plan, decision, spec, report)
- `docs/survey/*.md` (synthesis chapters)
- `docs/report/*.md` (synthesis reports)
- `docs/manuscript/*.md` (synthesis manuscripts)
- `docs/brief/*.md` (synthesis briefs)
- `docs/ideas/*.md` (idea notes)
- `docs/index/*.json` (indexes)

**Collection process:**

1. Read `docs/index/artifacts-index.json` for artifact list
2. Read `docs/index/papers-index.json` for materials
3. Read `docs/index/blogs-index.json` for blogs
4. Read `docs/index/github-index.json` for GitHub repos
5. Scan `docs/plans/` for plan artifacts
6. Scan `docs/survey/`, `docs/report/`, `docs/manuscript/`, `docs/brief/` for synthesis
7. Scan `docs/ideas/` for idea notes
8. Scan `wiki/*.md` for wiki pages (optional)

**Artifact list:**
```json
{
  "artifacts": [
    {"id": "Q-001", "type": "research-brief", "file": "docs/plans/brief-Q-001.md"},
    {"id": "Q-001", "type": "evidence-map", "file": "docs/plans/evidence-Q-001.md"},
    {"id": "J-001", "type": "judgment-summary", "file": "docs/plans/judgment-J-001.md"},
    {"id": "PLAN-001", "type": "research-plan", "file": "docs/plans/plan-PLAN-001.md"},
    {"id": "DEC-001", "type": "architecture-decision", "file": "docs/plans/decision-DEC-001.md"},
    {"id": "EXP-001", "type": "experiment-spec", "file": "docs/plans/spec-EXP-001.md"},
    {"id": "EXP-001", "type": "evaluation-report", "file": "docs/plans/report-EXP-001.md"},
    {"id": "SYN-001", "type": "synthesis", "file": "docs/survey/*.md"},
    {"id": "IDEA-001", "type": "idea-note", "file": "docs/ideas/idea-XXX.md"}
  ],
  "materials": [
    {"id": "P-001", "type": "paper", "file": "raw/paper/arxiv-XXX.pdf"},
    {"id": "B-001", "type": "blog", "file": "raw/web/XXX.md"}
  ],
  "indexes": [
    {"file": "docs/index/artifacts-index.json"},
    {"file": "docs/index/papers-index.json"},
    {"file": "docs/index/blogs-index.json"}
  ]
}
```

### 2. Create Timestamped Archive Directory

**Archive directory structure:**

```
docs/archive/
├── 20260411T163000/               # Timestamped snapshot
│   ├── brief-Q-001.md             # Research brief
│   ├── evidence-Q-001.md          # Evidence map
│   ├── judgment-J-001.md          # Judgment summary
│   ├── plan-PLAN-001.md           # Research plan
│   ├── decision-DEC-001.md        # Architecture decision
│   ├── spec-EXP-001.md            # Experiment spec
│   ├── report-EXP-001.md          # Evaluation report
│   ├── survey/                    # Synthesis chapters
│   │   ├── 00-introduction.md
│   │   ├── 01-framework.md
│   │   ├── ...
│   ├── ideas/                     # Idea notes
│   │   ├── idea-XXX.md
│   ├── index/                     # Indexes
│   │   ├── artifacts-index.json
│   │   ├── papers-index.json
│   │   ├── papers-index.md
│   └── archive-metadata.json      # Archive metadata
│
├── 20260411T120000/               # Earlier snapshot
│   └── ...
│
└── index.json                     # Archive catalog
```

**Timestamp generation:**
- Format: `YYYYMMDDTHHMMSS`
- Example: `20260411T163000`
- Generated at archive creation time

**Directory creation:**
```
docs/archive/20260411T163000/
├── (copy all artifacts)
└── archive-metadata.json
```

### 3. Copy Artifacts to Archive

**Copy process:**

For each artifact:
1. Read source file
2. Copy to archive directory
3. Preserve version metadata
4. Note in archive catalog

**Copy example:**
```
Source: docs/plans/brief-Q-001.md
Archive: docs/archive/20260411T163000/brief-Q-001.md

Source: docs/survey/02-formation.md
Archive: docs/archive/20260411T163000/survey/02-formation.md

Source: docs/index/artifacts-index.json
Archive: docs/archive/20260411T163000/index/artifacts-index.json
```

**Preservation rules:**
- Preserve directory structure (survey/, ideas/, index/)
- Preserve file metadata (YAML frontmatter)
- Preserve file permissions (read/write)
- Preserve timestamps (created_at, updated_at)

### 4. Generate Archive Metadata

**Archive metadata:**
```yaml
---
id: ARCH-001
type: archive
snapshot_timestamp: 2026-04-11T16:30:00Z
archive_directory: 20260411T163000
reason: "User-initiated before risky pivot"
trigger: manual_request
user: "user@example.com"

artifacts_archived:
  - id: Q-001
    type: research-brief
    file: brief-Q-001.md
    version: 1.0.0
    status: published

  - id: DEC-001
    type: architecture-decision
    file: decision-DEC-001.md
    version: 1.0.0
    status: published

  - id: EXP-001
    type: evaluation-report
    file: report-EXP-001.md
    version: 1.0.0
    status: published

  - id: SYN-001
    type: synthesis
    files: survey/*.md
    mode: survey
    status: published

artifacts_count: 8
materials_count: 10
indexes_count: 3

workspace_state: "Complete (bootstrap → collection → evidence → plan → decision → evaluation → synthesis)"

rollback_available: true
created_at: 2026-04-11T16:30:00Z
---
```

**Archive metadata structure:**
```json
// docs/archive/20260411T163000/archive-metadata.json
{
  "id": "ARCH-001",
  "type": "archive",
  "snapshot_timestamp": "2026-04-11T16:30:00Z",
  "archive_directory": "20260411T163000",
  "reason": "User-initiated before risky pivot",
  "trigger": "manual_request",
  "artifacts_archived": [
    {
      "id": "Q-001",
      "type": "research-brief",
      "file": "brief-Q-001.md",
      "version": "1.0.0",
      "status": "published"
    }
  ],
  "artifacts_count": 8,
  "materials_count": 10,
  "indexes_count": 3,
  "workspace_state": "Complete",
  "rollback_available": true,
  "created_at": "2026-04-11T16:30:00Z"
}
```

### 5. Update Archive Catalog

**Archive catalog:**
```json
// docs/archive/index.json
{
  "archives": [
    {
      "id": "ARCH-001",
      "timestamp": "20260411T163000",
      "directory": "docs/archive/20260411T163000",
      "reason": "User-initiated before risky pivot",
      "artifacts_count": 8,
      "created_at": "2026-04-11T16:30:00Z"
    },
    {
      "id": "ARCH-002",
      "timestamp": "20260411T120000",
      "directory": "docs/archive/20260411T120000",
      "reason": "Automatic during reconciliation",
      "artifacts_count": 5,
      "created_at": "2026-04-11T12:00:00Z"
    }
  ],
  "archives_count": 2,
  "last_archived": "2026-04-11T16:30:00Z",
  "rollback_latest": "docs/archive/20260411T163000"
}
```

**Catalog update:**
- Add new archive entry
- Update last_archived timestamp
- Update rollback_latest pointer

### 6. Mark Artifacts as Archived

**Artifact metadata update:**

In main artifacts (optional):
```yaml
---
id: DEC-001
type: architecture-decision
version: 1.0.0
status: published
archived_in: [ARCH-001]  # Archive IDs where this version preserved
archive_available: true
---
```

**Note:** Main artifacts remain in place (archive is snapshot, not deletion)

### 7. Display Archive Summary

**Archive completion summary:**

```
✓ Archiving current state...

Archived:
- brief-Q-001.md → docs/archive/20260411T163000/brief-Q-001.md
- evidence-Q-001.md → docs/archive/20260411T163000/evidence-Q-001.md
- decision-DEC-001.md → docs/archive/20260411T163000/decision-DEC-001.md
- report-EXP-001.md → docs/archive/20260411T163000/report-EXP-001.md
- survey/*.md → docs/archive/20260411T163000/survey/*.md (8 chapters)
- index/*.json → docs/archive/20260411T163000/index/*.json

Summary:
- Artifacts archived: 8
- Materials: 10
- Indexes: 3

Archive directory: docs/archive/20260411T163000
Archive metadata: docs/archive/20260411T163000/archive-metadata.json
Archive catalog: docs/archive/index.json

Reason: "User-initiated before risky pivot"

✓ Snapshot saved
✓ Rollback available: docs/archive/20260411T163000

You can rollback to this state if needed via `/omr-research-archive --rollback`
```

### 8. Offer Rollback Option

**Rollback capability:**

After archiving, ask user:
```
Archive complete!

Would you like to:
[1] Proceed with current work (archive preserved)
[2] Review archive contents
[3] Rollback instruction (how to restore later)

Choose [1-3]:
```

**If user chooses rollback instruction:**
```
To rollback to this archive:

/omr-research-archive --rollback ARCH-001

This will restore all artifacts from archive ARCH-001 (20260411T163000).

Caution: Rollback overwrites current state. Archive current state first if needed.

Archive ready for rollback when needed.
```

## Gates

None (archiving is safety mechanism, no gates)

## Can Call

None

## Can Be Called By

- `omr-reconcile`: Auto-archive superseded artifacts
- User manual request: `/omr-research-archive`

## Prerequisites

- At least one existing artifact (required)

**If no artifacts:**
- Error: "No artifacts to archive. Workspace empty."
- Do not proceed

## Examples

### Example 1: Manual archive
```
User: /omr-research-archive

System: ✓ Collecting artifacts...

        Artifacts found:
        - Plans: 7 artifacts
        - Synthesis: 8 chapters
        - Ideas: 3 notes
        - Indexes: 5 files

        ✓ Creating archive: docs/archive/20260411T163000

        ✓ Copying artifacts...

        Archived:
        - brief-Q-001.md
        - decision-DEC-001.md
        - report-EXP-001.md
        - survey/*.md (8 chapters)
        - ...

        Summary:
        - Artifacts: 18
        - Materials: 10
        - Indexes: 5

        Archive: docs/archive/20260411T163000
        Reason: (not specified)

        ✓ Snapshot saved
        ✓ Rollback available

        What next?
        [1] Proceed
        [2] Review archive
        [3] Rollback instruction

User: 1

System: ✓ Archive preserved
        Continue research whenever ready
```

### Example 2: Archive with reason
```
User: /omr-research-archive --reason "Before risky pivot to graph-only approach"

System: ✓ Archiving...

        Reason: "Before risky pivot to graph-only approach"

        ✓ Archive created: docs/archive/20260411T163000

        ✓ Snapshot saved

        Note: If pivot fails, rollback to this archive

        Proceed with pivot? [Y/n]

User: Y

System: ✓ Archive preserved as safety checkpoint
        Continue with risky change
```

### Example 3: Automatic archive during reconciliation
```
System: ✓ Re-evaluating evidence...

        ⚠️  Decision DEC-001 needs revision

        Auto-archiving superseded artifacts...

        ✓ Archive: docs/archive/20260411T163000
        - decision-DEC-001-v1.0.0.md (superseded)
        - report-EXP-001-v1.0.0.md (needs re-run)

        Reason: "Automatic during reconciliation"

        ✓ Old versions preserved
        ✓ Proceeding with reconciliation...

        Updating to DEC-001-v2.0.0
```

### Example 4: Gate D safety snapshot
```
System: ⚠️  GATE D: Before Publish

        Review criteria:
        [✓] Results traceable
        [✓] Evidence boundaries stated

        Create safety snapshot before publish? [y/N]

User: y

System: ✓ Archiving pre-publish snapshot...

        ✓ Archive: docs/archive/20260411T170000
        Reason: "Gate D safety snapshot"

        ✓ Snapshot saved

        Proceed with publish? [Y/n]

User: Y

System: ✓ Gate D passed
        ✓ Synthesis published

        Note: Pre-publish snapshot available for rollback
```

### Example 5: Rollback request
```
User: /omr-research-archive --rollback ARCH-001

System: ⚠️  Rollback requested

        Target archive: ARCH-001 (20260411T163000)

        This will restore all artifacts from archive, overwriting current state.

        Archive current state first? [Y/n]

User: Y

System: ✓ Archiving current state...

        ✓ Current: docs/archive/20260411T180000

        ✓ Restoring from ARCH-001...

        Restored:
        - brief-Q-001.md (v1.0.0)
        - decision-DEC-001.md (v1.0.0)
        - ...

        ✓ Rollback complete

        Workspace restored to 2026-04-11T16:30:00Z state

        Note: Current state preserved in docs/archive/20260411T180000
```

### Example 6: Review archive contents
```
User: /omr-research-archive --review ARCH-001

System: ✓ Archive contents: ARCH-001 (20260411T163000)

        Reason: "User-initiated before risky pivot"

        Artifacts:
        - brief-Q-001.md (v1.0.0)
        - evidence-Q-001.md (v1.0.0)
        - decision-DEC-001.md (v1.0.0)
        - report-EXP-001.md (v1.0.0)
        - survey/*.md (8 chapters)
        - ideas/*.md (3 notes)

        Total: 18 artifacts

        Created: 2026-04-11T16:30:00Z
        Directory: docs/archive/20260411T163000

        Rollback available: Yes
```

### Example 7: Missing prerequisites
```
User: /omr-research-archive

System: ⚠️  No artifacts found.
        Workspace appears empty.

        Cannot archive empty workspace.

        Run `/omr-bootstrap` and create some artifacts first.

        Aborting...
```

### Example 8: List all archives
```
User: /omr-research-archive --list

System: ✓ Archives available: 2

        [1] ARCH-001 (20260411T163000)
            Reason: "User-initiated before risky pivot"
            Artifacts: 18
            Created: 2026-04-11T16:30:00Z

        [2] ARCH-002 (20260411T120000)
            Reason: "Automatic during reconciliation"
            Artifacts: 5
            Created: 2026-04-11T12:00:00Z

        Latest rollback: ARCH-001

        To rollback: /omr-research-archive --rollback ARCH-XXX
```

## What NOT to Do

- Do NOT archive empty workspace (require at least one artifact)
- Do NOT overwrite archives (each archive is unique timestamped snapshot)
- Do NOT delete current artifacts (archive is snapshot, not deletion)
- Do NOT proceed without user approval for rollback (rollback overwrites current state)
- Do NOT skip archive during reconciliation (always preserve superseded versions)

## Success Criteria

- [ ] Artifacts collected from workspace
- [ ] Archive directory created (timestamped)
- [ ] Artifacts copied to archive
- [ ] Archive metadata generated
- [ ] Archive catalog updated
- [ ] Archive summary displayed
- [ ] Rollback capability available
- [ ] User informed of archive location and rollback option

## Edge Cases

### Empty workspace

If no artifacts exist:
- Error: "No artifacts to archive"
- Recommendation: "Run `/omr-bootstrap` first"

### Partial workspace

If workspace incomplete (e.g., only brief, no decision):
- Archive what exists
- Note: "Partial snapshot (workspace incomplete)"
- Proceed with archive

### Multiple archives

If multiple archives exist:
- Each archive is separate snapshot
- Archives do not overwrite each other
- Catalog maintains list of all archives

### Rollback with current state

If rollback requested:
- Always archive current state first (unless user explicitly declines)
- Then restore from target archive
- Preserve both old and new states

### Large archive

If many artifacts (>50):
- Archive may take time
- Show progress indicator
- Estimate time: "Archiving ~50 artifacts, estimated 30 seconds"

### Archive storage limits

If archive directory exceeds storage:
- Warn: "Archive size large (~1GB)"
- Ask: "Proceed anyway? [Y/n]"
- If yes: Archive despite size

### Pre-bootstrap archive

If user requests archive before bootstrap:
- Error: "No workspace initialized"
- Recommendation: "Run `/omr-bootstrap` first"

## Integration with Other Skills

**Called by:**
- `omr-reconcile`: Auto-archive superseded artifacts
- User manual: `/omr-research-archive`

**Rollback interaction:**
- Rollback does NOT call other skills
- Rollback restores artifacts from archive (file operation only)
- After rollback, user may need to re-run skills if artifacts reverted to older versions

**Archive timing:**
- After synthesis: Milestone archive (optional)
- Before Gate D: Safety snapshot (optional)
- During reconciliation: Auto-archive (automatic)

**Reconciliation flow:**
```
omr-reconcile →
  calls omr-research-archive (archive superseded) →
  calls omr-evidence (re-map) →
  calls omr-decision (re-decide) →
  calls omr-evaluation (re-run) →
  calls omr-synthesis (update)
```

## Use Cases

### Safety checkpoint

Before risky pivot or major change:
- Archive current state
- Proceed with change
- Rollback if needed

### Milestone preservation

After synthesis publication:
- Archive milestone state
- Preserve publication-quality artifacts
- Historical record for audit

### Reconciliation safety

During reconciliation:
- Auto-archive superseded versions
- Preserve history
- Traceability through versions

### Historical record

For research audit:
- Archive states at key points
- Review archive history
- Document research evolution

### Rollback capability

If experiments fail or decisions flawed:
- Rollback to previous archive
- Restart from stable state
- Avoid losing progress

### Experimentation safety

Before speculative experiments:
- Archive stable state
- Run speculative tests
- Rollback if hypothesis refuted