import threading
import time
import streamlit as st

def desc():
    st.title("Synchronization")
    st.header("Classical Problem - Cigarette Smoker Problem")
    st.write("""
    The scenario for the cigarette smokers problem consists of four threads: three smokers and one agent.
    In order to smoke, the smoker needs to acquire three items: tobacco, paper, and a match. Once the smoker has all three, they combine the paper and tobacco to roll a cigarette and use the match to light it.
    Each of the three smokers has an infinite supply of exactly one item and needs the other two.
    """)
    st.header("Synchronization Problem")
    st.write("""
    Three construction workers – a carpenter, electrician, and plumber – need to complete tasks in the same house.

    Each worker has access to common tools such as measuring tape and screwdrivers.

    Domain-specific tools (e.g., hammers, wire strippers, wrenches) are provided by the construction manager and available to the worker whose domain they belong to.

    The construction manager places only one of these tools at a time, and the worker whose domain the tool belongs to picks it up and starts working.

    After his/her work is complete, the construction manager places one of these tools again, and so on.
    """)

    st.header("C Program for Synchronization")
    st.code("""
    #include <stdio.h>
    #include <stdlib.h>
    #include <pthread.h>
    #include <unistd.h>
    #include <stdbool.h>

    pthread_mutex_t area;
    pthread_cond_t work_done;
    int current_worker = 0;  // 0: carpenter, 1: electrician, 2: plumber

    int total_work = 0;
    int carpenter_work = 0;
    int electrician_work = 0;
    int plumber_work = 0;

    #define TIME_LIMIT 45

    void *carpenter(void *arg) {
        while (carpenter_work < 100) {
            pthread_mutex_lock(&area);
            while (current_worker != 0) {
                pthread_cond_wait(&work_done, &area);
            }
            printf("Carpenter has acquired hammer.../n");
            sleep(1);
            for (int i = 15; i <= TIME_LIMIT; i += 15) {
                printf("Carpenter working for 15 mins.../n");
                total_work += 20;
                carpenter_work += 20;
                if (carpenter_work >= 100) {
                    break;
                }
                sleep(1);
            }
            if (carpenter_work >= 100) {
                printf("Carpenter has finished his work/n");
                sleep(1);
            } else {
                printf("TIME LIMIT REACHED/n");
                sleep(1);
            }
            current_worker = 1;
            pthread_cond_broadcast(&work_done);
            pthread_mutex_unlock(&area);
        }
        return NULL;
    }

    void *electrician(void *arg) {
        while (electrician_work < 100) {
            pthread_mutex_lock(&area);
            while (current_worker != 1) {
                pthread_cond_wait(&work_done, &area);
            }
            printf("Electrician has acquired wire stripper.../n");
            sleep(1);
            for (int i = 15; i <= TIME_LIMIT; i += 15) {
                printf("Electrician working for 15 mins.../n");
                total_work += 25;
                electrician_work += 25;
                if (electrician_work >= 100) {
                    break;
                }
                sleep(1);
            }
            if (electrician_work >= 100) {
                printf("Electrician has finished his work/n");
                sleep(1);
            } else {
                printf("TIME LIMIT REACHED/n");
                sleep(1);
            }
            current_worker = 2; 
            pthread_cond_broadcast(&work_done);
            pthread_mutex_unlock(&area);
        }
        return NULL;
    }

    void *plumber(void *arg) {
        while (plumber_work < 100) {
            pthread_mutex_lock(&area);
            while (current_worker != 2) {
                pthread_cond_wait(&work_done, &area);
            }
            printf("Plumber has acquired wrench.../n");
            sleep(1);
            for (int i = 15; i <= TIME_LIMIT; i += 15) {
                printf("Plumber working for 15 mins.../n");
                total_work += 50;
                plumber_work += 50;
                if (plumber_work >= 100) {
                    break;
                }
                sleep(1);
            }
            if (plumber_work >= 100) {
                printf("Plumber has finished his work/n");
                sleep(1);
            } else {
                printf("TIME LIMIT REACHED/n");
                sleep(1);
            }
            current_worker = 0;
            pthread_cond_broadcast(&work_done);
            pthread_mutex_unlock(&area);
        }
        return NULL;
    }

    void *construction_manager(void *arg) {
        while (total_work < 300) {
            pthread_mutex_lock(&area);
            pthread_cond_broadcast(&work_done);
            while (current_worker != 0) {
                pthread_cond_wait(&work_done, &area);
            }
            while (current_worker != 1) {
                pthread_cond_wait(&work_done, &area);
            }
            while (current_worker != 2) {
                pthread_cond_wait(&work_done, &area);
            }
            pthread_mutex_unlock(&area);
        }
        return NULL;
    }

    int main(int argc, char *argv[]) {
        pthread_t workers[3], const_manager;
        pthread_mutex_init(&area, NULL);
        pthread_cond_init(&work_done, NULL);
        
        pthread_create(&workers[0], NULL, &carpenter, NULL);
        pthread_create(&workers[1], NULL, &electrician, NULL);
        pthread_create(&workers[2], NULL, &plumber, NULL);
        pthread_create(&const_manager, NULL, &construction_manager, NULL);
        
        pthread_join(workers[0], NULL);
        pthread_join(workers[1], NULL);
        pthread_join(workers[2], NULL);
        pthread_join(const_manager, NULL);

        pthread_mutex_destroy(&area);
        pthread_cond_destroy(&work_done);
        
        return 0;
    }
    """, language="c")
    st.header("Output")
    st.image("outputsync.png")


import streamlit as st
import threading
import time

# Shared variables and locks
area_lock = threading.Lock()
work_done = threading.Condition(area_lock)
current_worker = 0  # 0: carpenter, 1: electrician, 2: plumber

total_work = 0
carpenter_work = 0
electrician_work = 0
plumber_work = 0

MAX_WORK = 300
TIME_LIMIT = 45

def update_progress_bar(progress, value, max_value):
    progress.progress(min(value, max_value) / max_value)

def carpenter():
    global total_work, carpenter_work, current_worker
    while carpenter_work < 100:
        with area_lock:
            while current_worker != 0:
                work_done.wait()
            st.write("Carpenter has acquired hammer...")
            for i in range(3):
                st.write("Carpenter working for 15 mins...")
                total_work += 20
                carpenter_work += 20
                time.sleep(1)
                if carpenter_work >= 100:
                    break
            if carpenter_work >= 100:
                st.write("Carpenter has finished his work")
            current_worker = 1
            work_done.notify_all()

def electrician():
    global total_work, electrician_work, current_worker
    while electrician_work < 100:
        with area_lock:
            while current_worker != 1:
                work_done.wait()
            st.write("Electrician has acquired wire stripper...")
            for i in range(3):
                st.write("Electrician working for 15 mins...")
                total_work += 25
                electrician_work += 25
                time.sleep(1)
                if electrician_work >= 100:
                    break
            if electrician_work >= 100:
                st.write("Electrician has finished his work")
            current_worker = 2
            work_done.notify_all()

def plumber():
    global total_work, plumber_work, current_worker
    while plumber_work < 100:
        with area_lock:
            while current_worker != 2:
                work_done.wait()
            st.write("Plumber has acquired wrench...")
            for i in range(3):
                st.write("Plumber working for 15 mins...")
                total_work += 50
                plumber_work += 50
                time.sleep(1)
                if plumber_work >= 100:
                    break
            if plumber_work >= 100:
                st.write("Plumber has finished his work")
            current_worker = 0
            work_done.notify_all()

def construction_manager():
    global current_worker, total_work
    while total_work < MAX_WORK:
        with area_lock:
            if current_worker == 0:
                st.write("Carpenter's turn")
            elif current_worker == 1:
                st.write("Electrician's turn")
            elif current_worker == 2:
                st.write("Plumber's turn")
            work_done.notify_all()
        time.sleep(0.1)  # Give workers a chance to acquire the lock

def main():
    desc()
    st.header("Construction Workers Synchronization(Visual)")

    start_button = st.button("Start Work")

    if start_button:
        st.subheader("Carpenter")
        progress_carpenter = st.progress(0)
        st.subheader("Electrician")
        progress_electrician = st.progress(0)
        st.subheader("Plumber")
        progress_plumber = st.progress(0)
        st.subheader("Total work")
        progress_total = st.progress(0)

        # Threads for workers
        t1 = threading.Thread(target=carpenter)
        t2 = threading.Thread(target=electrician)
        t3 = threading.Thread(target=plumber)
        t4 = threading.Thread(target=construction_manager)

        t4.start()
        t1.start()
        t2.start()
        t3.start()

        while total_work < MAX_WORK or carpenter_work < 100 or electrician_work < 100 or plumber_work < 100:
            update_progress_bar(progress_carpenter, carpenter_work, 100)
            update_progress_bar(progress_electrician, electrician_work, 100)
            update_progress_bar(progress_plumber, plumber_work, 100)
            update_progress_bar(progress_total, total_work, MAX_WORK)
            time.sleep(0.1)

        t1.join()
        t2.join()
        t3.join()
        t4.join()

        # Ensure progress bars are fully filled
        update_progress_bar(progress_carpenter, carpenter_work, 100)
        update_progress_bar(progress_electrician, electrician_work, 100)
        update_progress_bar(progress_plumber, plumber_work, 100)
        update_progress_bar(progress_total, total_work, MAX_WORK)

        st.write("All work completed!")

if __name__ == "__main__":
    main()

