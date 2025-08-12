import streamlit as st

def main():
    st.header("Commands")
    st.write("""
    **sndioctl**: A control utility for the OpenBSD sndio audio system.
    ```sh
    sndioctl
    ```
    
    **pfctl**: A utility for managing OpenBSD's Packet Filter (PF).
    ```sh
    pfctl -f /etc/pf.conf
    pfctl -sr
    pftcl -F all
    ```
    
    **smtpd**: A utility for managing simple mail transfer protocol daemon.
    ```sh
    smtpd -d
    ```
    
    **relayctl**: A relay daemon for load balancing and application layer filtering.
    ```sh
    relayctl reload
    relayctl show summary
    ```

    **ftp**: The File Transfer Protocol client for transferring files.
    ```sh
    ftp ftp.openbsd.org
    ```
    
    **bioctl**: A utility to manage RAID volumes.
    ```sh
    bioctl sd0
    ```
    
    **ifconfig**: A utility to configure network interfaces.
    ```sh
    ifconfig em0 up
    ifconfig em0 inet 192.168.1.2 netmask 255.255.255.0
    ```
    
    **hostname.if**: Interface-specific hostname configuration files.
    ```sh
    echo "dhcp" > /etc/hostname.em0
    ```
    
    **sysctl**: A utility to view and change kernel parameters at runtime.
    ```sh
    sysctl kern.version
    sysctl -w net.inet.ip.forwarding=1
    ```
    
    **tmux**: A terminal multiplexer.
    ```sh
    tmux new -s session_name
    tmux attach -t session_name
    ```
    
    **chroot**: A utility to change the root directory for a process.
    ```sh
    chroot /var/www
    ```
    """)
