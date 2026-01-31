/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    swcMinify: true,
    output: 'standalone',
    productionBrowserSourceMaps: false,
    eslint: {
        ignoreDuringBuilds: true,
    },
    typescript: {
        ignoreBuildErrors: true,
    },
    // Minimize image optimization memory usage
    images: {
        unoptimized: true,
    }
}

module.exports = nextConfig
