import json
import shutil
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible import context
import ansible.constants as C
from ansible.executor.playbook_executor import PlaybookExecutor

class ResultCallback(CallbackBase):

    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_unreachable(self, result):
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))

class RunPlaybook(object):

    def __init__(self, private_key_file=None):
        self.options = ImmutableDict(
            connection='smart',
            remote_user=None,
            remote_password=None,
            private_key_file=private_key_file,
            sudo=None,
            sudo_user=None,
            ask_sudo_pass=None,
            module_path=None,
            become=None,
            become_method=None,
            become_user=None,
            check=False,
            diff=False,
            listhosts=None,
            listtasks=None,
            listtags=None,
            verbosity=3,
            syntax=None,
            start_at_task=None,
            inventory=None)

        self.loader = DataLoader()
        self.passwords = dict()

    def run(self, playbook_path, inventory):
        context.CLIARGS = self.options
        self.inventory = InventoryManager(loader=self.loader, sources=inventory)
        variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

        self.executor = PlaybookExecutor(
            playbooks=playbook_path,
            inventory=self.inventory,
            variable_manager=variable_manager,
            loader=self.loader,
            passwords=self.passwords,
        )

        self.executor._tqm._stdout_callback = ResultCallback()
        result = self.executor.run()
        return result
