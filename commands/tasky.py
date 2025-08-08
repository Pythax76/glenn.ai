import json, os, time
DATA_PATH = os.path.join("data","tasky.json")

def _load():
    if not os.path.exists("data"): os.makedirs("data", exist_ok=True)
    if not os.path.exists(DATA_PATH): return {"tasks":[]}
    with open(DATA_PATH,"r",encoding="utf-8") as f:
        return json.load(f)

def _save(state):
    with open(DATA_PATH,"w",encoding="utf-8") as f:
        json.dump(state,f,indent=2)

def run(action="list", task=None, **kwargs):
    """
    tasky.queue:
      action=list                 -> show tasks
      action=add task="..."       -> add a task
    """
    state = _load()
    if action == "add":
        if not task:
            return "Tasky: no 'task=' provided."
        item = {"id": int(time.time()), "task": task, "ts": time.strftime("%Y-%m-%d %H:%M:%S")}
        state["tasks"].append(item)
        _save(state)
        print(f"Tasky: added -> {item['task']}")
        return f"Task count: {len(state['tasks'])}"
    else:
        # list
        if not state["tasks"]:
            return "Tasky: (no tasks)"
        print("Tasky: current queue")
        for t in state["tasks"]:
            print(f"  - [{t['id']}] {t['task']}  ({t['ts']})")
        return f"Task count: {len(state['tasks'])}"
