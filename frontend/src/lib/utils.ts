/**
 * Utility functions for the frontend
 */

/**
 * Format date to relative time (e.g., "2 hours ago")
 */
export function formatRelativeTime(dateString: string): string {
    const date = new Date(dateString);
    const now = new Date();
    const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);

    if (diffInSeconds < 60) return 'just now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
    if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)} days ago`;

    return date.toLocaleDateString();
}

/**
 * Get status color based on audit status
 */
export function getStatusColor(status: string): string {
    const colors: Record<string, string> = {
        pending: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
        cloning: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
        analyzing: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
        fixing: 'bg-indigo-500/20 text-indigo-400 border-indigo-500/30',
        validating: 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30',
        creating_pr: 'bg-pink-500/20 text-pink-400 border-pink-500/30',
        completed: 'bg-green-500/20 text-green-400 border-green-500/30',
        failed: 'bg-red-500/20 text-red-400 border-red-500/30',
    };

    return colors[status] || colors.pending;
}

/**
 * Get severity color
 */
export function getSeverityColor(severity: string): string {
    const colors: Record<string, string> = {
        low: 'text-blue-400',
        medium: 'text-yellow-400',
        high: 'text-orange-400',
        critical: 'text-red-400',
    };

    return colors[severity] || colors.low;
}

/**
 * Format status text for display
 */
export function formatStatus(status: string): string {
    return status
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

/**
 * Calculate progress percentage
 */
export function calculateProgress(audit: { processed_files: number; total_files: number }): number {
    if (audit.total_files === 0) return 0;
    return Math.round((audit.processed_files / audit.total_files) * 100);
}

/**
 * Truncate text with ellipsis
 */
export function truncate(text: string, maxLength: number): string {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}
