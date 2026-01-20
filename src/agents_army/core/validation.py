"""Validation runner for tests, linters, and builds."""

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class TestResults:
    """Results from test execution."""

    passed: bool
    output: str
    coverage: Optional[float] = None

    def __str__(self) -> str:
        """String representation."""
        status = "PASSED" if self.passed else "FAILED"
        coverage_str = f" (coverage: {self.coverage:.1%})" if self.coverage else ""
        return f"Tests {status}{coverage_str}"


@dataclass
class LinterResults:
    """Results from linter execution."""

    passed: bool
    output: str
    errors: List[str] = None

    def __init__(self, passed: bool, output: str, errors: Optional[List[str]] = None):
        """Initialize linter results."""
        self.passed = passed
        self.output = output
        self.errors = errors or []

    def __str__(self) -> str:
        """String representation."""
        status = "PASSED" if self.passed else "FAILED"
        errors_str = f" ({len(self.errors)} errors)" if self.errors else ""
        return f"Linter {status}{errors_str}"


@dataclass
class BuildResults:
    """Results from build execution."""

    succeeded: bool
    output: str
    artifacts: List[str] = None

    def __init__(
        self, succeeded: bool, output: str, artifacts: Optional[List[str]] = None
    ):
        """Initialize build results."""
        self.succeeded = succeeded
        self.output = output
        self.artifacts = artifacts or []

    def __str__(self) -> str:
        """String representation."""
        status = "SUCCEEDED" if self.succeeded else "FAILED"
        artifacts_str = f" ({len(self.artifacts)} artifacts)" if self.artifacts else ""
        return f"Build {status}{artifacts_str}"


class ValidationRunner:
    """Runs validation checks (tests, linters, builds)."""

    def __init__(self, project_path: str, config_path: Optional[str] = None):
        """
        Initialize validation runner.

        Args:
            project_path: Path to project root
            config_path: Optional path to validation config file
        """
        self.project_path = Path(project_path)
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: Optional[str]) -> dict:
        """
        Load validation configuration.

        Args:
            config_path: Path to config file

        Returns:
            Configuration dictionary
        """
        default_config = {
            "test_command": "pytest",
            "test_args": ["-v"],
            "linter_command": "flake8",
            "linter_args": ["--max-line-length=100"],
            "build_command": None,  # No default build command
            "build_args": [],
        }

        if config_path:
            config_file = Path(config_path)
            if config_file.exists():
                try:
                    with open(config_file, "r", encoding="utf-8") as f:
                        user_config = json.load(f)
                        default_config.update(user_config)
                except Exception:
                    pass  # Use defaults if config file invalid

        return default_config

    def run_tests(self, project_path: Optional[str] = None) -> TestResults:
        """
        Run tests for the project.

        Args:
            project_path: Optional project path (uses instance path if None)

        Returns:
            TestResults
        """
        path = Path(project_path) if project_path else self.project_path
        command = self.config.get("test_command", "pytest")
        args = self.config.get("test_args", ["-v"])

        try:
            # Run test command
            result = subprocess.run(
                [command] + args,
                cwd=str(path),
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )

            passed = result.returncode == 0
            output = result.stdout + result.stderr

            # Try to extract coverage if pytest-cov is used
            coverage = None
            if "coverage" in output.lower():
                # Try to parse coverage percentage
                import re

                coverage_match = re.search(r"(\d+\.?\d*)%", output)
                if coverage_match:
                    try:
                        coverage = float(coverage_match.group(1)) / 100.0
                    except ValueError:
                        pass

            return TestResults(passed=passed, output=output, coverage=coverage)

        except subprocess.TimeoutExpired:
            return TestResults(
                passed=False, output="Test execution timed out after 5 minutes"
            )
        except FileNotFoundError:
            # Command not found, assume tests pass (optional validation)
            return TestResults(passed=True, output="Test command not found, skipping")
        except Exception as e:
            return TestResults(passed=False, output=f"Error running tests: {str(e)}")

    def run_linter(self, project_path: Optional[str] = None) -> LinterResults:
        """
        Run linter for the project.

        Args:
            project_path: Optional project path (uses instance path if None)

        Returns:
            LinterResults
        """
        path = Path(project_path) if project_path else self.project_path
        command = self.config.get("linter_command", "flake8")
        args = self.config.get("linter_args", [])

        try:
            # Run linter command
            result = subprocess.run(
                [command] + args + [str(path)],
                cwd=str(path),
                capture_output=True,
                text=True,
                timeout=60,  # 1 minute timeout
            )

            passed = result.returncode == 0
            output = result.stdout + result.stderr

            # Extract errors from output
            errors = []
            if not passed and output:
                # Parse linter errors (format varies by linter)
                for line in output.split("\n"):
                    if line.strip() and ":" in line:
                        errors.append(line.strip())

            return LinterResults(passed=passed, output=output, errors=errors)

        except subprocess.TimeoutExpired:
            return LinterResults(
                passed=False, output="Linter execution timed out", errors=[]
            )
        except FileNotFoundError:
            # Command not found, assume linter passes (optional validation)
            return LinterResults(
                passed=True, output="Linter command not found, skipping", errors=[]
            )
        except Exception as e:
            return LinterResults(
                passed=False, output=f"Error running linter: {str(e)}", errors=[]
            )

    def run_build(self, project_path: Optional[str] = None) -> BuildResults:
        """
        Run build for the project.

        Args:
            project_path: Optional project path (uses instance path if None)

        Returns:
            BuildResults
        """
        path = Path(project_path) if project_path else self.project_path
        command = self.config.get("build_command")

        if not command:
            # No build command configured, assume build succeeds
            return BuildResults(
                succeeded=True, output="No build command configured, skipping"
            )

        args = self.config.get("build_args", [])

        try:
            # Run build command
            result = subprocess.run(
                [command] + args,
                cwd=str(path),
                capture_output=True,
                text=True,
                timeout=600,  # 10 minute timeout
            )

            succeeded = result.returncode == 0
            output = result.stdout + result.stderr

            # Try to detect build artifacts
            artifacts = []
            if succeeded:
                # Look for common build output directories
                for artifact_dir in ["dist", "build", "target", "out"]:
                    artifact_path = path / artifact_dir
                    if artifact_path.exists():
                        artifacts.append(str(artifact_path))

            return BuildResults(succeeded=succeeded, output=output, artifacts=artifacts)

        except subprocess.TimeoutExpired:
            return BuildResults(
                succeeded=False, output="Build execution timed out after 10 minutes"
            )
        except FileNotFoundError:
            # Command not found, assume build succeeds (optional validation)
            return BuildResults(
                succeeded=True, output="Build command not found, skipping"
            )
        except Exception as e:
            return BuildResults(
                succeeded=False, output=f"Error running build: {str(e)}"
            )
