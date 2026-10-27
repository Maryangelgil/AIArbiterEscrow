# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json
import typing

class AIArbiterEscrow(gl.Contract):
    # Variables de estado primitivas y estructuradas compatibles
    projects_json: str  # Almacena el JSON string de todos los proyectos
    deliverables_json: str  # Almacena el JSON string de las entregas
    audit_reports_json: str  # Almacena el JSON string de los reportes
    project_states_json: str  # Almacena el JSON string de los estados

    def __init__(self):
        """
        Inicializa el contrato de Escrow con arbitraje de IA descentralizado.
        """
        self.projects_json = "{}"
        self.deliverables_json = "{}"
        self.audit_reports_json = "{}"
        self.project_states_json = "{}"

    @gl.public.write
    def create_project(self, project_id: str, client_name: str, detailed_specs: str, bounty_amount: int) -> str:
        projects = json.loads(self.projects_json)
        project_states = json.loads(self.project_states_json)

        if project_id in projects:
            raise gl.vm.UserError(f"Error: Project ID {project_id} already exists.")

        projects[project_id] = {
            "client": str(gl.message.sender),
            "client_name": client_name,
            "specs": detailed_specs,
            "bounty": bounty_amount,
            "created_at_block": int(gl.env.block_number)
        }
        
        project_states[project_id] = "CREATED"

        # Guardar de vuelta al estado del contrato
        self.projects_json = json.dumps(projects)
        self.project_states_json = json.dumps(project_states)

        return f"Project {project_id} successfully created and locked in escrow."

    @gl.public.write
    def submit_work(self, project_id: str, contributor_address: str, work_url: str, summary: str) -> str:
        projects = json.loads(self.projects_json)
        deliverables = json.loads(self.deliverables_json)
        project_states = json.loads(self.project_states_json)

        if project_id not in projects:
            raise gl.vm.UserError("Error: Project does not exist.")
        
        current_state = project_states.get(project_id)
        if current_state not in ["CREATED", "DISPUTED"]:
            raise gl.vm.UserError(f"Error: Cannot submit work while project state is {current_state}.")

        deliverables[project_id] = {
            "contributor": contributor_address,
            "url": work_url,
            "summary": summary,
            "submitted_at": int(gl.env.block_number)
        }
        
        project_states[project_id] = "SUBMITTED"

        self.deliverables_json = json.dumps(deliverables)
        self.project_states_json = json.dumps(project_states)

        return f"Deliverable for project {project_id} submitted for AI validator audit."

    @gl.public.write
    def execute_validator_audit(self, project_id: str) -> typing.Any:
        projects = json.loads(self.projects_json)
        deliverables = json.loads(self.deliverables_json)
        audit_reports = json.loads(self.audit_reports_json)
        project_states = json.loads(self.project_states_json)

        if project_id not in projects or project_id not in deliverables:
            raise gl.vm.UserError("Error: Project or deliverable not found.")

        project = projects[project_id]
        deliverable = deliverables[project_id]

        project_states[project_id] = "UNDER_REVIEW"
        self.project_states_json = json.dumps(project_states)

        def run_consensus_evaluation() -> typing.Any:
            prompt = f"""
            You are the Chief AI Auditor and Technical Arbiter for a decentralized escrow network.
            Your task is to rigorously evaluate whether the delivered work fulfills the original project specifications.
            
            --- ORIGINAL PROJECT SPECIFICATIONS ---
            "{project['specs']}"
            
            --- SUBMITTED WORK DETAILS ---
            Deliverable URL: "{deliverable['url']}"
            Contributor Summary: "{deliverable['summary']}"
            
            Instructions for Validators:
            1. Scrutinize the technical scope, requirements, and quality based on the provided proof/URL.
            2. Evaluate compliance on a scale from 0 to 100.
            3. Provide a strict JSON response with exact keys. Do not include markdown formatting blocks like ```json, output raw JSON only:
            {{
                "status": "PASSED" or "FAILED",
                "score": <integer 0-100>,
                "code_quality_assessment": "<short technical review>",
                "requirements_met": true or false,
                "justification": "<detailed reasoning for the decision>"
            }}
            """
            
            raw_ai_response = gl.nondet.exec_prompt(prompt)
            cleaned_json = raw_ai_response.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned_json)

        # Consenso estricto entre validadores usando el principio de equivalencia
        audit_data = gl.eq_principle.strict_eq(run_consensus_evaluation)

        audit_reports[project_id] = {
            "audit_data": audit_data,
            "audited_at_block": int(gl.env.block_number)
        }

        is_passed = audit_data.get("requirements_met", False)
        score = audit_data.get("score", 0)

        if is_passed and score >= 75:
            project_states[project_id] = "APPROVED"
        else:
            project_states[project_id] = "DISPUTED"

        self.audit_reports_json = json.dumps(audit_reports)
        self.project_states_json = json.dumps(project_states)

        return audit_data

    @gl.public.view
    def get_project_dossier(self, project_id: str) -> dict[str, typing.Any]:
        projects = json.loads(self.projects_json)
        deliverables = json.loads(self.deliverables_json)
        audit_reports = json.loads(self.audit_reports_json)
        project_states = json.loads(self.project_states_json)

        if project_id not in projects:
            return {"error": "Project not found"}

        return {
            "state": project_states.get(project_id, "UNKNOWN"),
            "project_details": projects[project_id],
            "deliverable_details": deliverables.get(project_id, {}),
            "audit_report": audit_reports.get(project_id, {})
        }# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json
import typing

class AIArbiterEscrow(gl.Contract):
    # Variables de estado primitivas y estructuradas compatibles
    projects_json: str  # Almacena el JSON string de todos los proyectos
    deliverables_json: str  # Almacena el JSON string de las entregas
    audit_reports_json: str  # Almacena el JSON string de los reportes
    project_states_json: str  # Almacena el JSON string de los estados

    def __init__(self):
        """
        Inicializa el contrato de Escrow con arbitraje de IA descentralizado.
        """
        self.projects_json = "{}"
        self.deliverables_json = "{}"
        self.audit_reports_json = "{}"
        self.project_states_json = "{}"

    @gl.public.write
    def create_project(self, project_id: str, client_name: str, detailed_specs: str, bounty_amount: int) -> str:
        projects = json.loads(self.projects_json)
        project_states = json.loads(self.project_states_json)

        if project_id in projects:
            raise gl.vm.UserError(f"Error: Project ID {project_id} already exists.")

        projects[project_id] = {
            "client": str(gl.message.sender),
            "client_name": client_name,
            "specs": detailed_specs,
            "bounty": bounty_amount,
            "created_at_block": int(gl.env.block_number)
        }
        
        project_states[project_id] = "CREATED"

        # Guardar de vuelta al estado del contrato
        self.projects_json = json.dumps(projects)
        self.project_states_json = json.dumps(project_states)

        return f"Project {project_id} successfully created and locked in escrow."

    @gl.public.write
    def submit_work(self, project_id: str, contributor_address: str, work_url: str, summary: str) -> str:
        projects = json.loads(self.projects_json)
        deliverables = json.loads(self.deliverables_json)
        project_states = json.loads(self.project_states_json)

        if project_id not in projects:
            raise gl.vm.UserError("Error: Project does not exist.")
        
        current_state = project_states.get(project_id)
        if current_state not in ["CREATED", "DISPUTED"]:
            raise gl.vm.UserError(f"Error: Cannot submit work while project state is {current_state}.")

        deliverables[project_id] = {
            "contributor": contributor_address,
            "url": work_url,
            "summary": summary,
            "submitted_at": int(gl.env.block_number)
        }
        
        project_states[project_id] = "SUBMITTED"

        self.deliverables_json = json.dumps(deliverables)
        self.project_states_json = json.dumps(project_states)

        return f"Deliverable for project {project_id} submitted for AI validator audit."

    @gl.public.write
    def execute_validator_audit(self, project_id: str) -> typing.Any:
        projects = json.loads(self.projects_json)
        deliverables = json.loads(self.deliverables_json)
        audit_reports = json.loads(self.audit_reports_json)
        project_states = json.loads(self.project_states_json)

        if project_id not in projects or project_id not in deliverables:
            raise gl.vm.UserError("Error: Project or deliverable not found.")

        project = projects[project_id]
        deliverable = deliverables[project_id]

        project_states[project_id] = "UNDER_REVIEW"
        self.project_states_json = json.dumps(project_states)

        def run_consensus_evaluation() -> typing.Any:
            prompt = f"""
            You are the Chief AI Auditor and Technical Arbiter for a decentralized escrow network.
            Your task is to rigorously evaluate whether the delivered work fulfills the original project specifications.
            
            --- ORIGINAL PROJECT SPECIFICATIONS ---
            "{project['specs']}"
            
            --- SUBMITTED WORK DETAILS ---
            Deliverable URL: "{deliverable['url']}"
            Contributor Summary: "{deliverable['summary']}"
            
            Instructions for Validators:
            1. Scrutinize the technical scope, requirements, and quality based on the provided proof/URL.
            2. Evaluate compliance on a scale from 0 to 100.
            3. Provide a strict JSON response with exact keys. Do not include markdown formatting blocks like ```json, output raw JSON only:
            {{
                "status": "PASSED" or "FAILED",
                "score": <integer 0-100>,
                "code_quality_assessment": "<short technical review>",
                "requirements_met": true or false,
                "justification": "<detailed reasoning for the decision>"
            }}
            """
            
            raw_ai_response = gl.nondet.exec_prompt(prompt)
            cleaned_json = raw_ai_response.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned_json)

        # Consenso estricto entre validadores usando el principio de equivalencia
        audit_data = gl.eq_principle.strict_eq(run_consensus_evaluation)

        audit_reports[project_id] = {
            "audit_data": audit_data,
            "audited_at_block": int(gl.env.block_number)
        }

        is_passed = audit_data.get("requirements_met", False)
        score = audit_data.get("score", 0)

        if is_passed and score >= 75:
            project_states[project_id] = "APPROVED"
        else:
            project_states[project_id] = "DISPUTED"

        self.audit_reports_json = json.dumps(audit_reports)
        self.project_states_json = json.dumps(project_states)

        return audit_data

    @gl.public.view
    def get_project_dossier(self, project_id: str) -> dict[str, typing.Any]:
        projects = json.loads(self.projects_json)
        deliverables = json.loads(self.deliverables_json)
        audit_reports = json.loads(self.audit_reports_json)
        project_states = json.loads(self.project_states_json)

        if project_id not in projects:
            return {"error": "Project not found"}

        return {
            "state": project_states.get(project_id, "UNKNOWN"),
            "project_details": projects[project_id],
            "deliverable_details": deliverables.get(project_id, {}),
            "audit_report": audit_reports.get(project_id, {})
        }
