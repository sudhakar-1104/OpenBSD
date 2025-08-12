import streamlit as st

class BuddyAllocator:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.free_list = [[16, total_memory + 15]]
        self.allocated_blocks = []
        self.binarytree = [-1] * total_memory
        self.binarytree[0] = [16, total_memory + 15]

    def allocate(self, size):
        index = self.find_block(size)

        if index == -1:
            return -1

        while (self.free_list[index][1] - self.free_list[index][0] + 1) > size and (self.free_list[index][1] - self.free_list[index][0] + 1) // 2 >= size:
            self.split_block(index)

        allocated_block = self.free_list.pop(index)
        self.allocated_blocks.append(allocated_block)
        return allocated_block

    def free(self, ind):
        if ind == 0:
            return 0
        block = self.find_block_to_free(ind)
        if block == -1:
            return -1

        if (self.free_list!=[]):
            flag = 1
            for i, b in enumerate(self.free_list):
                if block[1] < b[0]:
                    self.free_list.insert(i, block)
                    self.allocated_blocks.remove(block)
                    flag = 0
                    break
            if flag == 1:
                self.free_list.append(block)
                self.allocated_blocks.remove(block)
        else:
            self.free_list.append(block)
            i=0

        while self.merge_with_buddy(0):
            continue

        return block

    def find_block(self, size):
        for i, block in enumerate(self.free_list):
            if (block[1] - block[0] + 1) >= size:
                return i
        return -1

    def split_block(self, index):
        start = self.free_list[index][0]
        end = self.free_list[index][1]
        block_size = (end - start + 1) // 2
        bin_index = self.binarytree.index(self.free_list[index])
        self.free_list[index] = [start, start + block_size - 1]
        self.free_list.insert(index + 1, [start + block_size, end])
        self.binarytree[(bin_index * 2) + 1] = self.free_list[index]
        self.binarytree[(bin_index * 2) + 2] = self.free_list[index + 1]

    def merge_with_buddy(self, index):
        if len(self.free_list) == 1:
            return False

        block = self.free_list[index]
        bin_index = self.binarytree.index(block)

        if bin_index % 2 == 0:
            buddy_index = bin_index - 1
        else:
            buddy_index = bin_index + 1

        buddy = self.binarytree[buddy_index]

        try:
            buddy_index = self.free_list.index(buddy)
        except ValueError:
            return False

        if index < buddy_index:
            self.free_list[index] = [block[0], buddy[1]]
            self.free_list.pop(buddy_index)
        else:
            self.free_list[index] = [buddy[0], block[1]]
            self.free_list.pop(buddy_index)

        return True

    def find_block_to_free(self, ind):
        for i in self.allocated_blocks:
            if i[0] == ind:
                return i
        return -1

def printfree(free_list, total_memory):
    memory_visual = ["<div style='font-family:monospace; font-size:14px; line-height:1.6;'>"]
    l = []
    for i in free_list:
        l.append(i[0])
        l.append(i[1])
    i = 0
    j = 0
    flag = 1

    while i <= 16:
        if i == 0:
            memory_visual.append(f"{i}|")
        elif i - 1 == 15:
            memory_visual.append(f"{i - 1}")
            break
        else:
            memory_visual.append("|")
        j = j + 1
        i = j * 2

    while i <= total_memory + 16:
        if i in l:
            flag = 0
            if i != 16:
                memory_visual.append(f"<span style='color:red;'>{i - 1}</span>")
                memory_visual.append(f"<span style='color:green;'>{i}_</span>")
            else:
                memory_visual.append(f"<span style='color:green;'>{i}_</span>")
        elif i - 1 in l:
            flag = 1
            if (i - 1) != total_memory + 15:
                memory_visual.append(f"<span style='color:red;'>_{i - 1}</span>")
                memory_visual.append(f"<span style='color:green;'>{i}</span>")
            else:
                memory_visual.append(f"<span style='color:red;'>_{i - 1}</span>")
        else:
            if i == 16:
                memory_visual.append(f"<span style='color:green;'>{i}</span>")
            if flag == 0:
                memory_visual.append("_")
            else:
                memory_visual.append("|")
            if (i - 1) == total_memory + 15:
                memory_visual.append(f"<span style='color:red;'>{i - 1}</span>")
        j = j + 1
        i = j * 2
    memory_visual.append("</div>")
    st.write("".join(memory_visual), unsafe_allow_html=True)

def main():
    st.title("Buddy Allocator")

    if "allocator" not in st.session_state:
        total_memory = st.number_input("Specify size of usable memory in bits (Excluding first 16 bits for OS):", min_value=1, value=32)
        st.session_state.allocator = BuddyAllocator(total_memory)
        st.session_state.total_memory = total_memory

    allocator = st.session_state.allocator
    total_memory = st.session_state.total_memory

    st.header("Memory Map")
    printfree(allocator.free_list, total_memory)

    action = st.radio("Choose action:", ["Allocate memory", "Deallocate memory"])

    if action == "Allocate memory":
        size = st.number_input("Specify size of memory you want to allocate:", min_value=1, value=1, key="allocate_size")
        if st.button("Allocate"):
            allocated_block = allocator.allocate(size)
            if allocated_block == -1:
                st.error("Not enough memory to allocate")
            else:
                st.success(f"Memory allocated from {allocated_block[0]} to {allocated_block[1]}")
            printfree(allocator.free_list, total_memory)
    elif action == "Deallocate memory":
        if allocator.allocated_blocks:
            sindex = st.number_input("Enter start index of block you want to deallocate:", min_value=1, key="deallocate_index")
            if st.button("Deallocate"):
                a = allocator.free(sindex)
                if a == -1:
                    st.error("Invalid starting index")
                elif a == 0:
                    st.warning("Memory at 0 allocated for OS")
                else:
                    st.success(f"Memory deallocated from {a[0]} to {a[1]}")
                    st.write(f"{(a[1] - a[0] + 1)} bits deallocated")
                printfree(allocator.free_list, total_memory)
        else:
            st.warning("No memory allocated")

if __name__ == "__main__":
    main()
