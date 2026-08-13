# Copyright (c) 2025, NVIDIA CORPORATION.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
from pathlib import Path

import yaml


def test_result_step_defines_skipping_env_and_uses_it():
    """The Result step must define SKIPPING_IS_ALLOWED in its env: block and
    reference it in its run script. Without the env definition the variable is
    always empty and the skip logic is dead code.
    """
    workflow_path = Path(__file__).parent / ".github" / "workflows" / "copyright-check.yml"
    assert workflow_path.exists(), f"Workflow file not found: {workflow_path}"

    workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))

    summary_job = workflow["jobs"]["copyright-check-summary"]
    result_step = next(
        (step for step in summary_job["steps"] if step.get("name") == "Result"),
        None,
    )
    assert result_step is not None, "Result step not found"

    assert "env" in result_step, "Result step is missing an env: block"
    assert "SKIPPING_IS_ALLOWED" in result_step["env"], "SKIPPING_IS_ALLOWED is not defined in the Result step env: block"
    expr = result_step["env"]["SKIPPING_IS_ALLOWED"].strip()
    assert expr, "SKIPPING_IS_ALLOWED env value is empty"
    assert "docs_only" in expr and "is_deployment_workflow" in expr, "SKIPPING_IS_ALLOWED expression does not reference the expected pre-flight outputs"

