
class SkillRegistry:
    """
    Central registry for registering and executing agent skills.
    """

    def __init__(self):
        self.skills = {}

    def register_skill(self, name, skill_function):
        """Register a skill using a unique name."""

        if not name:
            raise ValueError("Skill name is required")

        if not callable(skill_function):
            raise TypeError("Skill must be a callable function")

        if name in self.skills:
            raise ValueError(f"Skill '{name}' is already registered")

        self.skills[name] = skill_function

        return {
            "status": "success",
            "message": f"Skill '{name}' registered successfully"
        }

    def get_skill(self, name):
        """Retrieve a registered skill."""

        if name not in self.skills:
            raise KeyError(f"Skill '{name}' not found")

        return self.skills[name]

    def execute_skill(self, name, **kwargs):
        """Execute a registered skill."""

        skill = self.get_skill(name)

        return skill(**kwargs)

    def list_skills(self):
        """Return all registered skill names."""

        return list(self.skills.keys())


# Register existing project skills
skill_registry = SkillRegistry()

from app.skills.risk_analysis_skill import risk_analysis_skill

skill_registry.register_skill(
    "risk_analysis",
    risk_analysis_skill
)
