"""
Example of using El DT (Director Técnico).

This example demonstrates:
- Initializing a project
- Parsing a PRD
- Managing tasks
- Assigning tasks to agents
"""

import asyncio
from typing import Any

from agents_army import DT
from agents_army.core.agent import LLMProvider


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for example."""

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate mock response."""
        if "PRD" in prompt or "parse" in prompt.lower():
            return '''[
  {
    "title": "Implement User Authentication",
    "description": "Create login and registration system",
    "priority": 5,
    "tags": ["backend", "security"]
  },
  {
    "title": "Design User Interface",
    "description": "Create UI mockups and wireframes",
    "priority": 4,
    "tags": ["design", "frontend"]
  },
  {
    "title": "Write API Documentation",
    "description": "Document all API endpoints",
    "priority": 3,
    "tags": ["documentation"]
  }
]'''
        return "Mock response"


async def main():
    """Main example function."""
    print("El DT (Director Técnico) Example\n")

    # 1. Create El DT
    print("1. Creating El DT...")
    dt = DT(
        name="El DT",
        project_path=".taskmaster_example",
        prd_path=".taskmaster_example/docs/prd.txt",
        llm_provider=MockLLMProvider(),
    )
    print(f"   Created: {dt.name} ({dt.role.value})\n")

    # 2. Initialize project
    print("2. Initializing project...")
    project = await dt.initialize_project(
        project_name="Example Project",
        description="A sample project to demonstrate El DT capabilities",
        rules=[
            "Always validate outputs",
            "Follow best practices",
            "Document all changes",
        ],
    )
    print(f"   Project: {project.name}")
    print(f"   Path: {project.path}\n")

    # 3. Create PRD
    print("3. Creating PRD...")
    prd_content = """# Product Requirements Document

## Overview
Build a web application for task management.

## Features
1. User authentication (login, registration)
2. Task creation and management
3. User dashboard
4. API for mobile app

## Technical Requirements
- Python backend
- React frontend
- PostgreSQL database
- RESTful API
"""
    prd_file = dt.prd_path
    prd_file.parent.mkdir(parents=True, exist_ok=True)
    prd_file.write_text(prd_content)
    print(f"   PRD created at: {prd_file}\n")

    # 4. Parse PRD
    print("4. Parsing PRD and generating tasks...")
    tasks = await dt.parse_prd()
    print(f"   Generated {len(tasks)} tasks:")
    for task in tasks:
        print(f"     - {task.title} (Priority: {task.priority})")
    print()

    # 5. Get next task
    print("5. Getting next task to work on...")
    next_task = await dt.get_next_task()
    if next_task:
        print(f"   Next task: {next_task.title}")
        print(f"   Priority: {next_task.priority}")
        print(f"   Status: {next_task.status}\n")

    # 6. List all tasks
    print("6. Listing all tasks...")
    all_tasks = await dt.get_tasks()
    print(f"   Total tasks: {len(all_tasks)}")
    for task in all_tasks:
        print(f"     - {task.title}: {task.status}")
    print()

    # 7. Update task status
    if tasks:
        print("7. Updating task status...")
        first_task = tasks[0]
        updated = await dt.update_task_status(first_task.id, "done")
        print(f"   Updated: {updated.title} -> {updated.status}\n")

    print("Example completed successfully!")
    print("\nNote: Clean up .taskmaster_example directory if needed")


if __name__ == "__main__":
    asyncio.run(main())
