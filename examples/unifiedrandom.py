from clustersim.core.simulator import Simulator

from clustersim.core.workload import Task, Job, UnifiedRandomWorkload
from clustersim.core.resources import Cpu, Mem, Gpu, Node
import clustersim.core.scheduler

from matplotlib import pyplot as plt
from simpy import Environment

sim = Simulator()

sim.add_node({'gpu': Gpu([1, 1, 1, 1])})
dispatcher = sim.add_dispatcher('random')

dispatcher.add_workload('unified_random',
                        income_range=(4, 12), tasktime_range=(16, 36),
                        resources={'gpu': Gpu([0.5, 0.5])})
dispatcher.add_scheduler('basic', sim.nodes)

sim.run(until=20000)

# Print out the node statistics
node_stats = sim.nodes[0].records
index = [t[0] for t in node_stats['gpu-util']]
value = [t[1] for t in node_stats['gpu-util']]
# Print out the task statistics
s_rec = sim.dispatcher.schedulers[0].records
task_runtime = [v[1] for v in s_rec['task_runtime']]
task_waittime = [v[1] for v in s_rec['task_waittime']]
task_total = [v[1] for v in s_rec['task_total']]

fig, sub = plt.subplots(2, 2)

sub[0][0].hist(task_runtime, bins=range(
    int(min(task_runtime)), int(max(task_runtime)), 2))
sub[0][0].set_title('run time dist')

sub[0][1].hist(task_waittime, range(
    int(min(task_waittime)), int(max(task_waittime)), 2))
sub[0][1].set_title('task wait time dist')

sub[1][0].hist(task_total, range(
    int(min(task_total)), int(max(task_total)), 2))
sub[1][0].set_title('task total time dist')

sub[1][1].plot(index, value)
sub[1][1].set_title('gpu utilization')

plt.show()
