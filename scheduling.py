import streamlit as st
import time
import pandas as pd

class Process:
    def __init__(self, pid, priority, burst_time, arrival_time):
        self.pid = pid
        self.priority = priority
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.time_slice = self.calculate_time_slice()
        self.remaining_time = burst_time
        self.waiting_time = 0
        self.completion_time = 0
        self.original_at = arrival_time
        self.original_bt = burst_time
    
    def calculate_time_slice(self):
        return max(1, max(2, 6 - self.priority))

    def execute(self, chart):
        st.write(f"Process {self.pid} is executing with priority {self.priority} and time slice {self.time_slice}.")
        time.sleep(1)
        self.remaining_time -= self.time_slice
        self.waiting_time = 0
        if self.remaining_time < 0:
            r = self.time_slice + self.remaining_time
            self.completion_time += r
            for i in range(r):
                chart.append(f"p{self.pid}")
            self.remaining_time = 0
        else:
            r = self.time_slice
            self.completion_time += r
            for i in range(r):
                chart.append(f"p{self.pid}")
        st.write(f"Process {self.pid} remaining time: {self.remaining_time}")
        return r

    def is_finished(self):
        return self.remaining_time == 0

    def get_tat_and_wt(self):
        tat = self.completion_time - self.original_at
        wt = tat - self.original_bt
        return [tat, wt]

class ULE_Scheduler:
    def __init__(self, processes):
        self.processes = processes
        self.active_queue = []
        for process in processes:
            self.active_queue.append(process)
        self.expired_queue = []
        self.chart = []

    def adjust_priority(self):
        sorted_processes = sorted(self.processes, key=lambda x: x.waiting_time, reverse=True)
        for i, process in enumerate(sorted_processes):
            process.priority = i + 1

    def schedule(self):
        copy = sorted(self.active_queue, key=lambda x: x.priority)
        process_to_execute = None
        for i in copy:
            if i.arrival_time <= 0:
                process_to_execute = i
                break
        if process_to_execute is None:
            for i in self.expired_queue:
                if i.arrival_time <= 0:
                    process_to_execute = i
                    break
        r = process_to_execute.execute(self.chart)

        for i in self.processes:
            if i != process_to_execute:
                i.waiting_time += process_to_execute.time_slice
                i.arrival_time -= process_to_execute.time_slice
                i.completion_time += r

        if process_to_execute.is_finished():
            st.write(f"Process {process_to_execute.pid} finished.")
            self.active_queue.remove(process_to_execute)
            self.processes.remove(process_to_execute)
        else:
            if process_to_execute in self.active_queue:
                self.expired_queue.append(process_to_execute)
                self.active_queue.remove(process_to_execute)

        time.sleep(0.5)

    def load_balancing(self):
        if len(self.active_queue) < len(self.expired_queue):
            self.active_queue += self.expired_queue
            self.expired_queue = []
            self.adjust_priority()

    def run(self):
        while self.active_queue:
            self.schedule()
            self.load_balancing()
            time.sleep(0.1)

def main():
    st.title("ULE Scheduler")

    if "processes" not in st.session_state:
        st.session_state.processes = []
    if "pid" not in st.session_state:
        st.session_state.pid = 1

    st.subheader("Add Process")
    priority = st.number_input(f"Enter priority for process {st.session_state.pid}:", min_value=1, max_value=5, value=3)
    arrival_time = st.number_input(f"Enter arrival time for process {st.session_state.pid}:", min_value=0, value=0)
    burst_time = st.number_input(f"Enter burst time for process {st.session_state.pid}:", min_value=1, value=1)
    add_process = st.button("Add Process")

    if add_process:
        p = Process(st.session_state.pid, priority, burst_time, arrival_time)
        st.session_state.processes.append(p)
        st.session_state.pid += 1

    if st.session_state.processes:
        st.write("### Process List")
        process_list = [(p.pid, p.priority, p.burst_time, p.arrival_time) for p in st.session_state.processes]
        df = pd.DataFrame(process_list, columns=["ID", "Priority", "Burst Time", "Arrival Time"])
        st.table(df)

        if st.button("Start Scheduling"):
            c = st.session_state.processes.copy()
            scheduler = ULE_Scheduler(st.session_state.processes)
            scheduler.run()
            st.success("Scheduling Completed")
            tat = 0
            wt = 0
            for p in c:
                l = p.get_tat_and_wt()
                tat += l[0]
                wt += l[1]
            avg_tat = tat / len(c)
            avg_wt = wt / len(c)

            st.write("\n### Results")
            st.write(f"Average Turnaround Time: {avg_tat} ms")
            st.write(f"Average Waiting Time: {avg_wt} ms")
            st.write("\n### Gantt Chart")
            st.write(" | ".join(scheduler.chart))

if __name__ == "__main__":
    main()
