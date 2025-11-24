module.exports = {
  root: true,
  parser: '@typescript-eslint/parser',
  parserOptions: {
    sourceType: 'module'
  },
  plugins: ['svelte'],
  extends: ['eslint:recommended', 'plugin:svelte/recommended', 'prettier'],
  ignorePatterns: ['build/', '.svelte-kit/'],
  overrides: [
    {
      files: ['*.svelte'],
      processor: 'svelte/svelte'
    }
  ],
  env: {
    browser: true,
    es2022: true
  }
};
