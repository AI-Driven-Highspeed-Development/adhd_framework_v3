# ADHD-Managed Header Format

All exported files MUST include this header:

```markdown
<!-- ═══════════════════════════════════════════════════════════════════
     ADHD-MANAGED FILE
     
     Source: {sidecar_path}
     Expedition: {expedition_id}
     Created: {timestamp}
     Hash: sha256:{hash}
     
     ⚠️ MODIFICATION RULES:
     - Lines between USER CUSTOMIZATION markers are YOURS to edit
     - All other lines will be overwritten on sync
     - To prevent sync: delete this header (file becomes unmanaged)
═══════════════════════════════════════════════════════════════════ -->
```

## User Customization Zone

```markdown
<!-- USER CUSTOMIZATION START -->
{user's custom content preserved during sync}
<!-- USER CUSTOMIZATION END -->
```
