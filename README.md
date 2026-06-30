# OpenBSD Concepts 

An interactive Streamlit dashboard that explains and simulates core OpenBSD operating-system concepts: its headline security features, common administration commands, key system calls, memory allocation, CPU scheduling, and process synchronization. Built as a group academic project (Group 13).

## Overview

The app is a multi-page Streamlit dashboard with a sidebar navigation menu. Each page covers a different operating-systems topic, mixing reference material (write-ups, command examples, C code listings) with small live simulations you can interact with directly in the browser.

| Page | What it covers |
|---|---|
| **Home** | Project title banner, OpenBSD logo, and group member credits. |
| **OpenBSD Features** | A reference write-up of OpenBSD's security philosophy and notable technologies (W^X, ASLR, Unveil, Pledge, pf, CARP, secure boot, etc.). |
| **Commands** | A cheat sheet of common OpenBSD administration commands (`sndioctl`, `pfctl`, `smtpd`, `relayctl`, `ftp`, `bioctl`, `ifconfig`, `sysctl`, `tmux`, `chroot`) with example usage. |
| **System Calls** | An explanation of the socket-based system call sequence (`socket`, `setsockopt`, `bind`, `listen`, `accept`, `poll`, `read`, `send`, `close`) alongside a full C example program implementing a multi-client poll-based server. |
| **Buddy Allocator** | An interactive simulation of the buddy memory allocation algorithm — specify a memory size, allocate and deallocate blocks, and watch the free list and allocation tree update. |
| **ULE Scheduler** | An interactive simulation of priority-based scheduling inspired by the ULE scheduler — add processes with a priority, arrival time, and burst time, then run the scheduler and view a Gantt-style execution chart. |
| **Synchronization** | A write-up of classical synchronization problems (the Cigarette Smokers problem and a construction-worker mutual-exclusion scenario) with C `pthread` example code, plus a live threaded simulation you can start from the UI. |

## Project Structure

```
OpenBSD-main/
├── ui.py               # Entry point: sidebar navigation and page routing
├── features.py          # "OpenBSD Features" reference page
├── commands.py           # "Commands" cheat-sheet page
├── system_calls.py       # "System Calls" reference + C example page
├── memory.py              # "Buddy Allocator" interactive simulation
├── scheduling.py          # "ULE Scheduler" interactive simulation
├── synchronization.py     # "Synchronization" reference + live threaded demo
├── output.png             # Sample screenshot
└── outputsync.png          # Sample screenshot (synchronization page)
```

`ui.py` is the Streamlit entry point. It imports each topic module and routes to the corresponding `main()` (or `desc()`/`home()`) function based on the sidebar selection.

## Requirements

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [pandas](https://pandas.pydata.org/)

Install dependencies:

```bash
pip install streamlit pandas
```

> Note: no `requirements.txt` is included in this archive — the two packages above (plus standard-library modules such as `threading` and `time`) are sufficient to run every page.

## Running the App

From the project directory:

```bash
streamlit run ui.py
```

This launches a local web server (by default at `http://localhost:8501`) and opens the dashboard in your browser. Use the **"Choose a feature"** dropdown in the sidebar to switch between pages.

## Interactive Simulations

A few pages go beyond static text and let you drive a simulation:

- **Buddy Allocator** (`memory.py`) — enter a usable memory size, then allocate and deallocate blocks by index to see how the buddy system splits and merges free blocks.
- **ULE Scheduler** (`scheduling.py`) — add multiple processes (priority, arrival time, burst time) and click "Start Scheduling" to watch a simulated priority-based round-robin execution.
- **Synchronization** (`synchronization.py`) — click "Start Work" to run a live multi-threaded simulation of the construction-worker synchronization scenario described on the page.

