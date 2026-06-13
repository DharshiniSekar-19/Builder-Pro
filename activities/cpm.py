from collections import defaultdict, deque

class CPMEngine:
    def __init__(self, activities):
        self.activities = {a.id: a for a in activities}
        self.activity_list = activities

    def calculate(self):
        if not self.activity_list:
            return []

        adj = defaultdict(list)
        indegree = defaultdict(int)
        all_ids = set()

        for activity in self.activity_list:
            all_ids.add(activity.id)
            if activity.id not in indegree:
                indegree[activity.id] = 0

        for activity in self.activity_list:
            preds = activity.predecessors.all()
            for pred in preds:
                pred_id = pred.predecessor_activity.id
                adj[pred_id].append(activity.id)
                indegree[activity.id] += 1
                all_ids.add(pred_id)

        q = deque()
        for aid in all_ids:
            if indegree[aid] == 0:
                q.append(aid)

        topo_order = []
        temp_indegree = indegree.copy()
        while q:
            u = q.popleft()
            topo_order.append(u)
            for v in adj[u]:
                temp_indegree[v] -= 1
                if temp_indegree[v] == 0:
                    q.append(v)

        earliest = defaultdict(float)

        for node in topo_order:
            act = self.activities.get(node)
            if act:
                dur = act.expected_duration
                max_pred_ef = 0
                for pred in act.predecessors.all():
                    pred_id = pred.predecessor_activity.id
                    if earliest[pred_id] > max_pred_ef:
                        max_pred_ef = earliest[pred_id]
                act.earliest_start = round(max_pred_ef, 2)
                act.earliest_finish = round(max_pred_ef + dur, 2)
                earliest[node] = act.earliest_finish

        project_end = max(earliest.values()) if earliest else 0

        latest = defaultdict(lambda: float('inf'))
        for node in reversed(topo_order):
            act = self.activities.get(node)
            if act:
                if not act.dependents.exists():
                    latest[node] = project_end
                else:
                    min_ls = float('inf')
                    for dep in act.dependents.all():
                        dep_act = dep.activity
                        dep_dur = dep_act.expected_duration
                        ls_val = latest[dep_act.id] - dep_dur
                        if ls_val < min_ls:
                            min_ls = ls_val
                    latest[node] = min_ls

                act.latest_finish = round(latest[node], 2)
                act.latest_start = round(latest[node] - act.expected_duration, 2)
                act.float_time = round(act.latest_start - act.earliest_start, 2)
                act.is_critical = abs(act.float_time) < 0.001
                act.save()

        critical_path = [a for a in self.activity_list if a.is_critical]
        return critical_path


def run_cpm(project):
    activities = list(project.activities.all())
    engine = CPMEngine(activities)
    return engine.calculate()
