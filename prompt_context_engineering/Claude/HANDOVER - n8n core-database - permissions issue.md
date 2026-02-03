Claude Prompt (copy/paste)

You are an n8n core-database / permissions expert. I need root-cause analysis and a concrete fix.

Problem

After migrating to / running n8n 2.1.4 in Docker, the UI shows zero workflows (“Create your first workflow”), but the SQLite DB clearly contains 23 workflows with valid nodes JSON. We believe this is related to project-binding / permissions / schema expectations in newer n8n versions. We attempted DB patches to link workflows to projects and user to project; DB joins prove visibility should exist; UI still empty.

Environment

Docker Compose stack in ~/sigma-aetl-kafka/docker-compose.yml

n8n image: n8nio/n8n:latest logs show Version 2.1.4

SQLite in Docker volume: sigma-aetl-kafka_n8n_data

UI: http://<vm-ip>:5678

User email: fguiccia@gmail.com

userId: fbe0f72a-c8ac-45c4-b707-b92c5d56e330

personal projectId: H2GJWoUSsXsS8l14 name “Ferruccio Guicciardi fguiccia@gmail.com
”

urgent workflowId: ailnL2CjgyztQEl3 name “SIGMA-AELT Minimal Validator Test”

n8n logs excerpt (no obvious errors)

n8n ready on ::, port 5678

Version: 2.1.4

Warning: Python runner missing (JS runner registered). UI accessible.

Database facts (verified with sqlite3)

Workflows exist:

SELECT COUNT(*) FROM workflow_entity;  -- 23


Nodes JSON present:

SELECT COUNT(*) FROM workflow_entity WHERE nodes IS NOT NULL AND LENGTH(nodes) > 10;  -- 23


All workflows linked to project in shared_workflow:

SELECT COUNT(*) FROM shared_workflow WHERE projectId='H2GJWoUSsXsS8l14'; -- 23


No orphaned workflows:

SELECT COUNT(*) 
FROM workflow_entity w 
LEFT JOIN shared_workflow s ON s.workflowId=w.id
WHERE s.projectId IS NULL;  -- 0


User belongs to project:

SELECT projectId,userId,role 
FROM project_relation 
WHERE userId='fbe0f72a-c8ac-45c4-b707-b92c5d56e330';
-- returns H2GJWoUSsXsS8l14 | ... | project:admin


Project exists:

SELECT id,name,type,createdAt FROM project;
-- H2GJWoUSsXsS8l14 | ... | personal | 2025-09-07 ...


DB join proves “user should see workflows”:

SELECT w.id,w.name,p.name AS project_name,pr.role AS user_role
FROM workflow_entity w
JOIN shared_workflow sw ON sw.workflowId=w.id
JOIN project p ON p.id=sw.projectId
JOIN project_relation pr ON pr.projectId=p.id
WHERE pr.userId='fbe0f72a-c8ac-45c4-b707-b92c5d56e330';
-- returns 23 rows

What we already tried

Insert shared_workflow rows:

INSERT OR IGNORE INTO shared_workflow (workflowId, projectId, role)
SELECT id,'H2GJWoUSsXsS8l14','owner' FROM workflow_entity;


Insert / update project_relation:

INSERT OR IGNORE INTO project_relation (projectId,userId,role)
VALUES ('H2GJWoUSsXsS8l14','fbe0f72a-c8ac-45c4-b707-b92c5d56e330','project:admin');

UPDATE project_relation SET role='project:admin'
WHERE projectId='H2GJWoUSsXsS8l14'
AND userId='fbe0f72a-c8ac-45c4-b707-b92c5d56e330';


Restarted containers:

docker compose down && docker compose up -d

docker compose restart n8n (from correct folder)

UI STILL shows no workflows.

We attempted “migrations” via docker run but likely invoked wrong:

docker run ... n8nio/n8n:2.1.4 n8n migrate gave “Command n8n not found”

docker run ... n8nio/n8n:2.1.4 migrate gave “Command migrate not found”

API probe:

curl http://localhost:5678/api/v1/workflows returns {"message":"'X-N8N-API-KEY' header required"}

Your tasks (must be concrete, no generic advice)

Please do ALL of the following:

(A) Identify what the UI actually queries in n8n 2.1.4

Which tables/joins determine workflow list visibility?

Is shared_workflow + project_relation sufficient?

Are there additional ACL/ownership tables or special handling for personal projects?

(B) Check whether our schema indicates we are missing migrations

Example: workflow_entity does NOT have projectId column (update failed: “no such column projectId”).

Do we need migrations to add columns/tables for 2.1.4?

If yes, specify exactly what should exist.

(C) Provide the correct Docker commands to run n8n migrations

Exact command line(s) for n8n 2.1.4 in Docker using SQLite in the mounted volume.

Include correct entrypoint usage, working directory, and env vars if needed.

Assume volume mount is either /home/node/.n8n or /data but we can adjust.

(D) Provide a minimal DB patch that makes workflows visible in UI

If another table is missing: show exact INSERT statements.

If roles are wrong: show exact role values required for personal projects (e.g., project:personalOwner vs project:admin).

If the UI needs a “default project selection” record somewhere: show it.

(E) Credentials

Provide equivalent verification queries and fix for credentials visibility.

Likely tables: credentials_entity, shared_credentials (please confirm).

(F) Output format

Return:

A short root cause statement

A checklist of verification queries

A “Fix Plan” with exact commands + SQL in correct order

A fallback: how to export + re-import at least workflow ailnL2CjgyztQEl3 safely

Important: treat this like production recovery. Assume we already proved data exists. We need the missing link between DB state and UI listing.
