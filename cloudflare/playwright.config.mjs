import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests', testMatch: 'browser.spec.mjs', timeout: 45000,
  fullyParallel: false, workers: 1, retries: 0,
  reporter: [['list'], ['json', { outputFile: 'dist/verification/browser.json' }]],
  use: { baseURL: 'http://127.0.0.1:8787', headless: true,
    channel: process.env.PLAYWRIGHT_CHANNEL || undefined,
    screenshot: 'only-on-failure', trace: 'retain-on-failure' },
  projects: [
    { name: 'desktop', use: { viewport: { width: 1280, height: 900 } } },
    { name: 'mobile', use: { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true } },
  ],
});
