'use client';

import { useState, useEffect, useRef } from 'react';
import { Terminal, ChevronDown, ChevronUp } from 'lucide-react';
import { API_URL } from '@/lib/api';

interface LiveLogsProps {
    auditId: number;
    status: string;
}

interface LogEntry {
    timestamp: string;
    level: string;
    message: string;
}

export default function LiveLogs({ auditId, status }: LiveLogsProps) {
    const [logs, setLogs] = useState<LogEntry[]>([]);
    const [isCollapsed, setIsCollapsed] = useState(false);
    const logsContainerRef = useRef<HTMLDivElement>(null);

    // Auto-scroll inside the container when new logs arrive
    const scrollToBottom = () => {
        if (logsContainerRef.current) {
            // Smoothly scroll the log container to the bottom
            logsContainerRef.current.scrollTo({
                top: logsContainerRef.current.scrollHeight,
                behavior: 'smooth'
            });
        }
    };

    useEffect(() => {
        scrollToBottom();
    }, [logs]);

    useEffect(() => {
        const fetchLogs = async () => {
            try {
                const response = await fetch(`${API_URL}/api/audits/${auditId}`);
                const data = await response.json();

                if (data.logs && Array.isArray(data.logs)) {
                    setLogs(data.logs);
                }
            } catch (error) {
                console.error('Failed to fetch logs:', error);
            }
        };

        // Initial fetch
        fetchLogs();

        // Poll every 2 seconds if audit is in progress
        const interval = setInterval(() => {
            if (!['completed', 'failed'].includes(status)) {
                fetchLogs();
            }
        }, 2000);

        return () => clearInterval(interval);
    }, [auditId, status]);

    const getLogColor = (level: string) => {
        switch (level.toLowerCase()) {
            case 'error':
                return 'text-red-400';
            case 'warning':
                return 'text-yellow-400';
            case 'success':
                return 'text-green-400';
            case 'info':
            default:
                return 'text-blue-400';
        }
    };

    return (
        <div className="glass-card rounded-2xl overflow-hidden">
            {/* Header */}
            <div
                className="flex items-center justify-between p-4 bg-dark-800/50 cursor-pointer hover:bg-dark-800/70 transition-colors"
                onClick={() => setIsCollapsed(!isCollapsed)}
            >
                <div className="flex items-center gap-2">
                    <Terminal className="w-5 h-5 text-green-400" />
                    <h2 className="text-lg font-bold text-dark-50">Live Logs</h2>
                    <span className="text-xs text-dark-500">({logs.length} entries)</span>
                </div>
                <button className="p-1 hover:bg-dark-700/50 rounded">
                    {isCollapsed ? (
                        <ChevronDown className="w-5 h-5 text-dark-400" />
                    ) : (
                        <ChevronUp className="w-5 h-5 text-dark-400" />
                    )}
                </button>
            </div>

            {/* Logs Content */}
            {!isCollapsed && (
                <div
                    ref={logsContainerRef}
                    className="bg-dark-950/90 p-4 font-mono text-sm max-h-96 overflow-y-auto scroll-smooth"
                >
                    {logs.length === 0 ? (
                        <div className="text-dark-500 text-center py-8">
                            <Terminal className="w-8 h-8 mx-auto mb-2 opacity-50" />
                            <p>No logs yet. Audit will start soon...</p>
                        </div>
                    ) : (
                        <div className="space-y-1">
                            {logs.map((log, index) => (
                                <div key={index} className="flex gap-3 hover:bg-dark-800/30 px-2 py-1 rounded">
                                    <span className="text-dark-600 text-xs flex-shrink-0 w-20">
                                        {new Date(log.timestamp).toLocaleTimeString()}
                                    </span>
                                    <span className={`${getLogColor(log.level)} text-xs uppercase flex-shrink-0 w-16`}>
                                        [{log.level}]
                                    </span>
                                    <span className="text-dark-300 flex-1 break-all">
                                        {log.message}
                                    </span>
                                </div>
                            ))}
                        </div>
                    )}

                    {/* Live indicator */}
                    {!['completed', 'failed'].includes(status) && logs.length > 0 && (
                        <div className="mt-4 pt-4 border-t border-dark-800/50 flex items-center gap-2 text-xs text-dark-500">
                            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                            <span>Live - Updates every 2 seconds</span>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
