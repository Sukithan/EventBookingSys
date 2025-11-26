// https://nuxt.com/docs/api/configuration/nuxt-config
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

export default defineNuxtConfig({
    compatibilityDate: '2024-11-01',
    devtools: { enabled: true },

    // Global CSS
    css: [
        'vuetify/lib/styles/main.sass',
        '@mdi/font/css/materialdesignicons.min.css',
        '~/assets/css/main.css',
    ],

    build: {
        transpile: ['vuetify'],
    },

    modules: [
        '@nuxtjs/tailwindcss',
        (_options, nuxt) => {
            nuxt.hooks.hook('vite:extendConfig', (config) => {
                // @ts-ignore
                config.plugins.push(vuetify({ autoImport: true }))
            })
        },
    ],

    vite: {
        vue: {
            template: {
                transformAssetUrls,
            },
        },
    },

    // Runtime config for API
    runtimeConfig: {
        public: {
            apiBase: process.env.API_BASE_URL || 'http://localhost:8000'
        }
    },

    // SSR Configuration
    ssr: true,

    // Ensure proper hydration
    app: {
        head: {
            script: [
                {
                    innerHTML: `
                        // Prevent FOUC (Flash of Unstyled Content) for auth state
                        window.__NUXT_AUTH_LOADING__ = true;
                    `
                }
            ]
        }
    },

    // Experimental features for better hydration
    experimental: {
        payloadExtraction: false
    },

    // Tailwind CSS configuration
    tailwindcss: {
        cssPath: '~/assets/css/tailwind.css',
        configPath: 'tailwind.config.js',
        exposeConfig: false,
        viewer: true,
    }
})
