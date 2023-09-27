import nmap
import schedule
import time
from datetime import datetime
import threading

scan_count = 0  # Variable to keep track of the scan count
stop_scanning = threading.Event()  # Event to signal the termination of the scanning loop

def run_nmap_scan(target_ip):
    global scan_count
    scan_count += 1  # Increment the scan count
    print(f"\nScanning target IP: {target_ip}")

    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=target_ip, arguments='-Pn')
    except Exception as e:
        print(f"Error during Nmap scan: {e}")
        return []

    results = []
    for host in nm.all_hosts():
        host_result = {"host": host, "ports": []}

        if 'tcp' in nm[host]:
            for port in nm[host]['tcp'].keys():
                port_info = {
                    "port": port,
                    "service": nm[host]['tcp'][port]['name'],
                    "state": nm[host]['tcp'][port]['state']
                }
                host_result["ports"].append(port_info)

        results.append(host_result)

    return results

def save_results_to_file(results, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for result in results:
            file.write(f"Host: {result['host']}\n")
            if result['ports']:
                file.write("Open Ports:\n")
                for port_info in result['ports']:
                    file.write(f"  - Port {port_info['port']}: {port_info['service']} ({port_info['state']})\n")
            else:
                file.write("No open ports found.\n")
            file.write("\n")

def job():
    if not stop_scanning.is_set():
        target_ip = "X.X.X.X"
        results = run_nmap_scan(target_ip)

        # Get the current date and time in DD-MM-YYYY_HH-MM-SS format
        current_datetime = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

        # Save results to a file named with the current date
        filename = f"{current_datetime}_results.txt"
        save_results_to_file(results, filename)

        # Save the current results as the new previous results
        previous_filename = "previous_scan.txt"
        save_results_to_file(results, previous_filename)

def display_status():
    global scan_count

    # Display information sentence
    print("Press 'CTRL+C' to stop the automated scanning.")

    while not stop_scanning.is_set():
        # Get the remaining time until the next scan
        next_run = schedule.get_jobs()[0].next_run
        time_remaining = max(0, (next_run - datetime.now()).total_seconds())

        # Display the scan count and time remaining
        print(f"\rScans: {scan_count} | Time until next scan: {int(time_remaining)} seconds", end='')

        time.sleep(1)

if __name__ == "__main__":
    # Run the first scan immediately
    job()

    # Schedule the repetance
    schedule.every(60).minutes.do(job)

    # Start a thread to display the status continuously
    status_thread = threading.Thread(target=display_status)
    status_thread.start()

    try:
        # Keep the script running to allow the scheduled job to execute
        while not stop_scanning.is_set():
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScript terminated by user.")

    # Set the stop_scanning event to signal termination
    stop_scanning.set()

    # Wait for threads to finish before exiting
    status_thread.join()
