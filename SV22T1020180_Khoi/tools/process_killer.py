import tkinter as tk
from tkinter import ttk, messagebox
import subprocess


class ProcessKiller:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Killer")
        self.root.geometry("850x560")
        self.root.resizable(True, True)
        self.root.configure(bg="#1e1e2e")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        background="#2d2d44",
                        foreground="#cdd6f4",
                        fieldbackground="#2d2d44",
                        rowheight=24,
                        font=("Segoe UI", 9))
        style.configure("Treeview.Heading",
                        background="#45475a",
                        foreground="#cdd6f4",
                        font=("Segoe UI", 9, "bold"))
        style.map("Treeview",
                  background=[("selected", "#585b70")],
                  foreground=[("selected", "#f5e0dc")])
        style.configure("TNotebook", background="#1e1e2e")
        style.configure("TNotebook.Tab",
                        background="#313244", foreground="#cdd6f4",
                        padding=[14, 4],
                        font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", "#45475a")],
                  foreground=[("selected", "#f5e0dc")])

        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        self.tab_process = tk.Frame(notebook, bg="#1e1e2e")
        self.tab_port = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(self.tab_process, text="  Process  ")
        notebook.add(self.tab_port, text="  Kill theo Port  ")

        self._build_process_tab()
        self._build_port_tab()

    # ── Tab 1: Process ──
    def _build_process_tab(self):
        tab = self.tab_process

        top = tk.Frame(tab, bg="#1e1e2e", padx=10, pady=8)
        top.pack(fill=tk.X)

        tk.Label(top, text="Tìm kiếm:", bg="#1e1e2e", fg="#a6adc8",
                 font=("Segoe UI", 10)).pack(side=tk.LEFT)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.filter_list())
        ttk.Entry(top, textvariable=self.search_var, width=28).pack(side=tk.LEFT, padx=(6, 12))

        for text, cmd, bg in [
            ("Làm mới", self.load_processes, "#89b4fa"),
            ("Kill đã chọn", self.kill_selected, "#f38ba8"),
            ("Chọn tất cả", self.select_all, "#a6e3a1"),
            ("Bỏ chọn", self.deselect_all, "#fab387"),
        ]:
            tk.Button(top, text=text, command=cmd, bg=bg, fg="#1e1e2e",
                      font=("Segoe UI", 9, "bold"), relief=tk.FLAT,
                      padx=10, pady=2, cursor="hand2").pack(side=tk.LEFT, padx=3)

        tree_frame = tk.Frame(tab, bg="#1e1e2e", padx=10, pady=4)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(tree_frame,
                                 columns=("pid", "name", "mem"),
                                 show="headings", selectmode="extended")
        self.tree.heading("pid", text="PID", anchor=tk.W)
        self.tree.heading("name", text="Tên Process", anchor=tk.W)
        self.tree.heading("mem", text="Memory (KB)", anchor=tk.E)
        self.tree.column("pid", width=70, minwidth=60)
        self.tree.column("name", width=420, minwidth=200)
        self.tree.column("mem", width=120, minwidth=80, anchor=tk.E)

        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        bottom = tk.Frame(tab, bg="#1e1e2e", padx=10, pady=6)
        bottom.pack(fill=tk.X)
        self.status_var = tk.StringVar(value="Nhấn 'Làm mới' để tải danh sách")
        tk.Label(bottom, textvariable=self.status_var, bg="#1e1e2e", fg="#6c7086",
                 font=("Segoe UI", 9)).pack(side=tk.LEFT)

        self.all_processes = []
        self.load_processes()

    # ── Tab 2: Port ──
    def _build_port_tab(self):
        tab = self.tab_port

        top = tk.Frame(tab, bg="#1e1e2e", padx=10, pady=8)
        top.pack(fill=tk.X)

        tk.Label(top, text="Nhập port:", bg="#1e1e2e", fg="#a6adc8",
                 font=("Segoe UI", 10)).pack(side=tk.LEFT)

        self.port_var = tk.StringVar()
        port_entry = ttk.Entry(top, textvariable=self.port_var, width=12)
        port_entry.pack(side=tk.LEFT, padx=(6, 12))
        port_entry.bind("<Return>", lambda e: self.scan_port())

        tk.Button(top, text="Tìm process", command=self.scan_port,
                  bg="#89b4fa", fg="#1e1e2e",
                  font=("Segoe UI", 9, "bold"), relief=tk.FLAT,
                  padx=12, pady=2, cursor="hand2").pack(side=tk.LEFT, padx=3)

        tk.Button(top, text="Kill tất cả port này", command=self.kill_port_processes,
                  bg="#f38ba8", fg="#1e1e2e",
                  font=("Segoe UI", 9, "bold"), relief=tk.FLAT,
                  padx=12, pady=2, cursor="hand2").pack(side=tk.LEFT, padx=3)

        tk.Button(top, text="Scan tất cả port đang dùng", command=self.scan_all_ports,
                  bg="#cba6f7", fg="#1e1e2e",
                  font=("Segoe UI", 9, "bold"), relief=tk.FLAT,
                  padx=12, pady=2, cursor="hand2").pack(side=tk.LEFT, padx=3)

        tree_frame = tk.Frame(tab, bg="#1e1e2e", padx=10, pady=4)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.port_tree = ttk.Treeview(
            tree_frame,
            columns=("port", "pid", "name", "state"),
            show="headings", selectmode="extended")
        self.port_tree.heading("port", text="Port", anchor=tk.W)
        self.port_tree.heading("pid", text="PID", anchor=tk.W)
        self.port_tree.heading("name", text="Tên Process", anchor=tk.W)
        self.port_tree.heading("state", text="Trạng thái", anchor=tk.W)
        self.port_tree.column("port", width=80, minwidth=60)
        self.port_tree.column("pid", width=80, minwidth=60)
        self.port_tree.column("name", width=350, minwidth=150)
        self.port_tree.column("state", width=120, minwidth=80)

        vsb2 = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.port_tree.yview)
        self.port_tree.configure(yscrollcommand=vsb2.set)
        self.port_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb2.pack(side=tk.RIGHT, fill=tk.Y)

        bottom = tk.Frame(tab, bg="#1e1e2e", padx=10, pady=6)
        bottom.pack(fill=tk.X)
        self.port_status = tk.StringVar(value="Nhập port (VD: 5143) rồi nhấn Tìm, hoặc Scan tất cả")
        tk.Label(bottom, textvariable=self.port_status, bg="#1e1e2e", fg="#6c7086",
                 font=("Segoe UI", 9)).pack(side=tk.LEFT)

    # ── Process tab logic ──
    def load_processes(self):
        self.all_processes.clear()
        try:
            result = subprocess.run(
                ["tasklist", "/FO", "CSV", "/NH"],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            for line in result.stdout.strip().splitlines():
                parts = line.replace('"', '').split(',')
                if len(parts) >= 5:
                    name = parts[0].strip()
                    pid = parts[1].strip()
                    mem = parts[4].strip().replace(' K', '').replace(',', '').replace('.', '')
                    if pid.isdigit():
                        self.all_processes.append((pid, name, mem))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lấy danh sách process:\n{e}")
            return
        self.all_processes.sort(key=lambda x: x[1].lower())
        self.filter_list()
        self.status_var.set(f"Tổng cộng: {len(self.all_processes)} process")

    def filter_list(self):
        keyword = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        count = 0
        for pid, name, mem in self.all_processes:
            if keyword in name.lower() or keyword in pid:
                self.tree.insert("", tk.END, values=(pid, name, mem))
                count += 1
        self.status_var.set(f"Hiển thị: {count} / {len(self.all_processes)} process")

    def select_all(self):
        self.tree.selection_set(self.tree.get_children())

    def deselect_all(self):
        self.tree.selection_remove(*self.tree.selection())

    def kill_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn ít nhất một process.")
            return
        names = [f"  {self.tree.item(i, 'values')[1]} (PID: {self.tree.item(i, 'values')[0]})"
                 for i in selected]
        if not messagebox.askyesno(
                "Xác nhận Kill",
                f"Kill {len(selected)} process?\n\n"
                + "\n".join(names[:15])
                + ("\n  ..." if len(names) > 15 else "")):
            return
        killed, failed = self._kill_pids([self.tree.item(i, "values")[0] for i in selected])
        messagebox.showinfo("Kết quả", f"Đã kill: {killed}\nThất bại: {failed}")
        self.load_processes()

    # ── Port tab logic ──
    def _get_pid_name(self, pid):
        try:
            result = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            for line in result.stdout.strip().splitlines():
                parts = line.replace('"', '').split(',')
                if len(parts) >= 2 and parts[1].strip() == str(pid):
                    return parts[0].strip()
        except Exception:
            pass
        return "???"

    def _parse_netstat(self, port_filter=None):
        rows = []
        seen_pids = set()
        try:
            result = subprocess.run(
                ["netstat", "-ano", "-p", "TCP"],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) < 5:
                    continue
                if parts[0] not in ("TCP",):
                    continue
                local = parts[1]
                state = parts[3]
                pid = parts[4]
                if not pid.isdigit() or pid == "0":
                    continue
                port = local.rsplit(":", 1)[-1] if ":" in local else ""
                if port_filter and port != str(port_filter):
                    continue
                if state == "LISTENING":
                    key = (port, pid)
                    if key not in seen_pids:
                        seen_pids.add(key)
                        name = self._get_pid_name(pid)
                        rows.append((port, pid, name, state))
                elif not port_filter:
                    continue
                else:
                    key = (port, pid)
                    if key not in seen_pids:
                        seen_pids.add(key)
                        name = self._get_pid_name(pid)
                        rows.append((port, pid, name, state))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể chạy netstat:\n{e}")
        return rows

    def scan_port(self):
        port = self.port_var.get().strip()
        if not port.isdigit():
            messagebox.showwarning("Sai port", "Vui lòng nhập số port hợp lệ (VD: 5143)")
            return
        self.port_tree.delete(*self.port_tree.get_children())
        self.port_status.set(f"Đang tìm process trên port {port}...")
        self.root.update_idletasks()

        rows = self._parse_netstat(port_filter=port)
        for r in rows:
            self.port_tree.insert("", tk.END, values=r)

        if rows:
            self.port_status.set(f"Tìm thấy {len(rows)} process trên port {port}")
        else:
            self.port_status.set(f"Không có process nào đang dùng port {port}")

    def scan_all_ports(self):
        self.port_tree.delete(*self.port_tree.get_children())
        self.port_status.set("Đang scan tất cả port LISTENING...")
        self.root.update_idletasks()

        rows = self._parse_netstat()
        rows.sort(key=lambda x: int(x[0]) if x[0].isdigit() else 0)
        for r in rows:
            self.port_tree.insert("", tk.END, values=r)
        self.port_status.set(f"Tổng cộng: {len(rows)} port đang LISTENING")

    def kill_port_processes(self):
        port = self.port_var.get().strip()
        items = self.port_tree.get_children()
        if not items:
            messagebox.showwarning("Trống", "Chưa có process nào. Hãy Tìm hoặc Scan trước.")
            return

        selected = self.port_tree.selection()
        targets = selected if selected else items
        pids = list(set(self.port_tree.item(i, "values")[1] for i in targets))
        names = [f"  PID {p} - {self.port_tree.item(i, 'values')[2]}"
                 for i in targets for p in [self.port_tree.item(i, 'values')[1]]]

        label = f"port {port}" if port.isdigit() else "các port đã scan"
        if not messagebox.askyesno(
                "Xác nhận Kill",
                f"Kill {len(pids)} process trên {label}?\n\n"
                + "\n".join(names[:15])
                + ("\n  ..." if len(names) > 15 else "")):
            return

        killed, failed = self._kill_pids(pids)
        messagebox.showinfo("Kết quả", f"Đã kill: {killed}\nThất bại: {failed}")
        if port.isdigit():
            self.scan_port()
        else:
            self.scan_all_ports()

    # ── Shared ──
    def _kill_pids(self, pids):
        killed = failed = 0
        for pid in pids:
            try:
                r = subprocess.run(
                    ["taskkill", "/PID", str(pid), "/T", "/F"],
                    capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                if r.returncode == 0:
                    killed += 1
                else:
                    failed += 1
            except Exception:
                failed += 1
        return killed, failed


if __name__ == "__main__":
    root = tk.Tk()
    ProcessKiller(root)
    root.mainloop()
