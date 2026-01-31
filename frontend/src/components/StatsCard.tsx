'use client';

import { Activity, CheckCircle, XCircle, Clock, TrendingUp } from 'lucide-react';
import { Statistics } from '@/lib/api';

interface StatsCardProps {
    stats: Statistics;
}

export default function StatsCard({ stats }: StatsCardProps) {
    const statItems = [
        {
            label: 'Total Audits',
            value: stats.total_audits,
            icon: Activity,
            color: 'from-blue-500 to-cyan-500',
        },
        {
            label: 'Completed',
            value: stats.completed_audits,
            icon: CheckCircle,
            color: 'from-green-500 to-emerald-500',
        },
        {
            label: 'Pending',
            value: stats.pending_audits,
            icon: Clock,
            color: 'from-yellow-500 to-orange-500',
        },
        {
            label: 'Failed',
            value: stats.failed_audits,
            icon: XCircle,
            color: 'from-red-500 to-pink-500',
        },
        {
            label: 'Issues Found',
            value: stats.total_issues_found,
            icon: TrendingUp,
            color: 'from-purple-500 to-pink-500',
        },
        {
            label: 'Fixes Applied',
            value: stats.total_fixes_applied,
            icon: CheckCircle,
            color: 'from-indigo-500 to-purple-500',
        },
    ];

    return (
        <div className="glass-card rounded-2xl p-6 animate-fade-in">
            <h2 className="text-xl font-bold text-dark-50 mb-6">Statistics</h2>

            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {statItems.map((item, index) => (
                    <div
                        key={item.label}
                        className="p-4 bg-dark-800/50 rounded-xl border border-dark-700/50 hover:border-dark-600/50 transition-all duration-300 hover:scale-105"
                        style={{ animationDelay: `${index * 50}ms` }}
                    >
                        <div className={`inline-flex p-2 bg-gradient-to-br ${item.color} rounded-lg mb-3`}>
                            <item.icon className="w-5 h-5 text-white" />
                        </div>
                        <div className="text-2xl font-bold text-dark-50 mb-1">
                            {item.value.toLocaleString()}
                        </div>
                        <div className="text-xs text-dark-400 uppercase tracking-wide">
                            {item.label}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
