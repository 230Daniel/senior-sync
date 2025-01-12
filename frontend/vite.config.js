import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react-swc';

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
    const env = loadEnv(mode, process.cwd(), 'APP_');
    return {
        plugins: [react()],
        define: {
            __APP_BACKEND: JSON.stringify(env.APP_BACKEND),
        },
        optimizeDeps: {
            esbuildOptions: {
                target: 'esnext'
            }
        },
    };
});
