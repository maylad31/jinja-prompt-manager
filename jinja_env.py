from jinja2.sandbox import SandboxedEnvironment


def get_environment() -> SandboxedEnvironment:
    def require(value, name):
        if not value:
            raise Exception(f"Variable {name} is required")
        return value

    env = SandboxedEnvironment(trim_blocks=True, lstrip_blocks=True)
    env.filters["require"] = require
    return env
