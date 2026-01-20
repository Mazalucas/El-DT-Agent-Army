"""
Example: Using Planning Agents for Project Creation

This example demonstrates how to use the planning agents (PRD Creator, SRD Creator,
and Development Planner) to create comprehensive project plans, and how the DT
can execute these plans by assigning tasks to appropriate agents.
"""

import asyncio
from agents_army import (
    AgentSystem,
    DT,
    PRDCreator,
    SRDCreator,
    DevelopmentPlanner,
    BackendArchitect,
    FrontendDeveloper,
    DevOpsAutomator,
    QATester,
)


async def main():
    """Main example function."""
    print("=" * 80)
    print("Planning Agents Example: Creating a Project Plan")
    print("=" * 80)
    print()

    # Initialize the agent system
    system = AgentSystem()

    # Create planning agents
    print("1. Creating planning agents...")
    prd_creator = PRDCreator(name="PRD Creator")
    srd_creator = SRDCreator(name="SRD Creator")
    development_planner = DevelopmentPlanner(name="Development Planner")

    # Create DT
    dt = DT(name="El DT", project_path=".dt_example")

    # Register planning agents in the system
    system.register_agent(prd_creator)
    system.register_agent(srd_creator)
    system.register_agent(development_planner)
    system.register_agent(dt)

    # Register execution agents (for when DT assigns tasks)
    backend_architect = BackendArchitect(name="Backend Architect")
    frontend_developer = FrontendDeveloper(name="Frontend Developer")
    devops_automator = DevOpsAutomator(name="DevOps Automator")
    qa_tester = QATester(name="QA Tester")

    system.register_agent(backend_architect)
    system.register_agent(frontend_developer)
    system.register_agent(devops_automator)
    system.register_agent(qa_tester)

    # Set system reference in DT (needed for planning agent access)
    dt.system = system

    print("✓ All agents registered")
    print()

    # Step 1: Create PRD
    print("2. Creating Product Requirements Document (PRD)...")
    print("-" * 80)
    
    product_idea = """
    A task management application for small teams that allows:
    - Creating and organizing tasks in projects
    - Assigning tasks to team members
    - Tracking progress with kanban boards
    - Real-time collaboration
    - Mobile app for iOS and Android
    """
    
    business_objectives = [
        "Increase team productivity by 30%",
        "Reduce project management overhead",
        "Launch MVP within 3 months",
        "Acquire 1000 users in first 6 months"
    ]
    
    target_users = [
        "Small team managers (5-20 people)",
        "Project coordinators",
        "Team members who need task visibility"
    ]
    
    constraints = {
        "budget": "Limited - bootstrap startup",
        "timeline": "3 months for MVP",
        "team_size": "3 developers + 1 designer"
    }

    prd = await dt.create_prd(
        product_idea=product_idea,
        business_objectives=business_objectives,
        target_users=target_users,
        constraints=constraints,
    )
    
    print(f"✓ PRD created (Version: {prd['metadata']['version']})")
    print(f"  Sections: {len(prd['sections'])}")
    print(f"  Preview: {prd['prd_content'][:200]}...")
    print()

    # Step 2: Create SRD
    print("3. Creating Software Requirements Document (SRD)...")
    print("-" * 80)
    
    technical_context = {
        "current_stack": "Python, React, PostgreSQL",
        "infrastructure": "Cloud-based (AWS/GCP)",
        "team_expertise": "Full-stack developers"
    }
    
    existing_systems = [
        "Authentication service (Auth0)",
        "Payment processing (Stripe)"
    ]
    
    technical_constraints = {
        "must_use": "React for frontend, Python for backend",
        "cannot_use": "No proprietary databases",
        "scalability": "Must support 10,000 concurrent users"
    }

    srd = await dt.create_srd(
        prd=prd,
        technical_context=technical_context,
        existing_systems=existing_systems,
        technical_constraints=technical_constraints,
    )
    
    print(f"✓ SRD created (Version: {srd['metadata']['version']})")
    print(f"  Sections: {len(srd['sections'])}")
    print(f"  Preview: {srd['srd_content'][:200]}...")
    print()

    # Step 3: Create Development Plan
    print("4. Creating Development Plan...")
    print("-" * 80)
    
    plan_constraints = {
        "timeline": "3 months",
        "team_size": "4 people",
        "budget": "$50,000",
        "mvp_deadline": "End of month 3"
    }
    
    preferences = {
        "methodology": "Agile/Scrum",
        "sprints": "2-week sprints",
        "deployment": "Continuous deployment"
    }

    development_plan = await dt.create_development_plan(
        prd=prd,
        srd=srd,
        constraints=plan_constraints,
        preferences=preferences,
    )
    
    print(f"✓ Development Plan created (Version: {development_plan['metadata']['version']})")
    print(f"  Sections: {len(development_plan['sections'])}")
    print(f"  Preview: {development_plan['plan_content'][:200]}...")
    print()

    # Step 4: Extract tasks from plan
    print("5. Extracting tasks from development plan...")
    print("-" * 80)
    
    tasks = await dt.extract_tasks_from_plan(development_plan)
    
    print(f"✓ Extracted {len(tasks)} tasks")
    print()
    print("Sample tasks:")
    for i, task in enumerate(tasks[:5], 1):
        print(f"  {i}. {task.title}")
        print(f"     Phase: {task.metadata.get('phase', 'Unknown')}")
        print(f"     Priority: {task.priority}")
        print()
    print()

    # Step 5: Map tasks to agents and assign
    print("6. Mapping tasks to agents and assigning...")
    print("-" * 80)
    
    assignments = await dt.execute_plan(development_plan, auto_assign=True)
    
    print(f"✓ Assigned {len(assignments)} tasks to agents")
    print()
    print("Task assignments:")
    for assignment in assignments[:5]:
        task = dt.task_storage.load_task(assignment.task_id)
        if task:
            print(f"  - Task: {task.title[:50]}...")
            print(f"    Assigned to: {assignment.agent_role.value}")
            print()
    print()

    # Step 6: Show task status
    print("7. Current task status...")
    print("-" * 80)
    
    all_tasks = await dt.get_tasks(limit=100)
    pending = [t for t in all_tasks if t.status == "pending"]
    in_progress = [t for t in all_tasks if t.status == "in-progress"]
    
    print(f"Total tasks: {len(all_tasks)}")
    print(f"Pending: {len(pending)}")
    print(f"In Progress: {len(in_progress)}")
    print()

    print("=" * 80)
    print("Example completed successfully!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Review the generated PRD, SRD, and Development Plan")
    print("2. Refine plans if needed using the refine methods")
    print("3. Start executing tasks by having agents work on assigned tasks")
    print("4. Monitor progress through the DT's task management system")


if __name__ == "__main__":
    asyncio.run(main())
