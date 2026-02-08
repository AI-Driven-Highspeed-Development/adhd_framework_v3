from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from config_manager import ConfigManager

@dataclass
class ConfigKeys:
	___DATA___: Dict[str, Any] | None = None
	def dict_get(self, key: str, default: Any = None) -> Any:
		'Dictionary-style access to raw data. Prefer typed attributes when possible.'
		if self.___DATA___ is None:
			return default
		return self.___DATA___.get(key, default)
	def __getitem__(self, key: str) -> Any:
		if self.___DATA___ is None or key not in self.___DATA___:
			raise KeyError(key)
		return self.___DATA___[key]
	cli_manager: Optional['Cli_M'] = None
	temp_files_manager: Optional['TempFiles_M'] = None
	modules_controller_core: Optional['ModulesControllerCore'] = None
	workspace_core: Optional['WorkspaceCore'] = None
	exceptions_core: Optional['ExceptionsCore'] = None
	adhd_mcp: Optional['AdhdMcp'] = None
	uv_migrator_core: Optional['UvMigratorCore'] = None
	instruction_core: Optional['InstructionCore'] = None
	flow_core: Optional['FlowCore'] = None
	project_creator_core: Optional['ProjectCreatorCore'] = None
	module_creator_core: Optional['ModuleCreatorCore'] = None
	creator_common_core: Optional['CreatorCommonCore'] = None
	github_api_core: Optional['GithubApiCore'] = None
	my_module: Optional['MyModule'] = None
	questionary_core: Optional['QuestionaryCore'] = None
	yaml_reading_core: Optional['YamlReadingCore'] = None
	project_init_core: Optional['ProjectInitCore'] = None

	@staticmethod
	def from_raw(raw: Dict[str, Any] | None) -> 'ConfigKeys':
		inst = ConfigKeys()
		inst.___DATA___ = raw or {}
		inst._populate(raw or {})
		return inst

	def _populate(self, data: Dict[str, Any]):
		self.___DATA___ = data
		self.cli_manager = self.Cli_M.from_raw(data.get('cli_manager', {}))
		self.temp_files_manager = self.TempFiles_M.from_raw(data.get('temp_files_manager', {}))
		self.modules_controller_core = self.ModulesControllerCore.from_raw(data.get('modules_controller_core', {}))
		self.workspace_core = self.WorkspaceCore.from_raw(data.get('workspace_core', {}))
		self.exceptions_core = self.ExceptionsCore.from_raw(data.get('exceptions_core', {}))
		self.adhd_mcp = self.AdhdMcp.from_raw(data.get('adhd_mcp', {}))
		self.uv_migrator_core = self.UvMigratorCore.from_raw(data.get('uv_migrator_core', {}))
		self.instruction_core = self.InstructionCore.from_raw(data.get('instruction_core', {}))
		self.flow_core = self.FlowCore.from_raw(data.get('flow_core', {}))
		self.project_creator_core = self.ProjectCreatorCore.from_raw(data.get('project_creator_core', {}))
		self.module_creator_core = self.ModuleCreatorCore.from_raw(data.get('module_creator_core', {}))
		self.creator_common_core = self.CreatorCommonCore.from_raw(data.get('creator_common_core', {}))
		self.github_api_core = self.GithubApiCore.from_raw(data.get('github_api_core', {}))
		self.my_module = self.MyModule.from_raw(data.get('my_module', {}))
		self.questionary_core = self.QuestionaryCore.from_raw(data.get('questionary_core', {}))
		self.yaml_reading_core = self.YamlReadingCore.from_raw(data.get('yaml_reading_core', {}))
		self.project_init_core = self.ProjectInitCore.from_raw(data.get('project_init_core', {}))

	def __init__(self):
		self._populate({'cli_manager': {'module_name': 'cli_manager', 'path': {'data': './project/data/cli_manager'}, 'admin_cli': {'filename': 'admin_cli.py', 'output_dir': './'}}, 'temp_files_manager': {'module_name': 'temp_files_manager', 'path': {'data': './project/data/temp_files_manager', 'unix_temp': '/tmp/github_api_core', 'windows_temp': 'C:\\\\Temp\\\\github_api_core'}}, 'modules_controller_core': {'module_name': 'modules_controller_core', 'path': {'data': './project/data/modules_controller_core'}}, 'workspace_core': {'module_name': 'workspace_core', 'path': {'data': './project/data/workspace_core'}}, 'exceptions_core': {'module_name': 'exceptions_core', 'path': {'data': './project/data/exceptions_core'}}, 'adhd_mcp': {'module_name': 'adhd_mcp', 'path': {'data': './project/data/adhd_mcp'}}, 'uv_migrator_core': {'module_name': 'uv_migrator_core', 'path': {'data': './project/data/uv_migrator_core'}}, 'instruction_core': {'module_name': 'instruction_core', 'path': {'data': './project/data/instruction_core', 'official_target_dir': ['./.github'], 'custom_target_dir': [], 'mcp_permission_injection_json': './project/data/instruction_core/mcp_permission_injection.json'}}, 'flow_core': {'module_name': 'flow_core', 'path': {'data': './project/data/flow_core'}}, 'project_creator_core': {'module_name': 'project_creator_core', 'path': {'data': './project/data/project_creator_core', 'project_templates': './project/data/project_creator_core/project_templates.yaml', 'module_preload_sets': './project/data/project_creator_core/module_preload_sets.yaml'}}, 'module_creator_core': {'module_name': 'module_creator_core', 'path': {'data': './project/data/module_creator_core', 'module_templates': './project/data/module_creator_core/module_templates.yaml'}}, 'creator_common_core': {'module_name': 'creator_common_core', 'path': {'data': './project/data/creator_common_core'}}, 'github_api_core': {'module_name': 'github_api_core', 'path': {'data': './project/data/github_api_core'}}, 'my_module': {'module_name': 'my_module', 'path': {'data': './project/data/my_module'}}, 'questionary_core': {'module_name': 'questionary_core', 'path': {'data': './project/data/questionary_core'}}, 'yaml_reading_core': {'module_name': 'yaml_reading_core', 'path': {'data': './project/data/yaml_reading_core'}}, 'project_init_core': {'module_name': 'project_init_core', 'path': {'data': './project/data/project_init_core'}, 'framework_repo_url': 'https://github.com/AI-Driven-Highspeed-Development/ai_driven_highspeed_development_framework_bootstrapped'}})

	@dataclass
	class Cli_M:
		___DATA___: Dict[str, Any] | None = None
		def dict_get(self, key: str, default: Any = None) -> Any:
			'Dictionary-style access to raw data. Prefer typed attributes when possible.'
			if self.___DATA___ is None:
				return default
			return self.___DATA___.get(key, default)
		def __getitem__(self, key: str) -> Any:
			if self.___DATA___ is None or key not in self.___DATA___:
				raise KeyError(key)
			return self.___DATA___[key]
		module_name: Optional[str] = "cli_manager"
		path: Optional['Path'] = None
		admin_cli: Optional['AdminCli'] = None

		@staticmethod
		def from_raw(raw: Dict[str, Any] | None) -> 'Cli_M':
			inst = ConfigKeys.Cli_M()
			inst.___DATA___ = raw or {}
			inst._populate(raw or {})
			return inst

		def _populate(self, data: Dict[str, Any]):
			self.___DATA___ = data
			self.module_name = data.get('module_name', self.module_name)
			self.path = self.Path.from_raw(data.get('path', {}))
			self.admin_cli = self.AdminCli.from_raw(data.get('admin_cli', {}))

		def __init__(self):
			pass

		@dataclass
		class Path:
			___DATA___: Dict[str, Any] | None = None
			def dict_get(self, key: str, default: Any = None) -> Any:
				'Dictionary-style access to raw data. Prefer typed attributes when possible.'
				if self.___DATA___ is None:
					return default
				return self.___DATA___.get(key, default)
			def __getitem__(self, key: str) -> Any:
				if self.___DATA___ is None or key not in self.___DATA___:
					raise KeyError(key)
				return self.___DATA___[key]
			data: Optional[str] = "./project/data/cli_manager"

			@staticmethod
			def from_raw(raw: Dict[str, Any] | None) -> 'Path':
				inst = ConfigKeys.Cli_M.Path()
				inst.___DATA___ = raw or {}
				inst._populate(raw or {})
				return inst

			def _populate(self, data: Dict[str, Any]):
				self.___DATA___ = data
				self.data = data.get('data', self.data)

			def __init__(self):
				pass


		@dataclass
		class AdminCli:
			___DATA___: Dict[str, Any] | None = None
			def dict_get(self, key: str, default: Any = None) -> Any:
				'Dictionary-style access to raw data. Prefer typed attributes when possible.'
				if self.___DATA___ is None:
					return default
				return self.___DATA___.get(key, default)
			def __getitem__(self, key: str) -> Any:
				if self.___DATA___ is None or key not in self.___DATA___:
					raise KeyError(key)
				return self.___DATA___[key]
			filename: Optional[str] = "admin_cli.py"
			output_dir: Optional[str] = "./"

			@staticmethod
			def from_raw(raw: Dict[str, Any] | None) -> 'AdminCli':
				inst = ConfigKeys.Cli_M.AdminCli()
				inst.___DATA___ = raw or {}
				inst._populate(raw or {})
				return inst

			def _populate(self, data: Dict[str, Any]):
				self.___DATA___ = data
				self.filename = data.get('filename', self.filename)
				self.output_dir = data.get('output_dir', self.output_dir)

			def __init__(self):
				pass



	@dataclass
	class TempFiles_M:
		___DATA___: Dict[str, Any] | None = None
		def dict_get(self, key: str, default: Any = None) -> Any:
			'Dictionary-style access to raw data. Prefer typed attributes when possible.'
			if self.___DATA___ is None:
				return default
			return self.___DATA___.get(key, default)
		def __getitem__(self, key: str) -> Any:
			if self.___DATA___ is None or key not in self.___DATA___:
				raise KeyError(key)
			return self.___DATA___[key]
		module_name: Optional[str] = "temp_files_manager"
		path: Optional['Path'] = None

		@staticmethod
		def from_raw(raw: Dict[str, Any] | None) -> 'TempFiles_M':
			inst = ConfigKeys.TempFiles_M()
			inst.___DATA___ = raw or {}
			inst._populate(raw or {})
			return inst

		def _populate(self, data: Dict[str, Any]):
			self.___DATA___ = data
			self.module_name = data.get('module_name', self.module_name)
			self.path = self.Path.from_raw(data.get('path', {}))

		def __init__(self):
			pass

		@dataclass
		class Path:
			___DATA___: Dict[str, Any] | None = None
			def dict_get(self, key: str, default: Any = None) -> Any:
				'Dictionary-style access to raw data. Prefer typed attributes when possible.'
				if self.___DATA___ is None:
					return default
				return self.___DATA___.get(key, default)
			def __getitem__(self, key: str) -> Any:
				if self.___DATA___ is None or key not in self.___DATA___:
					raise KeyError(key)
				return self.___DATA___[key]
			data: Optional[str] = "./project/data/temp_files_manager"
			unix_temp: Optional[str] = "/tmp/github_api_core"
			windows_temp: Optional[str] = "C:\\Temp\\github_api_core"

			@staticmethod
			def from_raw(raw: Dict[str, Any] | None) -> 'Path':
				inst = ConfigKeys.TempFiles_M.Path()
				inst.___DATA___ = raw or {}
				inst._populate(raw or {})
				return inst

			def _populate(self, data: Dict[str, Any]):
				self.___DATA___ = data
				self.data = data.get('data', self.data)
				self.unix_temp = data.get('unix_temp', self.unix_temp)
				self.windows_temp = data.get('windows_temp', self.windows_temp)

			def __init__(self):
				pass



	@dataclass
	class ModulesControllerCore:
		___DATA___: Dict[str, Any] | None = None
		def dict_get(self, key: str, default: Any = None) -> Any:
			'Dictionary-style access to raw data. Prefer typed attributes when possible.'
			if self.___DATA___ is None:
				return default
			return self.___DATA___.get(key, default)
		def __getitem__(self, key: str) -> Any:
			if self.___DATA___ is None or key not in self.___DATA___:
				raise KeyError(key)
			return self.___DATA___[key]
		module_name: Optional[str] = "modules_controller_core"
		path: Optional['Path'] = None

		@staticmethod
		def from_raw(raw: Dict[str, Any] | None) -> 'ModulesControllerCore':
			inst = ConfigKeys.ModulesControllerCore()
			inst.___DATA___ = raw or {}
			inst._populate(raw or {})
			return inst

		def _populate(self, data: Dict[str, Any]):
			self.___DATA___ = data
			self.module_name = data.get('module_name', self.module_name)
			self.path = self.Path.from_raw(data.get('path', {}))

		def __init__(self):
			pass

		@dataclass
		class Path:
			___DATA___: Dict[str, Any] | None = None
			def dict_get(self, key: str, default: Any = None) -> Any:
				'Dictionary-style access to raw data. Prefer typed attributes when possible.'
				if self.___DATA___ is None:
					return default
				return self.___DATA___.get(key, default)
			def __getitem__(self, key: str) -> Any:
				if self.___DATA___ is None or key not in self.___DATA___:
					raise KeyError(key)
				return self.___DATA___[key]
			data: Optional[str] = "./project/data/modules_controller_core"

			@staticmethod
			def from_raw(raw: Dict[str, Any] | None) -> 'Path':
				inst = ConfigKeys.ModulesControllerCore.Path()
				inst.___DATA___ = raw or {}
				inst._populate(raw or {})
				return inst

			def _populate(self, data: Dict[str, Any]):
				self.___DATA___ = data
				self.data = data.get('data', self.data)

			def __init__(self):
				pass



	@dataclass
	class WorkspaceCore:
		___DATA___: Dict[str, Any] | None = None
		def dict_get(self, key: str, default: Any = None) -> Any:
			'Dictionary-style access to raw data. Prefer typed attributes when possible.'
			if self.___DATA___ is None:
				return default
			return self.___DATA___.get(key, default)
		def __getitem__(self, key: str) -> Any:
			if self.___DATA___ is None or key not in self.___DATA___:
				raise KeyError(key)
			return self.___DATA___[key]
		module_name: Optional[str] = "workspace_core"
		path: Optional['Path'] = None

		@staticmethod
		def from_raw(raw: Dict[str, Any] | None) -> 'WorkspaceCore':
			inst = ConfigKeys.WorkspaceCore()
			inst.___DATA___ = raw or {}
			inst._populate(raw or {})
			return inst

		def _populate(self, data: Dict[str, Any]):
			self.___DATA___ = data
			self.module_name = data.get('module_name', self.module_name)
			self.path = self.Path.from_raw(data.get('path', {}))

		def __init__(self):
			pass

		@dataclass
		class Path:
			___DATA___: Dict[str, Any] | None = None
			def dict_get(self, key: str, default: Any = None) -> Any:
				'Dictionary-style access to raw data. Prefer typed attributes when possible.'
				if self.___DATA___ is None:
					return default
				return self.___DATA___.get(key, default)
			def __getitem__(self, key: str) -> Any:
				if self.___DATA___ is None or key not in self.___DATA___:
					raise KeyError(key)
				return self.___DATA___[key]
			data: Optional[str] = "./project/data/workspace_core"

			@staticmethod
			def from_raw(raw: Dict[str, Any] | None) -> 'Path':
				inst = ConfigKeys.WorkspaceCore.Path()
				inst.___DATA___ = raw or {}
				inst._populate(raw or {})
				return inst

			def _populate(self, data: Dict[str, Any]):
				self.___DATA___ = data
				self.data = data.get('data', self.data)

			def __init__(self):
				pass



	@dataclass
	class ExceptionsCore:
		___DATA___: Dict[str, Any] | None = None
		def dict_get(self, key: str, default: Any = None) -> Any:
			'Dictionary-style access to raw data. Prefer typed attributes when possible.'
			if self.___DATA___ is None:
				return default
			return self.___DATA___.get(key, default)
		def __getitem__(self, key: str) -> Any:
			if self.___DATA___ is None or key not in self.___DATA___:
				raise KeyError(key)
			return self.___DATA___[key]
		module_name: Optional[str] = "exceptions_core"
		path: Optional['Path'] = None

		@staticmethod
		def from_raw(raw: Dict[str, Any] | None) -> 'ExceptionsCore':
			inst = ConfigKeys.ExceptionsCore()
			inst.___DATA___ = raw or {}
			inst._populate(raw or {})
			return inst

		def _populate(self, data: Dict[str, Any]):
			self.___DATA___ = data
			self.module_name = data.get('module_name', self.module_name)
			self.path = self.Path.from_raw(data.get('path', {}))

		def __init__(self):
			pass

		@dataclass
		class Path:
			___DATA___: Dict[str, Any] | None = None
			def dict_get(self, key: str, default: Any = None) -> Any:
				'Dictionary-style access to raw data. Prefer typed attributes when possible.'
				if self.___DATA___ is None:
					return default
				return self.___DATA___.get(key, default)
			def __getitem__(self, key: str) -> Any:
				if self.___DATA___ is None or key not in self.___DATA___:
					raise KeyError(key)
				return self.___DATA___[key]
			data: Optional[str] = "./project/data/exceptions_core"

			@staticmethod
			def from_raw(raw: Dict[str, Any] | None) -> 'Path':
				inst = ConfigKeys.ExceptionsCore.Path()
				inst.___DATA___ = raw or {}
				inst._populate(raw or {})
				return inst

			def _populate(self, data: Dict[str, Any]):
				self.___DATA___ = data
				self.data = data.get('data', self.data)

			def __init__(self):
				pass



	@dataclass
	class AdhdMcp:
		___DATA___: Dict[str, Any] | None = None
		def dict_get(self, key: str, default: Any = None) -> Any:
			'Dictionary-style access to raw data. Prefer typed attributes when possible.'
			if self.___DATA___ is None:
				return default
			return self.___DATA___.get(key, default)
		def __getitem__(self, key: str) -> Any:
			if self.___DATA___ is None or key not in self.___DATA___:
				raise KeyError(key)
			return self.___DATA___[key]
		module_name: Optional[str] = "adhd_mcp"
		path: Optional['Path'] = None

		@staticmethod
		def from_raw(raw: Dict[str, Any] | None) -> 'AdhdMcp':
			inst = ConfigKeys.AdhdMcp()
			inst.___DATA___ = raw or {}
			inst._populate(raw or {})
			return inst

		def _populate(self, data: Dict[str, Any]):
			self.___DATA___ = data
			self.module_name = data.get('module_name', self.module_name)
			self.path = self.Path.from_raw(data.get('path', {}))

		def __init__(self):
			pass

		@dataclass
		class Path:
			___DATA___: Dict[str, Any] | None = None
			def dict_get(self, key: str, default: Any = None) -> Any:
				'Dictionary-style access to raw data. Prefer typed attributes when possible.'
				if self.___DATA___ is None:
					return default
				return self.___DATA___.get(key, default)
			def __getitem__(self, key: str) -> Any:
				if self.___DATA___ is None or key not in self.___DATA___:
					raise KeyError(key)
				return self.___DATA___[key]
			data: Optional[str] = "./project/data/adhd_mcp"

			@staticmethod
			def from_raw(raw: Dict[str, Any] | None) -> 'Path':
				inst = ConfigKeys.AdhdMcp.Path()
				inst.___DATA___ = raw or {}
				inst._populate(raw or {})
				return inst

			def _populate(self, data: Dict[str, Any]):
				self.___DATA___ = data
				self.data = data.get('data', self.data)

			def __init__(self):
				pass



	@dataclass
	class UvMigratorCore:
		___DATA___: Dict[str, Any] | None = None
		def dict_get(self, key: str, default: Any = None) -> Any:
			'Dictionary-style access to raw data. Prefer typed attributes when possible.'
			if self.___DATA___ is None:
				return default
			return self.___DATA___.get(key, default)
		def __getitem__(self, key: str) -> Any:
			if self.___DATA___ is None or key not in self.___DATA___:
				raise KeyError(key)
			return self.___DATA___[key]
		module_name: Optional[str] = "uv_migrator_core"
		path: Optional['Path'] = None

		@staticmethod
		def from_raw(raw: Dict[str, Any] | None) -> 'UvMigratorCore':
			inst = ConfigKeys.UvMigratorCore()
			inst.___DATA___ = raw or {}
			inst._populate(raw or {})
			return inst

		def _populate(self, data: Dict[str, Any]):
			self.___DATA___ = data
			self.module_name = data.get('module_name', self.module_name)
			self.path = self.Path.from_raw(data.get('path', {}))

		def __init__(self):
			pass

		@dataclass
		class Path:
			___DATA___: Dict[str, Any] | None = None
			def dict_get(self, key: str, default: Any = None) -> Any:
				'Dictionary-style access to raw data. Prefer typed attributes when possible.'
				if self.___DATA___ is None:
					return default
				return self.___DATA___.get(key, default)
			def __getitem__(self, key: str) -> Any:
				if self.___DATA___ is None or key not in self.___DATA___:
					raise KeyError(key)
				return self.___DATA___[key]
			data: Optional[str] = "./project/data/uv_migrator_core"

			@staticmethod
			def from_raw(raw: Dict[str, Any] | None) -> 'Path':
				inst = ConfigKeys.UvMigratorCore.Path()
				inst.___DATA___ = raw or {}
				inst._populate(raw or {})
				return inst

			def _populate(self, data: Dict[str, Any]):
				self.___DATA___ = data
				self.data = data.get('data', self.data)

			def __init__(self):
				pass



	@dataclass
	class InstructionCore:
		___DATA___: Dict[str, Any] | None = None
		def dict_get(self, key: str, default: Any = None) -> Any:
			'Dictionary-style access to raw data. Prefer typed attributes when possible.'
			if self.___DATA___ is None:
				return default
			return self.___DATA___.get(key, default)
		def __getitem__(self, key: str) -> Any:
			if self.___DATA___ is None or key not in self.___DATA___:
				raise KeyError(key)
			return self.___DATA___[key]
		module_name: Optional[str] = "instruction_core"
		path: Optional['Path'] = None

		@staticmethod
		def from_raw(raw: Dict[str, Any] | None) -> 'InstructionCore':
			inst = ConfigKeys.InstructionCore()
			inst.___DATA___ = raw or {}
			inst._populate(raw or {})
			return inst

		def _populate(self, data: Dict[str, Any]):
			self.___DATA___ = data
			self.module_name = data.get('module_name', self.module_name)
			self.path = self.Path.from_raw(data.get('path', {}))

		def __init__(self):
			pass

		@dataclass
		class Path:
			___DATA___: Dict[str, Any] | None = None
			def dict_get(self, key: str, default: Any = None) -> Any:
				'Dictionary-style access to raw data. Prefer typed attributes when possible.'
				if self.___DATA___ is None:
					return default
				return self.___DATA___.get(key, default)
			def __getitem__(self, key: str) -> Any:
				if self.___DATA___ is None or key not in self.___DATA___:
					raise KeyError(key)
				return self.___DATA___[key]
			data: Optional[str] = "./project/data/instruction_core"
			official_target_dir: Optional[List] = None
			custom_target_dir: Optional[List] = None
			mcp_permission_injection_json: Optional[str] = "./project/data/instruction_core/mcp_permission_injection.json"

			@staticmethod
			def from_raw(raw: Dict[str, Any] | None) -> 'Path':
				inst = ConfigKeys.InstructionCore.Path()
				inst.___DATA___ = raw or {}
				inst._populate(raw or {})
				return inst

			def _populate(self, data: Dict[str, Any]):
				self.___DATA___ = data
				self.data = data.get('data', self.data)
				self.official_target_dir = data.get('official_target_dir', self.official_target_dir)
				self.custom_target_dir = data.get('custom_target_dir', self.custom_target_dir)
				self.mcp_permission_injection_json = data.get('mcp_permission_injection_json', self.mcp_permission_injection_json)

			def __init__(self):
				pass



	@dataclass
	class FlowCore:
		___DATA___: Dict[str, Any] | None = None
		def dict_get(self, key: str, default: Any = None) -> Any:
			'Dictionary-style access to raw data. Prefer typed attributes when possible.'
			if self.___DATA___ is None:
				return default
			return self.___DATA___.get(key, default)
		def __getitem__(self, key: str) -> Any:
			if self.___DATA___ is None or key not in self.___DATA___:
				raise KeyError(key)
			return self.___DATA___[key]
		module_name: Optional[str] = "flow_core"
		path: Optional['Path'] = None

		@staticmethod
		def from_raw(raw: Dict[str, Any] | None) -> 'FlowCore':
			inst = ConfigKeys.FlowCore()
			inst.___DATA___ = raw or {}
			inst._populate(raw or {})
			return inst

		def _populate(self, data: Dict[str, Any]):
			self.___DATA___ = data
			self.module_name = data.get('module_name', self.module_name)
			self.path = self.Path.from_raw(data.get('path', {}))

		def __init__(self):
			pass

		@dataclass
		class Path:
			___DATA___: Dict[str, Any] | None = None
			def dict_get(self, key: str, default: Any = None) -> Any:
				'Dictionary-style access to raw data. Prefer typed attributes when possible.'
				if self.___DATA___ is None:
					return default
				return self.___DATA___.get(key, default)
			def __getitem__(self, key: str) -> Any:
				if self.___DATA___ is None or key not in self.___DATA___:
					raise KeyError(key)
				return self.___DATA___[key]
			data: Optional[str] = "./project/data/flow_core"

			@staticmethod
			def from_raw(raw: Dict[str, Any] | None) -> 'Path':
				inst = ConfigKeys.FlowCore.Path()
				inst.___DATA___ = raw or {}
				inst._populate(raw or {})
				return inst

			def _populate(self, data: Dict[str, Any]):
				self.___DATA___ = data
				self.data = data.get('data', self.data)

			def __init__(self):
				pass



	@dataclass
	class ProjectCreatorCore:
		___DATA___: Dict[str, Any] | None = None
		def dict_get(self, key: str, default: Any = None) -> Any:
			'Dictionary-style access to raw data. Prefer typed attributes when possible.'
			if self.___DATA___ is None:
				return default
			return self.___DATA___.get(key, default)
		def __getitem__(self, key: str) -> Any:
			if self.___DATA___ is None or key not in self.___DATA___:
				raise KeyError(key)
			return self.___DATA___[key]
		module_name: Optional[str] = "project_creator_core"
		path: Optional['Path'] = None

		@staticmethod
		def from_raw(raw: Dict[str, Any] | None) -> 'ProjectCreatorCore':
			inst = ConfigKeys.ProjectCreatorCore()
			inst.___DATA___ = raw or {}
			inst._populate(raw or {})
			return inst

		def _populate(self, data: Dict[str, Any]):
			self.___DATA___ = data
			self.module_name = data.get('module_name', self.module_name)
			self.path = self.Path.from_raw(data.get('path', {}))

		def __init__(self):
			pass

		@dataclass
		class Path:
			___DATA___: Dict[str, Any] | None = None
			def dict_get(self, key: str, default: Any = None) -> Any:
				'Dictionary-style access to raw data. Prefer typed attributes when possible.'
				if self.___DATA___ is None:
					return default
				return self.___DATA___.get(key, default)
			def __getitem__(self, key: str) -> Any:
				if self.___DATA___ is None or key not in self.___DATA___:
					raise KeyError(key)
				return self.___DATA___[key]
			data: Optional[str] = "./project/data/project_creator_core"
			project_templates: Optional[str] = "./project/data/project_creator_core/project_templates.yaml"
			module_preload_sets: Optional[str] = "./project/data/project_creator_core/module_preload_sets.yaml"

			@staticmethod
			def from_raw(raw: Dict[str, Any] | None) -> 'Path':
				inst = ConfigKeys.ProjectCreatorCore.Path()
				inst.___DATA___ = raw or {}
				inst._populate(raw or {})
				return inst

			def _populate(self, data: Dict[str, Any]):
				self.___DATA___ = data
				self.data = data.get('data', self.data)
				self.project_templates = data.get('project_templates', self.project_templates)
				self.module_preload_sets = data.get('module_preload_sets', self.module_preload_sets)

			def __init__(self):
				pass



	@dataclass
	class ModuleCreatorCore:
		___DATA___: Dict[str, Any] | None = None
		def dict_get(self, key: str, default: Any = None) -> Any:
			'Dictionary-style access to raw data. Prefer typed attributes when possible.'
			if self.___DATA___ is None:
				return default
			return self.___DATA___.get(key, default)
		def __getitem__(self, key: str) -> Any:
			if self.___DATA___ is None or key not in self.___DATA___:
				raise KeyError(key)
			return self.___DATA___[key]
		module_name: Optional[str] = "module_creator_core"
		path: Optional['Path'] = None

		@staticmethod
		def from_raw(raw: Dict[str, Any] | None) -> 'ModuleCreatorCore':
			inst = ConfigKeys.ModuleCreatorCore()
			inst.___DATA___ = raw or {}
			inst._populate(raw or {})
			return inst

		def _populate(self, data: Dict[str, Any]):
			self.___DATA___ = data
			self.module_name = data.get('module_name', self.module_name)
			self.path = self.Path.from_raw(data.get('path', {}))

		def __init__(self):
			pass

		@dataclass
		class Path:
			___DATA___: Dict[str, Any] | None = None
			def dict_get(self, key: str, default: Any = None) -> Any:
				'Dictionary-style access to raw data. Prefer typed attributes when possible.'
				if self.___DATA___ is None:
					return default
				return self.___DATA___.get(key, default)
			def __getitem__(self, key: str) -> Any:
				if self.___DATA___ is None or key not in self.___DATA___:
					raise KeyError(key)
				return self.___DATA___[key]
			data: Optional[str] = "./project/data/module_creator_core"
			module_templates: Optional[str] = "./project/data/module_creator_core/module_templates.yaml"

			@staticmethod
			def from_raw(raw: Dict[str, Any] | None) -> 'Path':
				inst = ConfigKeys.ModuleCreatorCore.Path()
				inst.___DATA___ = raw or {}
				inst._populate(raw or {})
				return inst

			def _populate(self, data: Dict[str, Any]):
				self.___DATA___ = data
				self.data = data.get('data', self.data)
				self.module_templates = data.get('module_templates', self.module_templates)

			def __init__(self):
				pass



	@dataclass
	class CreatorCommonCore:
		___DATA___: Dict[str, Any] | None = None
		def dict_get(self, key: str, default: Any = None) -> Any:
			'Dictionary-style access to raw data. Prefer typed attributes when possible.'
			if self.___DATA___ is None:
				return default
			return self.___DATA___.get(key, default)
		def __getitem__(self, key: str) -> Any:
			if self.___DATA___ is None or key not in self.___DATA___:
				raise KeyError(key)
			return self.___DATA___[key]
		module_name: Optional[str] = "creator_common_core"
		path: Optional['Path'] = None

		@staticmethod
		def from_raw(raw: Dict[str, Any] | None) -> 'CreatorCommonCore':
			inst = ConfigKeys.CreatorCommonCore()
			inst.___DATA___ = raw or {}
			inst._populate(raw or {})
			return inst

		def _populate(self, data: Dict[str, Any]):
			self.___DATA___ = data
			self.module_name = data.get('module_name', self.module_name)
			self.path = self.Path.from_raw(data.get('path', {}))

		def __init__(self):
			pass

		@dataclass
		class Path:
			___DATA___: Dict[str, Any] | None = None
			def dict_get(self, key: str, default: Any = None) -> Any:
				'Dictionary-style access to raw data. Prefer typed attributes when possible.'
				if self.___DATA___ is None:
					return default
				return self.___DATA___.get(key, default)
			def __getitem__(self, key: str) -> Any:
				if self.___DATA___ is None or key not in self.___DATA___:
					raise KeyError(key)
				return self.___DATA___[key]
			data: Optional[str] = "./project/data/creator_common_core"

			@staticmethod
			def from_raw(raw: Dict[str, Any] | None) -> 'Path':
				inst = ConfigKeys.CreatorCommonCore.Path()
				inst.___DATA___ = raw or {}
				inst._populate(raw or {})
				return inst

			def _populate(self, data: Dict[str, Any]):
				self.___DATA___ = data
				self.data = data.get('data', self.data)

			def __init__(self):
				pass



	@dataclass
	class GithubApiCore:
		___DATA___: Dict[str, Any] | None = None
		def dict_get(self, key: str, default: Any = None) -> Any:
			'Dictionary-style access to raw data. Prefer typed attributes when possible.'
			if self.___DATA___ is None:
				return default
			return self.___DATA___.get(key, default)
		def __getitem__(self, key: str) -> Any:
			if self.___DATA___ is None or key not in self.___DATA___:
				raise KeyError(key)
			return self.___DATA___[key]
		module_name: Optional[str] = "github_api_core"
		path: Optional['Path'] = None

		@staticmethod
		def from_raw(raw: Dict[str, Any] | None) -> 'GithubApiCore':
			inst = ConfigKeys.GithubApiCore()
			inst.___DATA___ = raw or {}
			inst._populate(raw or {})
			return inst

		def _populate(self, data: Dict[str, Any]):
			self.___DATA___ = data
			self.module_name = data.get('module_name', self.module_name)
			self.path = self.Path.from_raw(data.get('path', {}))

		def __init__(self):
			pass

		@dataclass
		class Path:
			___DATA___: Dict[str, Any] | None = None
			def dict_get(self, key: str, default: Any = None) -> Any:
				'Dictionary-style access to raw data. Prefer typed attributes when possible.'
				if self.___DATA___ is None:
					return default
				return self.___DATA___.get(key, default)
			def __getitem__(self, key: str) -> Any:
				if self.___DATA___ is None or key not in self.___DATA___:
					raise KeyError(key)
				return self.___DATA___[key]
			data: Optional[str] = "./project/data/github_api_core"

			@staticmethod
			def from_raw(raw: Dict[str, Any] | None) -> 'Path':
				inst = ConfigKeys.GithubApiCore.Path()
				inst.___DATA___ = raw or {}
				inst._populate(raw or {})
				return inst

			def _populate(self, data: Dict[str, Any]):
				self.___DATA___ = data
				self.data = data.get('data', self.data)

			def __init__(self):
				pass



	@dataclass
	class MyModule:
		___DATA___: Dict[str, Any] | None = None
		def dict_get(self, key: str, default: Any = None) -> Any:
			'Dictionary-style access to raw data. Prefer typed attributes when possible.'
			if self.___DATA___ is None:
				return default
			return self.___DATA___.get(key, default)
		def __getitem__(self, key: str) -> Any:
			if self.___DATA___ is None or key not in self.___DATA___:
				raise KeyError(key)
			return self.___DATA___[key]
		module_name: Optional[str] = "my_module"
		path: Optional['Path'] = None

		@staticmethod
		def from_raw(raw: Dict[str, Any] | None) -> 'MyModule':
			inst = ConfigKeys.MyModule()
			inst.___DATA___ = raw or {}
			inst._populate(raw or {})
			return inst

		def _populate(self, data: Dict[str, Any]):
			self.___DATA___ = data
			self.module_name = data.get('module_name', self.module_name)
			self.path = self.Path.from_raw(data.get('path', {}))

		def __init__(self):
			pass

		@dataclass
		class Path:
			___DATA___: Dict[str, Any] | None = None
			def dict_get(self, key: str, default: Any = None) -> Any:
				'Dictionary-style access to raw data. Prefer typed attributes when possible.'
				if self.___DATA___ is None:
					return default
				return self.___DATA___.get(key, default)
			def __getitem__(self, key: str) -> Any:
				if self.___DATA___ is None or key not in self.___DATA___:
					raise KeyError(key)
				return self.___DATA___[key]
			data: Optional[str] = "./project/data/my_module"

			@staticmethod
			def from_raw(raw: Dict[str, Any] | None) -> 'Path':
				inst = ConfigKeys.MyModule.Path()
				inst.___DATA___ = raw or {}
				inst._populate(raw or {})
				return inst

			def _populate(self, data: Dict[str, Any]):
				self.___DATA___ = data
				self.data = data.get('data', self.data)

			def __init__(self):
				pass



	@dataclass
	class QuestionaryCore:
		___DATA___: Dict[str, Any] | None = None
		def dict_get(self, key: str, default: Any = None) -> Any:
			'Dictionary-style access to raw data. Prefer typed attributes when possible.'
			if self.___DATA___ is None:
				return default
			return self.___DATA___.get(key, default)
		def __getitem__(self, key: str) -> Any:
			if self.___DATA___ is None or key not in self.___DATA___:
				raise KeyError(key)
			return self.___DATA___[key]
		module_name: Optional[str] = "questionary_core"
		path: Optional['Path'] = None

		@staticmethod
		def from_raw(raw: Dict[str, Any] | None) -> 'QuestionaryCore':
			inst = ConfigKeys.QuestionaryCore()
			inst.___DATA___ = raw or {}
			inst._populate(raw or {})
			return inst

		def _populate(self, data: Dict[str, Any]):
			self.___DATA___ = data
			self.module_name = data.get('module_name', self.module_name)
			self.path = self.Path.from_raw(data.get('path', {}))

		def __init__(self):
			pass

		@dataclass
		class Path:
			___DATA___: Dict[str, Any] | None = None
			def dict_get(self, key: str, default: Any = None) -> Any:
				'Dictionary-style access to raw data. Prefer typed attributes when possible.'
				if self.___DATA___ is None:
					return default
				return self.___DATA___.get(key, default)
			def __getitem__(self, key: str) -> Any:
				if self.___DATA___ is None or key not in self.___DATA___:
					raise KeyError(key)
				return self.___DATA___[key]
			data: Optional[str] = "./project/data/questionary_core"

			@staticmethod
			def from_raw(raw: Dict[str, Any] | None) -> 'Path':
				inst = ConfigKeys.QuestionaryCore.Path()
				inst.___DATA___ = raw or {}
				inst._populate(raw or {})
				return inst

			def _populate(self, data: Dict[str, Any]):
				self.___DATA___ = data
				self.data = data.get('data', self.data)

			def __init__(self):
				pass



	@dataclass
	class YamlReadingCore:
		___DATA___: Dict[str, Any] | None = None
		def dict_get(self, key: str, default: Any = None) -> Any:
			'Dictionary-style access to raw data. Prefer typed attributes when possible.'
			if self.___DATA___ is None:
				return default
			return self.___DATA___.get(key, default)
		def __getitem__(self, key: str) -> Any:
			if self.___DATA___ is None or key not in self.___DATA___:
				raise KeyError(key)
			return self.___DATA___[key]
		module_name: Optional[str] = "yaml_reading_core"
		path: Optional['Path'] = None

		@staticmethod
		def from_raw(raw: Dict[str, Any] | None) -> 'YamlReadingCore':
			inst = ConfigKeys.YamlReadingCore()
			inst.___DATA___ = raw or {}
			inst._populate(raw or {})
			return inst

		def _populate(self, data: Dict[str, Any]):
			self.___DATA___ = data
			self.module_name = data.get('module_name', self.module_name)
			self.path = self.Path.from_raw(data.get('path', {}))

		def __init__(self):
			pass

		@dataclass
		class Path:
			___DATA___: Dict[str, Any] | None = None
			def dict_get(self, key: str, default: Any = None) -> Any:
				'Dictionary-style access to raw data. Prefer typed attributes when possible.'
				if self.___DATA___ is None:
					return default
				return self.___DATA___.get(key, default)
			def __getitem__(self, key: str) -> Any:
				if self.___DATA___ is None or key not in self.___DATA___:
					raise KeyError(key)
				return self.___DATA___[key]
			data: Optional[str] = "./project/data/yaml_reading_core"

			@staticmethod
			def from_raw(raw: Dict[str, Any] | None) -> 'Path':
				inst = ConfigKeys.YamlReadingCore.Path()
				inst.___DATA___ = raw or {}
				inst._populate(raw or {})
				return inst

			def _populate(self, data: Dict[str, Any]):
				self.___DATA___ = data
				self.data = data.get('data', self.data)

			def __init__(self):
				pass



	@dataclass
	class ProjectInitCore:
		___DATA___: Dict[str, Any] | None = None
		def dict_get(self, key: str, default: Any = None) -> Any:
			'Dictionary-style access to raw data. Prefer typed attributes when possible.'
			if self.___DATA___ is None:
				return default
			return self.___DATA___.get(key, default)
		def __getitem__(self, key: str) -> Any:
			if self.___DATA___ is None or key not in self.___DATA___:
				raise KeyError(key)
			return self.___DATA___[key]
		module_name: Optional[str] = "project_init_core"
		path: Optional['Path'] = None
		framework_repo_url: Optional[str] = "https://github.com/AI-Driven-Highspeed-Development/ai_driven_highspeed_development_framework_bootstrapped"

		@staticmethod
		def from_raw(raw: Dict[str, Any] | None) -> 'ProjectInitCore':
			inst = ConfigKeys.ProjectInitCore()
			inst.___DATA___ = raw or {}
			inst._populate(raw or {})
			return inst

		def _populate(self, data: Dict[str, Any]):
			self.___DATA___ = data
			self.module_name = data.get('module_name', self.module_name)
			self.path = self.Path.from_raw(data.get('path', {}))
			self.framework_repo_url = data.get('framework_repo_url', self.framework_repo_url)

		def __init__(self):
			pass

		@dataclass
		class Path:
			___DATA___: Dict[str, Any] | None = None
			def dict_get(self, key: str, default: Any = None) -> Any:
				'Dictionary-style access to raw data. Prefer typed attributes when possible.'
				if self.___DATA___ is None:
					return default
				return self.___DATA___.get(key, default)
			def __getitem__(self, key: str) -> Any:
				if self.___DATA___ is None or key not in self.___DATA___:
					raise KeyError(key)
				return self.___DATA___[key]
			data: Optional[str] = "./project/data/project_init_core"

			@staticmethod
			def from_raw(raw: Dict[str, Any] | None) -> 'Path':
				inst = ConfigKeys.ProjectInitCore.Path()
				inst.___DATA___ = raw or {}
				inst._populate(raw or {})
				return inst

			def _populate(self, data: Dict[str, Any]):
				self.___DATA___ = data
				self.data = data.get('data', self.data)

			def __init__(self):
				pass



