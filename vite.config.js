import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
	plugins: [sveltekit()],
	optimizeDeps: {
    exclude: ['layercake']
	},
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	},
  define: {
    'import.meta.env.BUILD_TIME': JSON.stringify(new Date().toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' }))
  }
});