import yaml
import shlex
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


class ConfigLoader:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.config = {}

    def load(self):
        if not self.file_path.exists():
            raise FileNotFoundError(f"Config file '{self.file_path}' not found.")

        try:
            with self.file_path.open('r') as file:
                self.config = yaml.safe_load(file) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse YAML: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default)


class DockerfileRenderer:
    def __init__(self, template_dir="templates", template_file="Dockerfile.j2"):
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(disabled_extensions=("j2",)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self.env.filters['to_cmd_list'] = self.to_cmd_list
        self.template = self.env.get_template(template_file)

    @staticmethod
    def to_cmd_list(command_str):
    # Converts "rails server" into '"rails", "server"' for valid CMD JSON array
        return ', '.join(f'"{arg}"' for arg in shlex.split(command_str))

    def render(self, context: dict, output_path="Dockerfile"):
        rendered = self.template.render(context)
        Path(output_path).write_text(rendered.strip() + "\n")
        print(f"Dockerfile created at: {output_path}")


if __name__ == "__main__":
    config = ConfigLoader("project.yaml")
    config.load()

    renderer = DockerfileRenderer()
    renderer.render({
        "name": config.get("name"),
        "startup_command": config.get("startup_command"),
        "maintainer": config.get("maintainer", "Your teammate")
    })