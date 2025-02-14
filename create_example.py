import os

def create_ansible_example():
    """
    Creates the Ansible variable precedence example directory and files.
    """

    base_dir = "ansible_variable_precedence"
    inventory_dir = os.path.join(base_dir, "inventory")
    group_vars_dir = os.path.join(inventory_dir, "group_vars")
    host_vars_dir = os.path.join(inventory_dir, "host_vars")
    roles_dir = os.path.join(base_dir, "roles")
    example_role_dir = os.path.join(roles_dir, "example_role")
    role_defaults_dir = os.path.join(example_role_dir, "defaults")
    role_vars_dir = os.path.join(example_role_dir, "vars")

    # Create Directories
    os.makedirs(group_vars_dir, exist_ok=True)
    os.makedirs(host_vars_dir, exist_ok=True)
    os.makedirs(role_defaults_dir, exist_ok=True)
    os.makedirs(role_vars_dir, exist_ok=True)

    # Create files and write content

    # inventory/hosts.ini
    hosts_ini_content = """[webservers]
webserver.example.com ansible_host=your_target_host  # Replace with your actual target host or localhost for testing

[webservers:vars]
group_inventory_var="Defined in group inventory"
"""
    with open(os.path.join(inventory_dir, "hosts.ini"), "w") as f:
        f.write(hosts_ini_content)

    # inventory/group_vars/all.yml
    group_vars_all_content = """message: " ECHO Message from group_vars/all [P2]"
"""
    with open(os.path.join(group_vars_dir, "all.yml"), "w") as f:
        f.write(group_vars_all_content)

    # inventory/host_vars/webserver.example.com.yml
    host_vars_content = """message: " ECHO Message from host_vars/webserver.example.com [P4]"
host_var: "This is a host variable"
"""
    with open(os.path.join(host_vars_dir, "webserver.example.com.yml"), "w") as f:
        f.write(host_vars_content)

    # roles/example_role/defaults/main.yml
    role_defaults_content = """message: " ECHO Message from Role Defaults [P1]"
role_default_var: "Role Default Var - Not Overridden Directly" # Just for illustration
"""
    with open(os.path.join(role_defaults_dir, "main.yml"), "w") as f:
        f.write(role_defaults_content)

    # roles/example_role/vars/main.yml
    role_vars_content = """message: " ECHO Message from Role Vars [P6]"
role_vars_var: "Role Vars Var - Not Overridden Directly" # Just for illustration
"""
    with open(os.path.join(role_vars_dir, "main.yml"), "w") as f:
        f.write(role_vars_content)

    # playbook.yml
    playbook_content = """---
- hosts: webservers
  gather_facts: false
  vars:
    message: " ECHO Message from Play Vars [P7]"
  vars_files:
    - vars_file.yml
  vars_prompt:
    - name: prompted_message
      prompt: "Enter a message [P9]"
      private: no
  roles:
    - role: example_role
      vars:
        message: " ECHO Message from Role Parameters [P15]" # Role Parameters
  tasks:
    - name: Print Message - Task Vars
      debug:
        msg: "Final Message (Task Vars) [P11]: {{ message }}"
      vars:
        message: " ECHO Message from Task Vars [P11]" # Task Vars

    - name: Print Message - Block Vars
      block:
        - debug:
            msg: "Block Message (Block Vars) [P10]: {{ message }}"
          vars:
            message: " ECHO Message from Block Vars [P10]" # Block Vars
        - debug:
            msg: "Message After Set Fact [P13 Overwrite Block P10]: {{ message }}" # Demonstrating Set Fact Overwrite
      vars:
        message: " ECHO Message Block Level Before Set Fact [P10 - Will be Overwritten]" # Block level variable

    - name: Set Fact
      set_fact:
        message: " ECHO Message from Set Fact [P13]"

    - name: Print Message - Vars Prompt
      debug:
        msg: "Prompted Message (Vars Prompt) [P9]: {{ prompted_message }}"

    - name: Print Message - Vars File
      debug:
        msg: "Vars File Message (Vars File) [P8]: {{ message }}"

    - name: Print Message - Role Default
      debug:
        msg: "Role Default Message [P1]: {{ message }}" # Will be Overwritten by Higher Precedence in Play

    - name: Print Message - Role Vars
      debug:
        msg: "Role Vars Message [P6]: {{ message }}" # Will be Overwritten by Higher Precedence in Play

    - name: Print Message - Group var
      debug:
        msg: "Group Var Message [P2]: {{ message }}" # Will be Overwritten by Higher Precedence in Play

    - name: Print Message - Host Var
      debug:
        msg: "Host Var Message [P4]: {{ message }}" # Will be Overwritten by Higher Precedence in Play

    - name: Print Message - Play Var
      debug:
        msg: "Play Var Message [P7]: {{ message }}" # Play Var Level

    - name: Print Message - Role Parameter
      debug:
        msg: "Role Parameter Message [P15]: {{ message }}" # Role Parameter Level - Overrides lower role vars and defaults

    - name: Final Message - Showing Highest Play Precedence - Role Parameter
      debug:
        msg: "Final Message (Highest Play Precedence - Role Parameter) [P15 visible]: {{ message }}" # Highest Precedence in this Play - Role Parameter
"""
    with open(os.path.join(base_dir, "playbook.yml"), "w") as f:
        f.write(playbook_content)

    # vars_file.yml
    vars_file_content = """vars_file_message: " ECHO Message from vars_file.yml [P8]"
message: " ECHO Message from Vars File [P8]" # Overriding again for example
"""
    with open(os.path.join(base_dir, "vars_file.yml"), "w") as f:
        f.write(vars_file_content)

    print(f"Ansible variable precedence example structure created in '{base_dir}' directory.")
    print("Remember to replace 'your_target_host' in 'inventory/hosts.ini' with your actual target or 'localhost' for local testing.")

if __name__ == "__main__":
    create_ansible_example()
