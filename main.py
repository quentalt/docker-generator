import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, ttk


class DockerFileGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Docker File Generator")

        # Dockerfile Section
        self.dockerfile_frame = tk.LabelFrame(root, text="Dockerfile", padx=10, pady=10)
        self.dockerfile_frame.pack(padx=10, pady=10, fill="both", expand="yes")

        tk.Label(self.dockerfile_frame, text="Base Image:").grid(row=0, column=0, sticky="w")
        self.base_image_entry = tk.Entry(self.dockerfile_frame, width=30)
        self.base_image_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.dockerfile_frame, text="Label:").grid(row=1, column=0, sticky="w")
        self.label_entry = tk.Entry(self.dockerfile_frame, width=30)
        self.label_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.dockerfile_frame, text="Command:").grid(row=2, column=0, sticky="w")
        self.command_entry = tk.Entry(self.dockerfile_frame, width=30)
        self.command_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.dockerfile_frame, text="Workdir:").grid(row=3, column=0, sticky="w")
        self.workdir_entry = tk.Entry(self.dockerfile_frame, width=30)
        self.workdir_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.dockerfile_frame, text="Copy:").grid(row=4, column=0, sticky="w")
        self.copy_entry = tk.Entry(self.dockerfile_frame, width=30)
        self.copy_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.dockerfile_frame, text="Expose:").grid(row=5, column=0, sticky="w")
        self.expose_entry = tk.Entry(self.dockerfile_frame, width=30)
        self.expose_entry.grid(row=5, column=1, padx=5, pady=5)

        self.generate_dockerfile_button = tk.Button(self.dockerfile_frame, text="Generate Dockerfile",
                                                    command=self.generate_dockerfile)
        self.generate_dockerfile_button.grid(row=6, columnspan=2, pady=10)

        # Docker Compose Section
        self.compose_frame = tk.LabelFrame(root, text="Docker Compose", padx=10, pady=10)
        self.compose_frame.pack(padx=10, pady=10, fill="both", expand="yes")

        self.services = []

        self.add_service_button = tk.Button(self.compose_frame, text="Add Service", command=self.add_service)
        self.add_service_button.grid(row=0, columnspan=2, pady=10)

        self.service_listbox = tk.Listbox(self.compose_frame, width=50, height=10)
        self.service_listbox.grid(row=1, columnspan=2, padx=5, pady=5)

        self.modify_service_button = tk.Button(self.compose_frame, text="Modify Service", command=self.modify_service)
        self.modify_service_button.grid(row=2, column=0, pady=10)

        self.delete_service_button = tk.Button(self.compose_frame, text="Delete Service", command=self.delete_service)
        self.delete_service_button.grid(row=2, column=1, pady=10)

        self.generate_compose_button = tk.Button(self.compose_frame, text="Generate Docker Compose",
                                                 command=self.generate_docker_compose)
        self.generate_compose_button.grid(row=3, columnspan=2, pady=10)

    def add_service(self):
        service_name = simpledialog.askstring("Service Name", "Enter the service name:")
        if not service_name:
            return

        image = simpledialog.askstring("Image", "Enter the image name:")
        if not image:
            return

        ports = simpledialog.askstring("Ports", "Enter the ports (e.g., 80:80):")
        if not ports:
            return

        volumes = simpledialog.askstring("Volumes", "Enter the volumes (comma-separated, optional):")
        env_vars = simpledialog.askstring("Environment Variables",
                                          "Enter the environment variables (comma-separated, optional):")

        service = {
            "name": service_name,
            "image": image,
            "ports": ports,
            "volumes": volumes,
            "env_vars": env_vars
        }

        self.services.append(service)
        self.service_listbox.insert(tk.END, service_name)
        messagebox.showinfo("Success", f"Service '{service_name}' added successfully!")

    def modify_service(self):
        selected_index = self.service_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No service selected!")
            return

        index = selected_index[0]
        service = self.services[index]

        service_name = simpledialog.askstring("Service Name", "Enter the service name:", initialvalue=service["name"])
        if not service_name:
            return

        image = simpledialog.askstring("Image", "Enter the image name:", initialvalue=service["image"])
        if not image:
            return

        ports = simpledialog.askstring("Ports", "Enter the ports (e.g., 80:80):", initialvalue=service["ports"])
        if not ports:
            return

        volumes = simpledialog.askstring("Volumes", "Enter the volumes (comma-separated, optional):",
                                         initialvalue=service["volumes"])
        env_vars = simpledialog.askstring("Environment Variables",
                                          "Enter the environment variables (comma-separated, optional):",
                                          initialvalue=service["env_vars"])

        service["name"] = service_name
        service["image"] = image
        service["ports"] = ports
        service["volumes"] = volumes
        service["env_vars"] = env_vars

        self.service_listbox.delete(index)
        self.service_listbox.insert(index, service_name)
        messagebox.showinfo("Success", f"Service '{service_name}' modified successfully!")

    def delete_service(self):
        selected_index = self.service_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No service selected!")
            return

        index = selected_index[0]
        service_name = self.services[index]["name"]

        del self.services[index]
        self.service_listbox.delete(index)
        messagebox.showinfo("Success", f"Service '{service_name}' deleted successfully!")

    def generate_dockerfile(self):
        base_image = self.base_image_entry.get()
        label = self.label_entry.get()
        command = self.command_entry.get()
        workdir = self.workdir_entry.get()
        copy = self.copy_entry.get()
        expose = self.expose_entry.get()

        if not base_image or not label or not command:
            messagebox.showerror("Error", "Base Image, Label, and Command fields are required!")
            return

        dockerfile_content = f"FROM {base_image}\nLABEL label=\"{label}\"\n"

        if workdir:
            dockerfile_content += f"WORKDIR {workdir}\n"

        if copy:
            dockerfile_content += f"COPY {copy}\n"

        if expose:
            dockerfile_content += f"EXPOSE {expose}\n"

        dockerfile_content += f"RUN {command}\n"

        file_path = filedialog.asksaveasfilename(defaultextension=".Dockerfile",
                                                 filetypes=[("Dockerfile", "*.Dockerfile")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(dockerfile_content.strip())
            messagebox.showinfo("Success", "Dockerfile generated successfully!")

    def generate_docker_compose(self):
        if not self.services:
            messagebox.showerror("Error", "No services added!")
            return

        docker_compose_content = "version: '3'\nservices:\n"

        for service in self.services:
            docker_compose_content += f"  {service['name']}:\n"
            docker_compose_content += f"    image: {service['image']}\n"
            docker_compose_content += f"    ports:\n      - \"{service['ports']}\"\n"

            if service['volumes']:
                volumes_list = service['volumes'].split(",")
                docker_compose_content += "    volumes:\n"
                for volume in volumes_list:
                    docker_compose_content += f"      - {volume}\n"

            if service['env_vars']:
                env_list = service['env_vars'].split(",")
                docker_compose_content += "    environment:\n"
                for env in env_list:
                    docker_compose_content += f"      - {env}\n"

        file_path = filedialog.asksaveasfilename(defaultextension=".yml", filetypes=[("YAML files", "*.yml")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(docker_compose_content.strip())
            messagebox.showinfo("Success", "Docker Compose file generated successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = DockerFileGeneratorApp(root)
    root.mainloop()
