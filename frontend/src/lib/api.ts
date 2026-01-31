/**
 * API client for communicating with the backend
 */
import axios from 'axios';

export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Types
export interface Repository {
    id: number;
    url: string;
    owner: string;
    name: string;
    branch: string;
    created_at: string;
}

export interface Issue {
    id: number;
    file_path: string;
    line_number?: number;
    issue_type: string;
    severity: string;
    description: string;
    original_code?: string;
    fixed_code?: string;
    explanation?: string;
    is_fixed: boolean;
    created_at: string;
}

export interface Audit {
    id: number;
    repository_id: number;
    status: string;
    task_id: string;
    total_files: number;
    processed_files: number;
    issues_found: number;
    fixes_applied: number;
    pr_url?: string;
    pr_number?: number;
    error_message?: string;
    created_at: string;
    started_at?: string;
    completed_at?: string;
    logs?: any[];
}

export interface AuditDetail extends Audit {
    repository: Repository;
    issues: Issue[];
}

export interface Statistics {
    total_audits: number;
    completed_audits: number;
    failed_audits: number;
    pending_audits: number;
    total_issues_found: number;
    total_fixes_applied: number;
    total_prs_created: number;
}

// API Functions
export const auditAPI = {
    // Create a new audit
    createAudit: async (url: string, branch: string = 'main', github_token?: string, gemini_api_key?: string) => {
        const payload: any = { url, branch };
        if (github_token) payload.github_token = github_token;
        if (gemini_api_key) payload.gemini_api_key = gemini_api_key;

        const response = await api.post('/api/audits/', payload);
        return response.data;
    },

    // Get all audits
    getAudits: async () => {
        const response = await api.get<Audit[]>('/api/audits/');
        return response.data;
    },

    // Get audit by ID
    getAudit: async (id: number) => {
        const response = await api.get<AuditDetail>(`/api/audits/${id}`);
        return response.data;
    },

    // Delete audit
    deleteAudit: async (id: number) => {
        await api.delete(`/api/audits/${id}`);
    },

    // Get statistics
    getStatistics: async () => {
        const response = await api.get<Statistics>('/api/stats/');
        return response.data;
    },
};

// Standalone exports for easier imports
export const createAudit = auditAPI.createAudit;
export const getAudits = auditAPI.getAudits;
export const getAudit = auditAPI.getAudit;
export const deleteAudit = auditAPI.deleteAudit;
export const getStatistics = auditAPI.getStatistics;
