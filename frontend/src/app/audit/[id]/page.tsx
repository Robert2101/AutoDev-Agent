'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { ArrowLeft, GitBranch, FileCode, AlertTriangle, CheckCircle, Code2, ExternalLink } from 'lucide-react';
import Link from 'next/link';
import { auditAPI, AuditDetail } from '@/lib/api';
import { formatRelativeTime, getStatusColor, formatStatus, getSeverityColor } from '@/lib/utils';

export default function AuditDetailPage({ params }: { params: { id: string } }) {
    const router = useRouter();
    const [audit, setAudit] = useState<AuditDetail | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchAudit = async () => {
            try {
                const data = await auditAPI.getAudit(parseInt(params.id));
                setAudit(data);
            } catch (err) {
                console.error('Failed to fetch audit:', err);
                setError('Failed to load audit details');
            } finally {
                setLoading(false);
            }
        };

        fetchAudit();

        // Auto-refresh every 5 seconds if audit is in progress
        const interval = setInterval(() => {
            if (audit && !['completed', 'failed'].includes(audit.status)) {
                fetchAudit();
            }
        }, 5000);

        return () => clearInterval(interval);
    }, [params.id, audit?.status]);

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="spinner" />
                <span className="ml-3 text-dark-400">Loading audit details...</span>
            </div>
        );
    }

    if (error || !audit) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <p className="text-red-400 mb-4">{error || 'Audit not found'}</p>
                    <Link href="/" className="text-primary-400 hover:text-primary-300">
                        ← Back to Dashboard
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <div className="mb-8">
                    <Link
                        href="/"
                        className="inline-flex items-center gap-2 text-dark-400 hover:text-dark-300 transition-colors mb-4"
                    >
                        <ArrowLeft className="w-4 h-4" />
                        <span>Back to Dashboard</span>
                    </Link>

                    <div className="glass-card rounded-2xl p-6">
                        <div className="flex items-start justify-between mb-4">
                            <div>
                                <div className="flex items-center gap-3 mb-2">
                                    <h1 className="text-2xl font-bold text-dark-50">
                                        {audit.repository.owner}/{audit.repository.name}
                                    </h1>
                                    <span className={`status-badge ${getStatusColor(audit.status)} border`}>
                                        {formatStatus(audit.status)}
                                    </span>
                                </div>
                                <div className="flex items-center gap-4 text-sm text-dark-400">
                                    <span className="flex items-center gap-1">
                                        <GitBranch className="w-4 h-4" />
                                        {audit.repository.branch}
                                    </span>
                                    <span>Audit #{audit.id}</span>
                                    <span>Created {formatRelativeTime(audit.created_at)}</span>
                                </div>
                            </div>

                            {audit.pr_url && (
                                <a
                                    href={audit.pr_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="btn-gradient flex items-center gap-2"
                                >
                                    <span>View Pull Request</span>
                                    <ExternalLink className="w-4 h-4" />
                                </a>
                            )}
                        </div>

                        {/* Stats Grid */}
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            <div className="p-4 bg-dark-800/30 rounded-lg">
                                <div className="text-2xl font-bold text-dark-50">{audit.total_files}</div>
                                <div className="text-xs text-dark-500 uppercase">Total Files</div>
                            </div>
                            <div className="p-4 bg-dark-800/30 rounded-lg">
                                <div className="text-2xl font-bold text-yellow-400">{audit.issues_found}</div>
                                <div className="text-xs text-dark-500 uppercase">Issues Found</div>
                            </div>
                            <div className="p-4 bg-dark-800/30 rounded-lg">
                                <div className="text-2xl font-bold text-green-400">{audit.fixes_applied}</div>
                                <div className="text-xs text-dark-500 uppercase">Fixes Applied</div>
                            </div>
                            <div className="p-4 bg-dark-800/30 rounded-lg">
                                <div className="text-2xl font-bold text-primary-400">
                                    {audit.pr_number ? `#${audit.pr_number}` : '-'}
                                </div>
                                <div className="text-xs text-dark-500 uppercase">PR Number</div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Issues List */}
                <div className="glass-card rounded-2xl p-6">
                    <h2 className="text-xl font-bold text-dark-50 mb-6 flex items-center gap-2">
                        <Code2 className="w-5 h-5 text-primary-400" />
                        Detected Issues ({audit.issues.length})
                    </h2>

                    {audit.issues.length === 0 ? (
                        <div className="text-center py-12">
                            <CheckCircle className="w-12 h-12 text-green-400 mx-auto mb-4" />
                            <p className="text-dark-400">No issues found in this repository!</p>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            {audit.issues.map((issue, index) => (
                                <div
                                    key={issue.id}
                                    className="p-5 bg-dark-800/50 rounded-xl border border-dark-700/50"
                                    style={{ animationDelay: `${index * 50}ms` }}
                                >
                                    {/* Issue Header */}
                                    <div className="flex items-start justify-between mb-3">
                                        <div className="flex-1">
                                            <div className="flex items-center gap-2 mb-2">
                                                <AlertTriangle className={`w-4 h-4 ${getSeverityColor(issue.severity)}`} />
                                                <span className={`text-sm font-semibold ${getSeverityColor(issue.severity)} uppercase`}>
                                                    {issue.severity}
                                                </span>
                                                <span className="text-sm text-dark-500">•</span>
                                                <span className="text-sm text-dark-400">
                                                    {issue.issue_type.replace(/_/g, ' ')}
                                                </span>
                                            </div>
                                            <h3 className="text-base font-medium text-dark-200">
                                                {issue.description}
                                            </h3>
                                            <p className="text-sm text-dark-500 mt-1">
                                                <FileCode className="w-3 h-3 inline mr-1" />
                                                {issue.file_path}
                                                {issue.line_number && ` : Line ${issue.line_number}`}
                                            </p>
                                        </div>

                                        {issue.is_fixed && (
                                            <div className="flex items-center gap-1 px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-xs font-semibold">
                                                <CheckCircle className="w-3 h-3" />
                                                <span>Fixed</span>
                                            </div>
                                        )}
                                    </div>

                                    {/* Explanation */}
                                    {issue.explanation && (
                                        <div className="mb-3 p-3 bg-dark-900/50 rounded-lg">
                                            <p className="text-sm text-dark-300">{issue.explanation}</p>
                                        </div>
                                    )}

                                    {/* Code Comparison */}
                                    {issue.original_code && issue.fixed_code && (
                                        <div className="grid md:grid-cols-2 gap-4 mt-4">
                                            <div>
                                                <div className="text-xs text-red-400 font-semibold mb-2">Original Code</div>
                                                <pre className="bg-dark-900/70 border border-red-500/30 rounded-lg p-3 overflow-x-auto">
                                                    <code className="text-xs text-dark-300 font-mono">{issue.original_code}</code>
                                                </pre>
                                            </div>
                                            <div>
                                                <div className="text-xs text-green-400 font-semibold mb-2">Fixed Code</div>
                                                <pre className="bg-dark-900/70 border border-green-500/30 rounded-lg p-3 overflow-x-auto">
                                                    <code className="text-xs text-dark-300 font-mono">{issue.fixed_code}</code>
                                                </pre>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
