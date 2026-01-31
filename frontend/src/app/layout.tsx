import type { Metadata } from 'next';
import '../styles/globals.css';

export const metadata: Metadata = {
    title: 'AutoDev Agent - AI-Powered Code Auditing',
    description: 'An autonomous AI agent that audits GitHub repositories, detects bugs and security vulnerabilities, and automatically creates Pull Requests with fixes.',
    keywords: ['AI', 'code review', 'GitHub', 'automation', 'bug detection', 'security'],
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body className="min-h-screen">
                {children}
            </body>
        </html>
    );
}
