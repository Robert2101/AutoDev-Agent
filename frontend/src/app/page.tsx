'use client';

import { useState, useEffect } from 'react';
import { Bot, Github, Sparkles, RefreshCw, ExternalLink } from 'lucide-react';
import RepoForm from '@/components/RepoForm';
import StatsCard from '@/components/StatsCard';
import AuditList from '@/components/AuditList';
import { auditAPI, Audit, Statistics } from '@/lib/api';

export default function HomePage() {
    const [audits, setAudits] = useState<Audit[]>([]);
    const [stats, setStats] = useState<Statistics | null>(null);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);

    const fetchData = async () => {
        try {
            const [auditsData, statsData] = await Promise.all([
                auditAPI.getAudits(),
                auditAPI.getStatistics(),
            ]);
            setAudits(auditsData);
            setStats(statsData);
        } catch (error) {
            console.error('Failed to fetch data:', error);
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    useEffect(() => {
        fetchData();

        // Auto-refresh every 10 seconds
        const interval = setInterval(fetchData, 10000);
        return () => clearInterval(interval);
    }, []);

    const handleRefresh = () => {
        setRefreshing(true);
        fetchData();
    };

    return (
        <div className="min-h-screen">
            {/* Header */}
            <header className="border-b border-dark-800/50 backdrop-blur-xl sticky top-0 z-50 bg-dark-950/80">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-gradient-to-br from-primary-500 to-purple-500 rounded-lg glow">
                                <Bot className="w-6 h-6 text-white" />
                            </div>
                            <div>
                                <h1 className="text-xl font-bold gradient-text">AutoDev Agent</h1>
                                <p className="text-xs text-dark-500">AI-Powered Code Auditing</p>
                            </div>
                        </div>

                        <div className="flex items-center gap-4">
                            <button
                                onClick={handleRefresh}
                                disabled={refreshing}
                                className="p-2 hover:bg-dark-800/50 rounded-lg transition-colors"
                                title="Refresh"
                            >
                                <RefreshCw className={`w-5 h-5 text-dark-400 ${refreshing ? 'animate-spin' : ''}`} />
                            </button>

                            <a
                                href="https://github.com/your-org/autodev-agent"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="flex items-center gap-2 px-4 py-2 bg-dark-800/50 hover:bg-dark-700/50 rounded-lg transition-colors"
                            >
                                <Github className="w-5 h-5 text-dark-400" />
                                <span className="text-sm text-dark-300">GitHub</span>
                            </a>
                        </div>
                    </div>
                </div>
            </header>

            {/* Hero Section */}
            <section className="py-12 px-4 sm:px-6 lg:px-8">
                <div className="max-w-7xl mx-auto text-center">
                    <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary-500/10 border border-primary-500/30 rounded-full mb-6">
                        <Sparkles className="w-4 h-4 text-primary-400" />
                        <span className="text-sm text-primary-400 font-medium">Powered by Google Gemini 2.0 Flash</span>
                    </div>

                    <h2 className="text-4xl md:text-5xl font-bold text-dark-50 mb-4 text-shadow">
                        The Self-Healing Repository
                    </h2>
                    <p className="text-xl text-dark-400 max-w-2xl mx-auto">
                        Submit a GitHub repository, and watch as AI detects bugs, generates fixes,
                        and creates Pull Requests automatically.
                    </p>
                </div>
            </section>

            {/* Main Content */}
            <main className="pb-12 px-4 sm:px-6 lg:px-8">
                <div className="max-w-7xl mx-auto">
                    {loading ? (
                        <div className="flex items-center justify-center py-20">
                            <div className="spinner" />
                            <span className="ml-3 text-dark-400">Loading...</span>
                        </div>
                    ) : (
                        <>
                            {/* Stats */}
                            {stats && (
                                <div className="mb-6">
                                    <StatsCard stats={stats} />
                                </div>
                            )}

                            {/* Related Tools - Quick Access Bar */}
                            <div className="grid md:grid-cols-2 gap-4 mb-8">
                                {/* VibeCraft */}
                                <div className="glass-card rounded-2xl p-4 flex items-center gap-4 border-l-4 border-l-primary-500 hover:bg-dark-800/20 transition-all">
                                    <div className="p-3 bg-primary-500/10 rounded-xl">
                                        <Sparkles className="w-6 h-6 text-primary-400" />
                                    </div>
                                    <div className="flex-1">
                                        <h3 className="text-sm font-bold text-dark-50">VibeCraft Vizualizer</h3>
                                        <p className="text-xs text-dark-400">Interactive codebase dependency graphs.</p>
                                    </div>
                                    <a
                                        href="https://repo-dig.vercel.app/"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="p-2 bg-dark-800/50 hover:bg-primary-500/20 rounded-lg text-primary-400 transition-colors"
                                    >
                                        <ExternalLink className="w-5 h-5" />
                                    </a>
                                </div>

                                {/* Assignment Planner */}
                                <div className="glass-card rounded-2xl p-4 flex items-center gap-4 border-l-4 border-l-purple-500 hover:bg-dark-800/20 transition-all">
                                    <div className="p-3 bg-purple-500/10 rounded-xl">
                                        <Bot className="w-6 h-6 text-purple-400" />
                                    </div>
                                    <div className="flex-1">
                                        <h3 className="text-sm font-bold text-dark-50">Assignment Planner Pro</h3>
                                        <p className="text-xs text-dark-400">Smart project planning & task management.</p>
                                    </div>
                                    <a
                                        href="https://spectacular-gumdrop-c2c3c7.netlify.app/"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="p-2 bg-dark-800/50 hover:bg-purple-500/20 rounded-lg text-purple-400 transition-colors"
                                    >
                                        <ExternalLink className="w-5 h-5" />
                                    </a>
                                </div>
                            </div>
                            <div className="grid lg:grid-cols-3 gap-8">
                                {/* Submission Form */}
                                <div className="lg:col-span-1 space-y-6">
                                    <RepoForm onAuditCreated={fetchData} />



                                    {/* How It Works Guide */}
                                    <div className="glass-card rounded-2xl p-6">
                                        <h3 className="text-lg font-bold text-dark-50 mb-4 flex items-center gap-2">
                                            <Sparkles className="w-5 h-5 text-yellow-400" />
                                            How It Works
                                        </h3>
                                        <ul className="space-y-3 text-sm text-dark-300">
                                            <li className="flex gap-2">
                                                <span className="text-primary-400 font-bold">1.</span>
                                                <span><strong className="text-white">Submit Repo</strong>: Enter any public GitHub URL. We auto-detect the branch.</span>
                                            </li>
                                            <li className="flex gap-2">
                                                <span className="text-primary-400 font-bold">2.</span>
                                                <span><strong className="text-white">AI Analysis</strong>: Gemini 2.0 Flash scans for bugs & security issues.</span>
                                            </li>
                                            <li className="flex gap-2">
                                                <span className="text-primary-400 font-bold">3.</span>
                                                <span><strong className="text-white">Auto-Fix</strong>: The agent generates fixes and validates them.</span>
                                            </li>
                                            <li className="flex gap-2">
                                                <span className="text-primary-400 font-bold">4.</span>
                                                <span><strong className="text-white">Pull Request</strong>: A PR is automatically created with fixes!</span>
                                            </li>
                                        </ul>
                                    </div>
                                </div>

                                {/* Audit List */}
                                <div className="lg:col-span-2">
                                    <AuditList audits={audits} onRefresh={fetchData} />
                                </div>
                            </div>
                        </>
                    )}
                </div>
            </main>

            {/* Footer */}
            <footer className="border-t border-dark-800/50 py-8 px-4 sm:px-6 lg:px-8">
                <div className="max-w-7xl mx-auto text-center text-dark-500 text-sm">
                    <p>Built with ❤️ using AI-powered development</p>
                    <p className="mt-2">Powered by Google Gemini, FastAPI, Next.js, and Docker</p>
                </div>
            </footer>
        </div>
    );
}
