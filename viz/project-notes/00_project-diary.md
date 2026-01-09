
# [[2026-02-26]]

## Tasks
```dataviewjs 
await dv.taskList
	(dv.pages('"Projects/IT/20260109_ExaGo_viz"')
		.file
			.tasks
				.where(t => !t.completed				
					&& t.text.includes("(fix) build viz")
					| t.text.includes("test")
					//&& t.tags.includes("#testtag")
					//&& t.due >= dv.date("2024-04-15") 
					//&& t.created \<?\> dv.date("")
					//&& t.start \<?\> dv.date("")
					//&& t.scheduled \<?\> dv.date("")
					//&& t.repeat 
					//&& t.status 
					//&& t.priority
				)
				//.groupBy(g => g.header)
				.sort(s => s.due, 'desc')
	, false												
	)
```
# DONE
- [x] (docs) MR/PR  [developer guidelines](https://github.com/pnnl/ExaGO/blob/develop/docs/developer_guidelines.md#p023-keep-mrs-up-to-date-with-target-branch) guides to keep fork `feature-branch` updated with `develop` branch actually updates it with fork `origin/develop`, not `upstream/develop` (original branch)  [created:: 2026-02-02]  [completion:: 2026-02-27]
	- [RESULT](https://github.com/pnnl/ExaGO/pull/205)
- [x] fork for minor `developer guidelines` merge request  [completion:: 2026-02-25]
- [x] (git) update to upstream develop  [created:: 2026-02-25 ] [completion:: 2026-02-25]
- [x] (issue) adopt [LangSmith Studio local server deploy](https://docs.langchain.com/oss/python/langchain/studio#setup-local-agent-server) debug, prompt management, testing, monitoring, annotstion  [created:: 2026-02-01]  [completion:: 2026-02-25]
	- RESULT: it is up automatically on `langgraph dev`
- [x] (build) [app folder structure: folders, files](https://docs.langchain.com/oss/python/langgraph/application-structure)  [id:: knt6gu]  [created:: 2026-02-01]  [due:: 2026-02-09]  [completion:: 2026-02-21]
	- RESULT: [chatgrid agentic AI backend](https://github.com/Walter462/ExaGO/blob/191-add-sql-context-management/viz/chatgrid_backend/README.md), [chatgrid chat user interface](https://github.com/Walter462/ExaGO/blob/191-add-sql-context-management/viz/chatgrid_chat_ui/README.md)
	- [LangSmith Deployment](https://docs.langchain.com/langsmith/deployments)
	- [langsmith/local-server](https://docs.langchain.com/langsmith/local-server)
- [x] build agent ui: multi-platform image  [created:: 2026-02-08]  [due:: 2026-02-09]  [completion:: 2026-02-21]
	- [RESULT: docker file](https://hub.docker.com/r/walternzd/chatgrid_chat_ui)
- [x] (issue) adopt [LangChain Agent Chat UI](https://docs.langchain.com/oss/python/langgraph/ui), in frontend to ensure `time-travel`, `human in the loop` and other features: [Agent Chat UI features YT video](https://youtu.be/lInrwVnZ83o)  [created:: 2026-02-01]  [completion:: 2026-02-21]
	- RESULT: [Initial commit of chatgrid_backend (AI agent) and chatgrid_chat_ui (chat window user interface) modules](https://github.com/Walter462/ExaGO/commit/7851c1cf70af47ebabf57fd50588bfbcb35f5d98)
---
- [x] build agent server  [created:: 2026-02-06]  [completion:: 2026-02-08]
	- long-term memory (SQL) not working without license -> solution aegra
	- [RESULT: docker file](https://hub.docker.com/repositories/walternzd)
- [x] build lang smith   [created:: 2026-02-06] [completion:: 2026-02-08]
- [x] build agent chat UI  [created:: 2026-02-06]  [completion:: 2026-02-08]
	- not working on arm64
	-  [RESULT: docker file](https://hub.docker.com/repositories/walternzd)
- [x] (git) commit notes changes  [created:: 2026-02-04]  [due:: 2026-02-05] [completion:: 2026-02-05]
	- [RESULT](https://github.com/Walter462/ExaGO/commit/e1b484a4ffd655176867d1d2819e802bf3550b25)
- [x] (git) update origin/branches to upstream/develop  [created:: 2026-02-04]  [due:: 2026-02-05]  [completion:: 2026-02-05]
	- [RESULT](https://github.com/Walter462/ExaGO/commit/e1b484a4ffd655176867d1d2819e802bf3550b25)
---
>git<->obsidian project notes sync 
- [x] (viz/project notes/)test script [created:: 2026-02-03] [completion:: 2026-02-03]
- [x] (viz/project notes/) make script executable [created:: 2026-02-03]  
- [x] (viz/)update .gitignore [created:: 2026-02-03]  [completion:: 2026-02-03]
- [x] (viz/project notes/) add local notes folder/note (git <-> obsidian) sync tool (unison) [created:: 2026-02-03]  [completion:: 2026-02-03]
---
- [x] (dev tools & docs) attach [LangChainMCP](https://docs.langchain.com/use-these-docs)  [created:: 2026-02-01]  [completion:: 2026-02-02]
