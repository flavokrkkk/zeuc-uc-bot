import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import svgr from "vite-plugin-svgr";
import path from "path";
import vitePluginBundleObfuscator from "vite-plugin-bundle-obfuscator";
export default defineConfig({
    server: {
        host: "0.0.0.0",
        port: 3000,
    },
    build: {
        minify: "terser",
    },
    plugins: [
        react(),
        svgr({
            svgrOptions: {
                exportType: "default",
                ref: true,
                svgo: false,
                titleProp: true,
            },
            include: ["**/*.svg"],
        }),
        vitePluginBundleObfuscator({
            enable: true,
            log: false,
            autoExcludeNodeModules: true,
            threadPool: true,
            options: {
                compact: true,
                controlFlowFlattening: true,
                identifierNamesGenerator: "hexadecimal",
                deadCodeInjection: false,
                debugProtection: false,
                disableConsoleOutput: false,
                selfDefending: true,
                simplify: true,
                stringArray: false,
                stringArrayCallsTransform: false,
                stringArrayEncoding: [],
                stringArrayThreshold: 0.75,
                unicodeEscapeSequence: false,
            },
        }),
    ],
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "src"),
            "@app": path.resolve(__dirname, "src/app"),
            "@pages": path.resolve(__dirname, "src/pages"),
            "@widgets": path.resolve(__dirname, "src/widgets"),
            "@features": path.resolve(__dirname, "src/features"),
            "@entities": path.resolve(__dirname, "src/entities"),
            "@shared": path.resolve(__dirname, "src/shared"),
            "@lib": path.resolve(__dirname, "src/lib"),
        },
    },
});
