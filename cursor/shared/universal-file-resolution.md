# Universal File Resolution Protocol

**PROTOCOL: How to locate files.**

To find a file (e.g., "**Product Definition**") within Project Root or a Track:

1. **Identify Index:**
   - **Project Context:** `conductor/index.md`
   - **Track Context:** Read **Tracks Registry** → follow link to track folder → `<track_folder>/index.md`
   - **Fallback:** `<Tracks Directory>/<track_id>/index.md`

2. **Check Index:** Read the index and find a matching link label.

3. **Resolve Path:** Resolve relative to the directory containing that `index.md`.

4. **Fallback:** Use default paths below if index missing.

5. **Verify:** Confirm the file exists.

**Default paths (project):**

- **Product Definition**: `conductor/product.md`
- **Tech Stack**: `conductor/tech-stack.md`
- **Workflow**: `conductor/workflow.md`
- **Product Guidelines**: `conductor/product-guidelines.md`
- **Tracks Registry**: `conductor/tracks.md`
- **Tracks Directory**: `conductor/tracks/`

**Default paths (track):**

- **Specification**: `conductor/tracks/<track_id>/spec.md`
- **Implementation Plan**: `conductor/tracks/<track_id>/plan.md`
- **Metadata**: `conductor/tracks/<track_id>/metadata.json`
