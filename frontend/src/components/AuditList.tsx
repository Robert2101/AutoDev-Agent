'use client';

import { Audit, deleteAudit } from '@/lib/api';
import { formatRelativeTime, getStatusColor, formatStatus, calculateProgress } from '@/lib/utils';
import { ExternalLink, GitBranch, FileCode, AlertTriangle, CheckCircle, Trash2 } from 'lucide-react';
import Link from 'next/link';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

interface AuditListProps {
    audits: Audit[];
    onRefresh?: () => void;
}

export default function AuditList({ audits, onRefresh }: AuditListProps) {
    const router = useRouter();
    const [deletingId, setDeletingId] = useState<number | null>(null);

    const handleDelete = async (e: React.MouseEvent, auditId: number) => {
        e.preventDefault();
        e.stopPropagation();

        if (!confirm('Are you sure you want to delete this audit?')) {
            return;
        }

        setDeletingId(auditId);

        try {
            await deleteAudit(auditId);

            // Refresh the page or call refresh callback
            if (onRefresh) {
                onRefresh();
            } else {
                router.refresh();
            }
        } catch (error) {
            console.error('Failed to delete audit:', error);
            alert('Failed to delete audit. Please try again.');
        } finally {
            setDeletingId(null);
        }
    };

    if (audits.length === 0) {
        return (
            <div className="glass-card rounded-2xl p-12 text-center">
                <div className="inline-flex p-4 bg-dark-800/50 rounded-full mb-4">
                    <FileCode className="w-8 h-8 text-dark-500" />
                </div>
                <h3 className="text-xl font-semibold text-dark-400 mb-2">No audits yet</h3>
                <p className="text-dark-500">Submit a repository to get started</p>
            </div>
        );
    }

    return (
        <div className="glass-card rounded-2xl p-6">
            <h2 className="text-xl font-bold text-dark-50 mb-6">Recent Audits</h2>

            <div className="space-y-4">
                {audits.map((audit, index) => (
                    <Link
                        key={audit.id}
                        href={`/audit/${audit.id}`}
                        className="block"
                        style={{ animationDelay: `${index * 50}ms` }}
                    >
                        <div className="p-5 bg-dark-800/50 rounded-xl border border-dark-700/50 hover:border-primary-500/50 transition-all duration-300 hover:scale-[1.02] cursor-pointer group">
                            {/* Header */}
                            <div className="flex items-start justify-between mb-4">
                                <div className="flex-1">
                                    <div className="flex items-center gap-2 mb-2">
                                        <GitBranch className="w-4 h-4 text-primary-400" />
                                        <span className="text-sm font-mono text-dark-400">
                                            Audit #{audit.id}
                                        </span>
                                        <span className={`status-badge ${getStatusColor(audit.status)} border`}>
                                            {formatStatus(audit.status)}
                                        </span>
                                    </div>
                                    <p className="text-xs text-dark-500">
                                        Created {formatRelativeTime(audit.created_at)}
                                    </p>
                                </div>

                                <div className="flex items-center gap-2">
                                    {audit.pr_url && (
                                        <a
                                            href={audit.pr_url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="flex items-center gap-1 text-sm text-primary-400 hover:text-primary-300 transition-colors"
                                            onClick={(e) => e.stopPropagation()}
                                        >
                                            <span>View PR</span>
                                            <ExternalLink className="w-4 h-4" />
                                        </a>
                                    )}

                                    {/* Delete Button for ALL audits to allow manual queue management */}
                                    {true && (
                                        <button
                                            onClick={(e) => handleDelete(e, audit.id)}
                                            disabled={deletingId === audit.id}
                                            className="p-2 rounded-lg bg-red-500/10 border border-red-500/30 hover:bg-red-500/20 hover:border-red-500/50 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed group/delete"
                                            title="Delete audit"
                                        >
                                            {deletingId === audit.id ? (
                                                <div className="w-4 h-4 border-2 border-red-400 border-t-transparent rounded-full animate-spin" />
                                            ) : (
                                                <Trash2 className="w-4 h-4 text-red-400 group-hover/delete:text-red-300 transition-colors" />
                                            )}
                                        </button>
                                    )}
                                </div>
                            </div>

                            {/* Progress Bar */}
                            {audit.status !== 'completed' && audit.status !== 'failed' && audit.total_files > 0 && (
                                <div className="mb-4">
                                    <div className="flex justify-between text-xs text-dark-400 mb-2">
                                        <span>{audit.processed_files} / {audit.total_files} files</span>
                                        <span>{calculateProgress(audit)}%</span>
                                    </div>
                                    <div className="h-2 bg-dark-700 rounded-full overflow-hidden">
                                        <div
                                            className="h-full bg-gradient-to-r from-primary-500 to-purple-500 transition-all duration-500 rounded-full"
                                            style={{ width: `${calculateProgress(audit)}%` }}
                                        />
                                    </div>
                                </div>
                            )}

                            {/* Stats */}
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                <div>
                                    <div className="text-xs text-dark-500 mb-1">Files</div>
                                    <div className="text-lg font-semibold text-dark-300">{audit.total_files}</div>
                                </div>
                                <div>
                                    <div className="text-xs text-dark-500 mb-1">Issues Found</div>
                                    <div className="flex items-center gap-1">
                                        <AlertTriangle className="w-4 h-4 text-yellow-400" />
                                        <span className="text-lg font-semibold text-dark-300">{audit.issues_found}</span>
                                    </div>
                                </div>
                                <div>
                                    <div className="text-xs text-dark-500 mb-1">Fixes Applied</div>
                                    <div className="flex items-center gap-1">
                                        <CheckCircle className="w-4 h-4 text-green-400" />
                                        <span className="text-lg font-semibold text-dark-300">{audit.fixes_applied}</span>
                                    </div>
                                </div>
                                <div>
                                    <div className="text-xs text-dark-500 mb-1">PR Number</div>
                                    <div className="text-lg font-semibold text-dark-300">
                                        {audit.pr_number ? `#${audit.pr_number}` : '-'}
                                    </div>
                                </div>
                            </div>

                            {/* Error Message */}
                            {audit.error_message && (
                                <div className="mt-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
                                    <p className="text-xs text-red-400">{audit.error_message}</p>
                                </div>
                            )}
                        </div>
                    </Link>
                ))}
            </div>
        </div>
    );
}
