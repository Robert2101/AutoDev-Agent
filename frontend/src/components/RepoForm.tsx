'use client';

import { useState } from 'react';
import { Github, Sparkles, AlertCircle, Settings, ChevronDown, ChevronUp, Key } from 'lucide-react';
import { auditAPI } from '@/lib/api';

interface RepoFormProps {
    onAuditCreated: () => void;
}

export default function RepoForm({ onAuditCreated }: RepoFormProps) {
    const [url, setUrl] = useState('');
    const [branch, setBranch] = useState('main');

    // Advanced Settings State
    const [showAdvanced, setShowAdvanced] = useState(false);
    const [githubToken, setGithubToken] = useState('');
    const [geminiKey, setGeminiKey] = useState('');

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            await auditAPI.createAudit(url, branch, githubToken, geminiKey);
            setUrl('');
            setBranch('main');
            // Optional: reset keys or keep them
            setGithubToken('');
            setGeminiKey('');
            setShowAdvanced(false);
            onAuditCreated();
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to create audit. Please check the URL and try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="glass-card rounded-2xl p-8 animate-slide-up">
            <div className="flex items-center gap-3 mb-6">
                <div className="p-3 bg-gradient-to-br from-primary-500 to-purple-500 rounded-xl glow">
                    <Github className="w-6 h-6 text-white" />
                </div>
                <div>
                    <h2 className="text-2xl font-bold text-dark-50">Submit Repository</h2>
                    <p className="text-dark-400 text-sm">Let AI audit your code and create fixes</p>
                </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label htmlFor="url" className="block text-sm font-medium text-dark-300 mb-2">
                        GitHub Repository URL
                    </label>
                    <input
                        type="url"
                        id="url"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        placeholder="https://github.com/username/repository"
                        className="input-field w-full"
                        required
                    />
                    <p className="text-xs text-dark-500 mt-1">
                        Example: https://github.com/facebook/react
                    </p>
                </div>

                <div>
                    <label htmlFor="branch" className="block text-sm font-medium text-dark-300 mb-2">
                        Branch
                    </label>
                    <input
                        type="text"
                        id="branch"
                        value={branch}
                        onChange={(e) => setBranch(e.target.value)}
                        placeholder="main"
                        className="input-field w-full"
                        required
                    />
                </div>

                {error && (
                    <div className="flex items-start gap-2 p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
                        <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                        <p className="text-sm text-red-400">{error}</p>
                    </div>
                )}

                {/* Advanced Settings Toggle */}
                <div className="pt-2 border-t border-dark-700/50">
                    <button
                        type="button"
                        onClick={() => setShowAdvanced(!showAdvanced)}
                        className="flex items-center gap-2 text-sm text-dark-400 hover:text-primary-400 transition-colors"
                    >
                        <Settings className="w-4 h-4" />
                        <span>Advanced Settings (Custom Keys)</span>
                        {showAdvanced ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </button>

                    {showAdvanced && (
                        <div className="mt-4 space-y-4 animate-slide-up p-4 bg-dark-800/50 rounded-lg border border-dark-700/50">
                            <div>
                                <label className="block text-xs font-medium text-dark-400 mb-1">
                                    Custom GitHub Token (Optional)
                                </label>
                                <div className="relative">
                                    <Key className="absolute left-3 top-2.5 w-4 h-4 text-dark-500" />
                                    <input
                                        type="password"
                                        value={githubToken}
                                        onChange={(e) => setGithubToken(e.target.value)}
                                        placeholder="ghp_..."
                                        className="input-field w-full pl-10 text-sm"
                                    />
                                </div>
                                <p className="text-[10px] text-dark-500 mt-1">Overrides system default. Needed for private repos.</p>
                            </div>

                            <div>
                                <label className="block text-xs font-medium text-dark-400 mb-1">
                                    Custom Gemini API Key (Optional)
                                </label>
                                <div className="relative">
                                    <Sparkles className="absolute left-3 top-2.5 w-4 h-4 text-dark-500" />
                                    <input
                                        type="password"
                                        value={geminiKey}
                                        onChange={(e) => setGeminiKey(e.target.value)}
                                        placeholder="AIza..."
                                        className="input-field w-full pl-10 text-sm"
                                    />
                                </div>
                                <p className="text-[10px] text-dark-500 mt-1">Use your own quota/tier.</p>
                            </div>
                        </div>
                    )}
                </div>

                <button
                    type="submit"
                    disabled={loading || !url}
                    className="btn-gradient w-full flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                >
                    {loading ? (
                        <>
                            <div className="spinner" />
                            <span>Creating Audit...</span>
                        </>
                    ) : (
                        <>
                            <Sparkles className="w-5 h-5" />
                            <span>Start AI Audit</span>
                        </>
                    )}
                </button>
            </form>

            <div className="mt-6 p-4 bg-dark-800/30 rounded-lg border border-dark-700/30">
                <h3 className="text-sm font-semibold text-dark-300 mb-2">What happens next?</h3>
                <ul className="text-xs text-dark-400 space-y-1">
                    <li>✓ Repository is cloned and analyzed</li>
                    <li>✓ AI detects bugs and security issues</li>
                    <li>✓ Automated fixes are generated</li>
                    <li>✓ Pull Request is created for review</li>
                </ul>
            </div>
        </div>
    );
}
