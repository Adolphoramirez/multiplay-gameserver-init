#!/usr/bin/env python
# -*- coding: utf-8 -*-

from AnsiblePlaybook import RunPlaybook

inventory = ",".join(["175.24.247.12",]) + ","

ansible = RunPlaybook()
print(ansible.run(inventory=inventory, playbook_path=["playbooks/server_init.yml",]))
